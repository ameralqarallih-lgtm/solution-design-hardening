"""Built-in benchmark transports. Output stores measurements supplied by the host."""

import json
import math
import os
import re
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


CLIS = {"claude-code": "claude", "codex": "codex", "copilot": "copilot"}
API_DEFAULTS = {
    "openai": "https://api.openai.com/v1",
    "ollama": "http://127.0.0.1:11434/v1",
    "litellm": "http://127.0.0.1:4000/v1",
    "lm-studio": "http://127.0.0.1:1234/v1",
}
API_KEYS = {"openai": "OPENAI_API_KEY"}
AGENTS = (*CLIS, *API_DEFAULTS, "openai-compatible", "mock")
REQUIRED_FLAGS = {
    "codex": ("--ignore-user-config", "--ignore-rules", "--ephemeral", "--json", "--sandbox"),
    "claude-code": ("--tools", "--strict-mcp-config", "--setting-sources", "--no-session-persistence"),
    "copilot": ("--available-tools", "--disable-builtin-mcps", "--output-format"),
}
MAX_RESPONSE = 1_000_000
STOP_STATUSES = {"auth_error", "configuration_error"}
RETRYABLE_STATUSES = {"adapter_error", "connection_error", "rate_limited", "service_error", "timeout"}


class AdapterError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


def failure(status, message):
    return {"status": status, "message": message}


def successful(response, usage=None, cost=None, model=None):
    if not isinstance(response, str) or not response.strip():
        raise AdapterError("invalid_output", "The agent returned no final text.")
    usage = {key: value for key, value in (usage or {}).items()
             if type(value) is int and value >= 0}
    if usage.get("cached_input_tokens", 0) > usage.get("input_tokens", 0):
        usage.pop("cached_input_tokens")
    result = {"status": "ok", "response": response, "usage": usage, "activation": "unknown"}
    if type(cost) in (int, float) and math.isfinite(cost) and cost >= 0:
        result["cost_usd"] = cost
    if isinstance(model, str) and model.strip():
        result["reported_model"] = model
    return result


def event_records(raw):
    events = [json.loads(line) for line in raw.splitlines() if line.strip()]
    if not all(isinstance(event, dict) for event in events):
        raise ValueError("expected JSONL objects")
    return events


def openai_result(data, cost=None):
    choice = data["choices"][0]
    message = choice["message"]
    usage = data.get("usage") or {}
    details = usage.get("prompt_tokens_details") or {}
    result = successful(message.get("content"), {
        "input_tokens": usage.get("prompt_tokens"),
        "output_tokens": usage.get("completion_tokens"),
        "cached_input_tokens": details.get("cached_tokens"),
    }, cost=cost, model=data.get("model"))
    if choice.get("finish_reason") == "length":
        result["output_limit_reached"] = True
    return result


def cli_result(agent, raw):
    if agent == "claude-code":
        data = json.loads(raw)
        if data.get("is_error") or data.get("subtype") != "success":
            raise cli_failure(raw)
        usage = data.get("usage") or {}
        # Anthropic supplies uncached, cache-write and cache-read input separately.
        input_counts = [usage.get(key, 0) for key in
                        ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")]
        total = (sum(input_counts) if "input_tokens" in usage
                 and all(type(n) is int and n >= 0 for n in input_counts) else None)
        models = list(data.get("modelUsage") or {})
        return successful(data.get("result"), {
            "input_tokens": total,
            "output_tokens": usage.get("output_tokens"),
            "cached_input_tokens": usage.get("cache_read_input_tokens"),
        }, cost=data.get("total_cost_usd"), model=models[0] if len(models) == 1 else None)

    events = event_records(raw)
    if agent == "codex":
        turns = [event for event in events if event.get("type") == "turn.completed"]
        if not turns:
            raise cli_failure(raw)
        messages = [event["item"].get("text") for event in events
                    if event.get("type") == "item.completed"
                    and event["item"].get("type") == "agent_message"]
        usage = turns[-1].get("usage") or {}
        return successful(messages[-1] if messages else None, {
            key: usage.get(key) for key in
            ("input_tokens", "output_tokens", "cached_input_tokens")
        })

    messages = [event.get("data", {}).get("content") for event in events
                if event.get("type") == "assistant.message"
                and not event.get("data", {}).get("toolRequests")]
    calls = [event["data"] for event in events if event.get("type") == "assistant.usage"]
    usage = {}
    for field, key in (("inputTokens", "input_tokens"), ("outputTokens", "output_tokens"),
                       ("cacheReadTokens", "cached_input_tokens")):
        counts = [call.get(field) for call in calls]
        if counts and all(type(n) is int and n >= 0 for n in counts):
            usage[key] = sum(counts)
    models = {call.get("model") for call in calls if isinstance(call.get("model"), str)}
    return successful(messages[-1] if messages else None, usage,
                      model=next(iter(models)) if len(models) == 1 else None)


def cli_failure(output):
    # Inspect locally for known errors. Avoid persisting raw stderr, which can include secrets.
    output = output.decode("utf-8", errors="replace").lower()
    if re.search(r"\b(401|403)\b|not logged in|unauthorized|authentication failed|"
                 r"invalid api key|please (?:log|sign) in|not authenticated", output):
        return AdapterError("auth_error", "Agent authentication failed. Sign in or check its credential.")
    if re.search(r"unknown (?:option|argument)|unexpected argument|unrecognized option|"
                 r"unsupported model|model not found|invalid model", output):
        return AdapterError("configuration_error", "Check the agent version and selected model.")
    if re.search(r"\b429\b|rate.limit|too many requests", output):
        return AdapterError("rate_limited", "The agent reached its rate limit.")
    return AdapterError("adapter_error", "The agent exited unsuccessfully. Run doctor --probe to diagnose it.")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def api_url(value):
    if not isinstance(value, str):
        raise ValueError("Set the API base URL with --base-url or OPENAI_BASE_URL.")
    try:
        parts = urlsplit(value)
        if (parts.scheme not in ("http", "https") or not parts.hostname or parts.username is not None
                or parts.query or parts.fragment or any(c.isspace() for c in value)):
            raise ValueError
        _ = parts.port
    except ValueError:
        raise ValueError("Use an HTTP(S) API base URL without credentials, query, or fragment.") from None
    return value.rstrip("/")


def cli_run(command, cwd, timeout, prompt=None):
    env = os.environ.copy()
    for name in ("COPILOT_ALLOW_ALL", "GITHUB_COPILOT_PROMPT_MODE_EXTENSIONS"):
        env.pop(name, None)
    env["COPILOT_AUTO_UPDATE"] = "false"
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        options = {"stdin": subprocess.DEVNULL} if prompt is None else {"input": prompt.encode("utf-8")}
        result = subprocess.run(command, cwd=cwd, env=env, stdout=stdout, stderr=stderr,
                                timeout=timeout, **options)
        stdout.seek(0)
        stderr.seek(0)
        raw = stdout.read(MAX_RESPONSE + 1)
        diagnostic = stderr.read(32768)
    return result.returncode, raw, diagnostic


@dataclass
class Agent:
    name: str
    model: str | None
    base_url: str | None = None
    api_key_env: str | None = None

    def __post_init__(self):
        if self.name not in AGENTS:
            raise ValueError(f"Unknown agent. Choose from: {', '.join(AGENTS)}.")
        if self.model is not None and (not isinstance(self.model, str) or not self.model.strip()
                                       or self.model.startswith("-")):
            raise ValueError("Choose a nonempty model identifier.")
        if self.name in CLIS and self.model and not re.fullmatch(r"[A-Za-z0-9_.:/@+-]+", self.model):
            raise ValueError("Use a CLI model identifier without spaces or shell punctuation.")
        if self.name == "mock":
            self.model = self.model or "synthetic"
        if self.is_api:
            configured_url = os.getenv("OPENAI_BASE_URL") if self.name in ("openai", "openai-compatible") else None
            self.base_url = api_url(self.base_url or configured_url or API_DEFAULTS.get(self.name))
            self.api_key_env = self.api_key_env or API_KEYS.get(self.name)
            if self.api_key_env and (not isinstance(self.api_key_env, str)
                                     or not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", self.api_key_env)):
                raise ValueError("Provide the name of an API key environment variable.")
        elif self.base_url or self.api_key_env:
            raise ValueError("API URL and key options apply only to API adapters.")

    @property
    def is_api(self):
        return self.name not in CLIS and self.name != "mock"

    def identity(self):
        return {"agent": self.name, "model": self.model, "base_url": self.base_url,
                "api_key_env": self.api_key_env}

    def executable(self):
        command = CLIS[self.name]
        executable = shutil.which(command)
        if not executable:
            raise AdapterError("configuration_error", f"Install {command} and place it on PATH.")
        return str(Path(executable).resolve())

    def doctor(self):
        """Check configuration and local login state without invoking a model."""
        if self.name == "mock":
            return {"agent": self.name, "status": "ready", "version": "builtin",
                    "auth": "not_required"}
        if self.is_api:
            if self.api_key_env and not os.getenv(self.api_key_env):
                raise AdapterError("configuration_error", f"Set {self.api_key_env} in the environment.")
            return {"agent": self.name, "status": "configured", "version": "chat-completions",
                    "auth": "credential_present" if self.api_key_env else "not_configured"}
        executable = self.executable()
        with tempfile.TemporaryDirectory(prefix="sdh-doctor-") as directory:
            version_flags = ["--no-auto-update", "--version"] if self.name == "copilot" else ["--version"]
            code, raw, diagnostic = cli_run([executable, *version_flags], directory, 10)
            if code:
                raise cli_failure(raw + diagnostic)
            match = re.search(rb"\b\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?\b", raw + diagnostic)
            version = match[0].decode("ascii") if match else "unknown"
            help_flags = {
                "codex": ["exec", "--help"],
                "claude-code": ["--help"],
                "copilot": ["--no-auto-update", "--help"],
            }
            code, help_text, _ = cli_run([executable, *help_flags[self.name]], directory, 10)
            if code or not all(flag.encode() in help_text for flag in REQUIRED_FLAGS[self.name]):
                raise AdapterError("configuration_error",
                                   f"Update {CLIS[self.name]} for benchmark flags, then rerun doctor.")
            auth = "unverified"
            if self.name in ("codex", "claude-code"):
                flags = ["login", "status"] if self.name == "codex" else ["auth", "status"]
                code, _, _ = cli_run([executable, *flags], directory, 10)
                if code:
                    raise AdapterError("auth_error", f"Sign in to {CLIS[self.name]} and rerun doctor.")
                auth = "local_login_reported"
            elif any(os.getenv(name) for name in ("COPILOT_GITHUB_TOKEN", "GH_TOKEN", "GITHUB_TOKEN")):
                auth = "credential_present"
        return {"agent": self.name, "status": "ready", "version": version, "auth": auth}

    def cli_command(self, workspace):
        executable = self.executable()
        if self.name == "codex":
            return [executable, "-a", "never", "exec", "--sandbox", "read-only", "--json",
                    "--skip-git-repo-check", "--ephemeral", "--ignore-user-config", "--ignore-rules",
                    "--disable", "shell_tool", "--disable", "unified_exec", "--disable", "apps",
                    "--disable", "browser_use", "--disable", "computer_use", "--disable", "plugins",
                    "--enable", "skip_host_skill_discovery", "-c", 'web_search="disabled"',
                    "-c", "project_doc_max_bytes=0", "--model", self.model, "-"]
        if self.name == "claude-code":
            mcp = workspace / "mcp.json"
            mcp.write_text('{"mcpServers":{}}', encoding="utf-8")
            settings = workspace / "settings.json"
            settings.write_text('{"disableAllHooks":true}', encoding="utf-8")
            return [executable, "-p", "--model", self.model, "--output-format", "json",
                    "--tools", "", "--disallowedTools", "mcp__*", "--strict-mcp-config",
                    "--mcp-config", mcp.name, "--setting-sources", "project",
                    "--settings", settings.name, "--no-chrome",
                    "--no-session-persistence"]
        return [executable, "--model", self.model, "--no-auto-update", "--no-ask-user",
                "--no-custom-instructions", "--disable-builtin-mcps", "--available-tools=ask_user",
                "--deny-tool=shell,write,read,url,memory", "--sync-session=off",
                "--output-format=json"]

    def api_request(self, prompt, timeout):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.api_key_env:
            credential = os.getenv(self.api_key_env)
            if not credential:
                raise AdapterError("configuration_error", f"Set {self.api_key_env} in the environment.")
            headers["Authorization"] = f"Bearer {credential}"
        data = {"model": self.model, "messages": [{"role": "user", "content": prompt}], "stream": False}
        request = Request(self.base_url + "/chat/completions", headers=headers,
                          data=json.dumps(data).encode("utf-8"), method="POST")
        try:
            with build_opener(NoRedirect).open(request, timeout=timeout) as response:
                payload = response.read(MAX_RESPONSE + 1)
                cost_header = response.headers.get("x-litellm-response-cost")
        except HTTPError as error:
            with error:
                code = error.code
            if code in (401, 403):
                raise AdapterError("auth_error", f"API rejected the credential or model access (HTTP {code}).")
            if code == 429:
                raise AdapterError("rate_limited", "API rate limit reached (HTTP 429).")
            if 300 <= code < 500:
                raise AdapterError("configuration_error", f"Check the API URL and model (HTTP {code}).")
            raise AdapterError("service_error", f"API failed (HTTP {code}).")
        except URLError as error:
            if isinstance(error.reason, TimeoutError):
                raise AdapterError("timeout", "The API connection timed out.")
            raise AdapterError("connection_error", "Could not connect to the model API. Check its URL and server.")
        if len(payload) > MAX_RESPONSE:
            raise AdapterError("invalid_output", "The API response exceeded the ingestion limit.")
        try:
            cost = float(cost_header) if cost_header is not None else None
        except ValueError:
            cost = None
        return openai_result(json.loads(payload), cost)

    def run(self, prompt, workspace, timeout):
        start = time.monotonic()
        try:
            if self.name == "mock":
                result = successful("SYNTHETIC ADAPTER SMOKE TEST - no model invoked.")
            elif self.is_api:
                result = self.api_request(prompt, timeout)
            else:
                code, raw, diagnostic = cli_run(self.cli_command(workspace), workspace, timeout, prompt)
                if code:
                    raise cli_failure(diagnostic + raw)
                if len(raw) > MAX_RESPONSE:
                    raise AdapterError("invalid_output", "The CLI response exceeded the ingestion limit.")
                result = cli_result(self.name, raw)
        except AdapterError as error:
            result = failure(error.status, str(error))
        except (subprocess.TimeoutExpired, TimeoutError):
            result = failure("timeout", "The agent exceeded the timeout.")
        except OSError:
            result = failure("adapter_error", "Could not start or communicate with the agent.")
        except (ValueError, TypeError, IndexError, KeyError, AttributeError):
            result = failure("invalid_output", "The response did not match the agent's expected output format.")
        return {**result, "wall_seconds": time.monotonic() - start}

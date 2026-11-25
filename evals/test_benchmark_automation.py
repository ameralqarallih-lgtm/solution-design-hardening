import contextlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from xml.etree import ElementTree

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import benchmark
from benchmark import ROOT, read, write
from benchmark_adapters import AdapterError, Agent, cli_result
from benchmark_automation import parse_grade, run_lock
from benchmark_report import generate


def cli(*args):
    with (patch.object(sys, "argv", ["benchmark.py", *map(str, args)]),
          contextlib.redirect_stdout(io.StringIO()),
          contextlib.redirect_stderr(io.StringIO())):
        return benchmark.main()


def result(status="ok", response="Synthetic test observation"):
    return {"status": status, "response": response, "usage": {"input_tokens": 12},
            "wall_seconds": 0.1}


GRADE = {"detection": 2, "remediation": 2, "verification": 1, "safety": 2,
         "safety_violation": False, "notes": "Test reviewer", "true_positives": [],
         "false_positives": []}


class AutomationTests(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory()
        self.addCleanup(workspace.cleanup)
        self.root = Path(workspace.name)
        self.out = self.root / "experiment"

    def evaluate(self, *args):
        return cli("evaluate", self.out, "--agent", "mock", "--cases", "local-transaction", *args)

    def test_cli_smoke_and_report_artifacts(self):
        process = subprocess.run([sys.executable, "-B", str(ROOT / "tools/benchmark.py"),
                                  "evaluate", str(self.out), "--agent", "mock", "--cases", "outbox-crash"],
                                 capture_output=True)
        self.assertEqual(process.returncode, 0, process.stderr.decode("utf-8", errors="replace"))
        self.assertIn(b"[2/2]", process.stderr)
        report = read(self.out / "report.json")
        self.assertTrue(report["synthetic"])
        self.assertIsNone(report["comparisons"]["skill"]["mean_paired_delta_out_of_8"])
        self.assertEqual(report["conditions"]["baseline"]["successful"], 1)
        self.assertEqual(report["grade_sources"], {"human": 0, "automated_provisional": 0})
        self.assertEqual(len(read(self.out / "grades.template.json")), 2)
        self.assertIsNotNone(ElementTree.parse(self.out / "report.svg").getroot())

    def test_run_gets_only_scenario_and_declared_context(self):
        with patch.object(Agent, "run", autospec=True, return_value=result()) as run:
            self.assertEqual(self.evaluate(), 0)
        prompts = [call.args[1] for call in run.call_args_list]
        short, long = sorted(prompts, key=len)
        self.assertTrue(long.endswith(short))
        plan = read(self.out / "plan.private.json")
        self.assertEqual(short, plan["runs"][0]["prompt"])
        self.assertEqual(plan["runs"][0]["prompt"], plan["runs"][1]["prompt"])
        self.assertNotIn(read(self.out / "rubric.private.json")["local-transaction"], long)
        packet = read(self.out / "review.json")
        self.assertTrue(all(set(row) == {"run_id", "case_id", "prompt", "response"} for row in packet))

    def test_resume_retry_preserves_prior_attempt_and_skips_successes(self):
        with patch.object(Agent, "run", side_effect=[result("timeout"), result()]):
            self.assertEqual(self.evaluate(), 1)
        before = {path.name: path.read_bytes() for path in (self.out / "raw.private").glob("*.json")}
        with patch.object(Agent, "run", return_value=result()) as run:
            self.assertEqual(cli("evaluate", self.out, "--resume"), 1)
            run.assert_not_called()
            self.assertEqual(cli("evaluate", self.out, "--resume", "--retry-failed"), 0)
            run.assert_called_once()
        histories = list((self.out / "attempts.private").glob("*/*.json"))
        self.assertEqual(len(histories), 1)
        previous = read(histories[0])
        latest = read(self.out / "raw.private" / (previous["run_id"] + ".json"))
        self.assertEqual(previous["status"], "timeout")
        self.assertEqual(latest["status"], "ok")
        self.assertEqual(latest["attempt"], 2)
        self.assertEqual(histories[0].read_bytes(), before[previous["run_id"] + ".json"])
        report = read(self.out / "report.json")
        self.assertEqual(sum(row["attempts"] for row in report["conditions"].values()), 3)

    def test_transient_retry_and_auth_fail_fast(self):
        with (patch.object(Agent, "run", side_effect=[result("rate_limited"),
                                                     result("auth_error")]) as run,
              patch("benchmark_automation.time.sleep")):
            self.assertEqual(self.evaluate("--retries", "3"), 1)
            self.assertEqual(run.call_count, 2)
        report = read(self.out / "report.json")
        self.assertEqual(sum(row["attempted"] for row in report["conditions"].values()), 1)
        self.assertEqual(sum(row["attempts"] for row in report["conditions"].values()), 2)

    def test_config_is_reusable_and_resume_rejects_setting_changes(self):
        config = self.root / "evaluate.json"
        write(config, {"agent": "mock", "cases": ["outbox-crash"], "trials": 2})
        self.assertEqual(cli("evaluate", self.out, "--config", config, "--trials", "1"), 0)
        self.assertEqual(read(self.out / "plan.private.json")["trials"], 1)
        with self.assertRaises(SystemExit) as error:
            cli("evaluate", self.out, "--resume", "--trials", "2")
        self.assertEqual(error.exception.code, 2)

    def test_tampered_rubric_is_rejected_on_resume(self):
        self.assertEqual(self.evaluate(), 0)
        write(self.out / "rubric.private.json", {"local-transaction": "tampered"})
        with self.assertRaises(SystemExit) as error:
            cli("evaluate", self.out, "--resume")
        self.assertEqual(error.exception.code, 2)

    def test_external_model_requires_opt_in_before_preflight(self):
        with patch.object(Agent, "doctor") as doctor, self.assertRaises(SystemExit) as error:
            cli("evaluate", self.out, "--agent", "codex", "--model", "test-model")
        self.assertEqual(error.exception.code, 2)
        doctor.assert_not_called()
        self.assertFalse(self.out.exists())

    def test_provisional_grades_and_human_override(self):
        def simulate(agent, prompt, *_):
            if agent.model == "independent-judge":
                self.assertNotIn("Apply this reference guidance", prompt)
                self.assertIn('"allowed_true_positives"', prompt)
                return result(response=json.dumps(GRADE))
            return result()

        with patch.object(Agent, "run", autospec=True, side_effect=simulate) as run:
            self.assertEqual(self.evaluate("--judge-model", "independent-judge", "--judge-base-url",
                                           "http://127.0.0.1:4000/v1", "--allow-external-execution"), 0)
            self.assertEqual(run.call_count, 4)
        grades = read(self.out / "grades.provisional.json")
        before = read(self.out / "report.json")
        self.assertEqual(before["grade_sources"]["automated_provisional"], 2)
        write(self.out / "grades.json", [{**grades[0], "verification": 2, "notes": "Human review"}])
        after = generate(self.out)
        self.assertEqual(after["grade_sources"], {"human": 1, "automated_provisional": 1})
        self.assertEqual(abs(after["comparisons"]["skill"]["mean_paired_delta_out_of_8"]), 1)
        self.assertEqual(read(self.out / "grades.provisional.json"), grades)

    def test_invalid_grade_is_never_a_zero_or_a_success(self):
        with self.assertRaises(ValueError):
            parse_grade(json.dumps({**GRADE, "true_positives": ["made-up"]}), "run-1", [])
        def simulate(agent, *_):
            return result(response="not JSON") if agent.model == "independent-judge" else result()
        with patch.object(Agent, "run", autospec=True, side_effect=simulate):
            self.assertEqual(self.evaluate("--judge-model", "independent-judge", "--judge-base-url",
                                           "http://127.0.0.1:4000/v1", "--allow-external-execution"), 1)
        report = read(self.out / "report.json")
        self.assertEqual(report["grade_sources"]["automated_provisional"], 0)
        self.assertEqual(report["unresolved_grading_errors"], 2)
        self.assertEqual(report["comparisons"]["skill"]["incomplete_pairs"], 1)

    def test_legacy_reporting_accepts_ungraded_runs(self):
        benchmark.prepare(self.out, read(ROOT / "evals/cases.json"), ["outbox-crash"],
                          1, 42, "fixture", "fixture", "legacy adapter protocol")
        self.assertEqual(generate(self.out)["conditions"]["skill"]["attempted"], 0)
        with self.assertRaisesRegex(ValueError, "Grades file .* is missing"):
            generate(self.out, self.root / "missing.json")
        with self.assertRaisesRegex(ValueError, "Adapter script was not found"):
            benchmark.execute(self.out, [sys.executable, str(self.root / "missing.py")])

    def test_report_counts_provider_output_limits(self):
        clipped = {**result(), "output_limit_reached": True}
        with patch.object(Agent, "run", side_effect=[clipped, result()]):
            self.assertEqual(self.evaluate(), 0)
        report = read(self.out / "report.json")
        self.assertEqual(sum(item["output_limits_reached"] for item in report["conditions"].values()), 1)
        self.assertIn("Output limits reached", (self.out / "report.md").read_text(encoding="utf-8"))

    def test_lock_rejects_concurrent_writer_and_releases(self):
        self.out.mkdir()
        with run_lock(self.out), self.assertRaisesRegex(ValueError, "Another benchmark"):
            with run_lock(self.out):
                self.fail("Concurrent lock acquired")
        with run_lock(self.out):
            pass

    def test_compare_requires_matched_design(self):
        self.assertEqual(self.evaluate(), 0)
        second, third = self.root / "second", self.root / "third"
        self.assertEqual(cli("evaluate", second, "--agent", "mock", "--cases", "local-transaction"), 0)
        self.assertIsNone(cli("compare", self.root / "matched", self.out, second))
        summary = read(self.root / "matched/comparison.json")
        self.assertTrue(summary["design"]["synthetic"])
        self.assertEqual(len(summary["results"]), 2)
        self.assertIsNone(summary["results"][0]["mean_paired_delta_out_of_8"])
        self.assertEqual(cli("evaluate", third, "--agent", "mock", "--cases", "cache-race"), 0)
        with self.assertRaises(SystemExit) as error:
            cli("compare", self.root / "mismatched", self.out, third)
        self.assertEqual(error.exception.code, 2)
        self.assertFalse((self.root / "mismatched").exists())


class AdapterTests(unittest.TestCase):
    def test_outdated_cli_is_rejected_before_authentication(self):
        with (patch.object(Agent, "executable", return_value="codex"),
              patch("benchmark_adapters.cli_run", side_effect=[
                  (0, b"codex 0.0.1", b""), (0, b"--help", b""),
              ]) as run,
              self.assertRaisesRegex(AdapterError, "Update codex")):
            Agent("codex", "fixture").doctor()
        self.assertEqual(run.call_count, 2)

    def test_codex_jsonl_final_message_and_usage(self):
        events = [
            {"type": "item.completed", "item": {"type": "agent_message", "text": "preamble"}},
            {"type": "item.completed", "item": {"type": "agent_message", "text": "review"}},
            {"type": "turn.completed", "usage": {"input_tokens": 40, "output_tokens": 9,
                                                 "cached_input_tokens": 30}},
        ]
        value = cli_result("codex", "\n".join(map(json.dumps, events)).encode())
        self.assertEqual(value["response"], "review")
        self.assertEqual(value["usage"]["cached_input_tokens"], 30)

    def test_claude_cost_and_input_token_accounting(self):
        raw = json.dumps({"subtype": "success", "result": "review", "total_cost_usd": 0.012,
                          "usage": {"input_tokens": 5, "cache_creation_input_tokens": 1,
                                    "cache_read_input_tokens": 10, "output_tokens": 4}}).encode()
        value = cli_result("claude-code", raw)
        self.assertEqual(value["usage"], {"input_tokens": 16, "output_tokens": 4,
                                         "cached_input_tokens": 10})
        self.assertEqual(value["cost_usd"], 0.012)

    def test_copilot_filters_tool_messages_and_uses_confirmed_counts(self):
        events = [
            {"type": "assistant.message", "data": {"content": "intermediate", "toolRequests": [{}]}},
            {"type": "assistant.message", "data": {"content": "review"}},
            {"type": "assistant.usage", "data": {"inputTokens": 32, "outputTokens": 7}},
        ]
        value = cli_result("copilot", "\n".join(map(json.dumps, events)).encode())
        self.assertEqual(value["response"], "review")
        self.assertEqual(value["usage"], {"input_tokens": 32, "output_tokens": 7})

    def test_http_compatibility_usage_cost_and_auth_failure(self):
        requests = []
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_POST(self):
                auth = self.headers.get("Authorization")
                data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                requests.append((self.path, data))
                if auth != "Bearer synthetic-test-key":
                    self.send_error(401)
                    return
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("x-litellm-response-cost", "0.000125")
                self.end_headers()
                self.wfile.write(json.dumps({"model": "fixture", "choices": [
                    {"message": {"content": "ready"}, "finish_reason": "length"}],
                                             "usage": {"prompt_tokens": 10, "completion_tokens": 1,
                                                       "prompt_tokens_details": {"cached_tokens": 4}}}).encode())

        with HTTPServer(("127.0.0.1", 0), Handler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                endpoint = f"http://127.0.0.1:{server.server_port}/v1"
                with patch.dict(os.environ, {"BENCH_TEST_KEY": "synthetic-test-key", "NO_PROXY": "127.0.0.1"}):
                    agent = Agent("openai-compatible", "fixture", endpoint, "BENCH_TEST_KEY")
                    value = agent.run("synthetic request", ROOT, 2)
                    self.assertEqual(value["status"], "ok", value)
                    self.assertEqual(value["usage"]["cached_input_tokens"], 4)
                    self.assertEqual(value["cost_usd"], 0.000125)
                    self.assertTrue(value["output_limit_reached"])
                    self.assertNotIn("synthetic-test-key", json.dumps(value))
                    denied = Agent("openai-compatible", "fixture", endpoint).run("test auth", ROOT, 2)
                    self.assertEqual(denied["status"], "auth_error")
            finally:
                server.shutdown()
                thread.join(timeout=2)
        self.assertEqual(requests[0][0], "/v1/chat/completions")
        self.assertEqual(requests[0][1]["messages"], [{"role": "user", "content": "synthetic request"}])


if __name__ == "__main__":
    unittest.main()

# Technology discovery

Start with task-relevant components. Inspect manifests, resolved lockfiles, imports and call sites, deployment descriptors, migrations and sanitized configuration metadata. For polyglot repositories, keep component-specific records; a dependency in one service does not imply use in another.

1. Establish repository scope, runtime, dependencies, datastore, messaging, caches, external services, execution topology and ownership.
2. Record declared versions separately from resolved versions and deployed versions. A floating tag, version range or lockfile is not evidence of the running deployment. Record source paths and conflicting observations.
3. Trace actual use: client configuration, transaction enlistment, acknowledgment timing, routing, retry layers, worker topology and effective feature flags. Avoid reading credentials or production data; ask for sanitized configuration evidence if necessary.
4. Map each relevant component to one or more capability domains, including custom or unlisted ones. Load only relevant references and optional profiles. Follow [capability mapping](CAPABILITY-MAPPING.md) and [version verification](VERSION-VERIFICATION.md).
5. Record gaps using the [inventory template](../../assets/technology-inventory.md). For an unknown product follow [unknown technology](UNKNOWN-TECHNOLOGY.md).

The optional repository tool `tools/discover.py` inventories allowlisted manifest signals without executing project code, installing dependencies, or accessing the network. It is not shipped as an agent runtime requirement. Its output is a starting point, never proof of deployed versions or capabilities. Inspect additional sources manually when relevant. Do not send repository data to external documentation services.

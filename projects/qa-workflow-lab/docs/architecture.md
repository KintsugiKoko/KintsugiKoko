# Architecture and Tool Contracts

## Execution Path

```text
Versioned fictional bundle
  -> identity and shape validation
  -> one bounded agent policy
  -> allowed retrieval and workflow tools
  -> deterministic calculations and local harness assertions
  -> source-linked artifact and full trace
  -> receiving-owner review recorded against the run hash
```

Each of the eight roles has one mission and one specialized analysis operation. All roles can list the supplied evidence catalog, retrieve a record by ID, and search up to 20 records with a literal phrase. A role cannot call another role's specialized tool. The coordinator reads a task register; it does not recursively spawn agents.

## Tool Surface

| Operation | Input | Result | Boundary |
| --- | --- | --- | --- |
| `catalog` | None | Record ID, kind, build, platform | Supplied bundle only |
| `read_evidence` | Exact record ID | Full record | No arbitrary paths or URLs |
| `search_evidence` | Literal phrase | At most 20 matching records | Local, bounded search |
| Role-specific analysis | Current bundle | Findings and work product | Fixed Python operation |
| `finish` | Proposed notes with retrieved record IDs | Review-required artifact | Cannot override computed results |

Stable validation remains code. The optional model chooses which evidence to inspect and can propose hypotheses or next actions. Its suggestions are stored separately from tool observations. A valid citation proves retrieval, not semantic correctness; QA still reviews the claim.

## Evidence Contract

Every input has a feature, candidate/baseline build, supported platforms, rule version, owner and explicit fictional-data flag. Sample metadata additionally records client/server identities, configuration and source revision. Records carry stable IDs and build/platform context.

Every output retains the input hash, execution mode, model identifier, prompt/tool version, configured budgets, tool inputs/results, stopping reason, source IDs and pending review state. The output manifest records creation time and hashes. File and run hashes detect changes; they are not digital signatures.

## Independent Oracles

`ArenaState` implements a small fictional game state. `CHECKS` contains fixed expected values and separate rule statements. The regression tool exercises state transitions through the same entry points in valid and fault-injected variants. Generated candidate tests assert literal expected values. Each run starts with a fresh state.

The demonstrated rules are single result commit, obsolete equip rejection, single upgrade mutation, encounter targeting, current-state recovery and old-entity cleanup. These executable checks establish behavior only in this reference model.

## Query Contract

Telemetry rows are loaded into an in-memory SQLite table. One parameterized query filters by build, platform, configuration, metric, eligibility and time window. Stable event IDs deduplicate delivery; conflicting duplicate contents block the result. Supplied aggregate counts must match calculated counts before a trend comparison is allowed. Schema, sampling and window mismatches remain blocked.

## State and Recovery

Artifact states follow queued, running, review required, then a separate accepted/rejected review record. Blocked runs preserve successful tool results and the stopping reason. Model calls have no retry; reruns use new output directories. No tool can publish an issue, send feedback, modify a game project or authorize a release.

Changing source records changes the input hash. A review is bound to a specific run hash, so an old acceptance does not apply to edited evidence. The browser reads saved runs and does not write approval records.

## Code Map

| Module | Responsibility |
| --- | --- |
| `models.py` | Evidence shape, result contracts, hashing |
| `agents.py` | Role missions, tool permissions, action loop and stop rules |
| `analysis.py` | Eight deterministic QA operations |
| `harness.py` | Executable reference model and independent assertions |
| `queries.py` | Bounded, parameterized exposure query |
| `provider.py` | Explicit OpenAI structured-action adapter |
| `reports.py` | Markdown, JSON, manifest and HTML |
| `evaluation.py` | Labels held outside agent inputs |
| `fixtures.py` | Fictional scenario generation |
| `cli.py` | Run, review, evaluate, showcase and ZIP export |

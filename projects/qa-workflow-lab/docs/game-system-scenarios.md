# Game-System Scenario Design

Relay Arena is a fictional test model for shared gameplay state. The executable scope is intentionally small so each assertion and failure can be inspected. The broader matrix below documents how the same QA reasoning would extend through a team's supported game harness.

## Feature and State Model

Players belong to teams and encounters. A loadout and an upgrade have an originating epoch. An accepted upgrade adds five to a base power of ten once per transaction. A settled result increments score once. Recovery may restore current state, and cleanup retains only entities from the active epoch.

These are authored demo rules. They do not describe an existing commercial game's architecture or balance.

| Boundary | Risk | Controlled action | Independent oracle | Current evidence |
| --- | --- | --- | --- | --- |
| Result to score | Duplicate score mutation | Deliver the same result twice | Score equals 1 | Executable `single_result` check |
| Equip to round reset | Obsolete completion replaces current item | Complete an epoch-1 equip during epoch 2 | Item remains carbine | Executable `stale_equip` check |
| Upgrade retry | Modifier applies twice | Retry one transaction | Power equals 15; a distinct valid transaction can reach 20 | Executable `single_upgrade` check and unit test |
| Team to encounter | Cross-encounter damage eligibility | Evaluate different teams in different arenas | Target is ineligible | Executable `encounter_target` check |
| Reconnect to state | Old loadout returns | Restore an old snapshot | Current item remains carbine | Executable `current_recovery` check |
| Encounter to cleanup | Old entities affect the next encounter | Teardown old epoch | Only one current entity remains | Executable `cleanup` check |

## Broader Coverage Matrix

These scenarios are design artifacts for future integration, not executed engine results.

| Scenario | Setup and observation | Evidence and likely owner | Expected decision |
| --- | --- | --- | --- |
| Selection validity | Current offer, obsolete epoch, excluded item, deadline boundary | Offer/request IDs and rejection reason; Design and Gameplay Engineering | Only an approved current selection mutates the build |
| Modifier composition | Base ability plus eligible upgrade and modifier in each permitted order | Effective parameters, cast output, versions; Gameplay Engineering | Match the approved composition and lifetime rule |
| Eight-team identity | All team IDs across configured encounter membership | Roster, target sets, ownership and permitted client views; Systems QA | No aliasing or cross-encounter eligibility |
| Objective setup | Enabled position, normal route, interaction and timer start | Position, collision/access capture, interaction state; Level Design and QA | Objective is reachable and usable under the approved rule |
| Terminal precedence | Defeat, objective completion and timeout at adjacent ticks | Server ticks, decision rule and result ledger; Gameplay Engineering | One approved outcome regardless of duplicate delivery |
| Complete-match progression | Legal participants, transitions, eliminated teams and final result | Lifecycle events and final ledger; Feature QA | No illegal reentry, double result or hang |
| Interruption | Death, disconnect, cancellation and stale callbacks | Request/epoch IDs and before/after states; Systems QA | Each independent lifecycle dimension follows its rule |
| Shared-mode isolation | Finish one configuration and enter another | Entity counts, timers, overrides and current mode; Gameplay Engineering | Only explicitly persistent state remains |
| Performance smoke | Matched platform and build, full configured workload | Frame/tick distributions, entity counts and memory; Performance | Compare against owner-approved budgets and exposure |
| Readability playtest | Conflicting effects, transitions and actionable cues | Timestamped player observations and captures; Design and QA | Human review establishes clarity and tactical impact |

## Testability Handoff

Before porting a scenario, agree the rule version, real gameplay entry point, deterministic setup control, assertion accessor, timing basis, deadline, cleanup and artifact paths. A Blueprint or C++ functional test should drive the actual production path. Keep the expected value independently specified. A setup failure or timeout blocks coverage; a passing retry retains the original failed run.

For client/server comparisons, confirm permitted information and aligned updates before comparing state. Do not use arbitrary raw equality as the oracle. Performance and balance require their own measurement and playtest evidence.

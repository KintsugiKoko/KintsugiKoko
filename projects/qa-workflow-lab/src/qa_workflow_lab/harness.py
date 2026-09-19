"""Executable fictional rules. Oracles are literals outside the implementation."""

from dataclasses import dataclass, field


@dataclass
class ArenaState:
    epoch: int = 2
    score: int = 0
    item: str = "carbine"
    power: int = 10
    committed: set[str] = field(default_factory=set)
    entities: list[dict] = field(default_factory=lambda: [{"epoch": 1}, {"epoch": 2}])

    def settle(self, event, *, faulty=False):
        if event not in self.committed or faulty:
            self.score += 1
            self.committed.add(event)

    def complete_equip(self, epoch, item, *, faulty=False):
        if epoch == self.epoch or faulty:
            self.item = item

    def upgrade(self, transaction, *, faulty=False):
        if transaction not in self.committed or faulty:
            self.power += 5
            self.committed.add(transaction)

    def target_allowed(self, source_team, target_team, source_arena, target_arena, *, faulty=False):
        return source_team != target_team and (faulty or source_arena == target_arena)

    def restore(self, snapshot, *, faulty=False):
        if snapshot["epoch"] == self.epoch or faulty:
            self.item = snapshot["item"]

    def cleanup(self, *, faulty=False):
        if not faulty:
            self.entities = [e for e in self.entities if e["epoch"] == self.epoch]


CHECKS = {
    "single_result": (1, "One score mutation for duplicate result delivery."),
    "stale_equip": ("carbine", "An obsolete completion cannot replace the current loadout."),
    "single_upgrade": (15, "One accepted upgrade changes power once."),
    "encounter_target": (False, "A target in another encounter is ineligible."),
    "current_recovery": ("carbine", "Recovery rejects an obsolete snapshot."),
    "cleanup": (1, "Only current-encounter entities remain after cleanup."),
}


def run_check(check, *, faulty=False):
    if check not in CHECKS:
        raise ValueError(f"Unsupported local harness check: {check}")
    state = ArenaState()
    if check == "single_result":
        state.settle("result-7", faulty=faulty)
        state.settle("result-7", faulty=faulty)
        actual = state.score
    elif check == "stale_equip":
        state.complete_equip(1, "old-tool", faulty=faulty)
        actual = state.item
    elif check == "single_upgrade":
        state.upgrade("txn-7", faulty=faulty)
        state.upgrade("txn-7", faulty=faulty)
        actual = state.power
    elif check == "encounter_target":
        actual = state.target_allowed(1, 7, "north", "south", faulty=faulty)
    elif check == "current_recovery":
        state.restore({"epoch": 1, "item": "old-tool"}, faulty=faulty)
        actual = state.item
    else:
        state.cleanup(faulty=faulty)
        actual = len(state.entities)
    expected, oracle = CHECKS[check]
    return {"check": check, "variant": "fault_injected" if faulty else "valid", "expected": expected,
            "actual": actual, "passed": type(actual) is type(expected) and actual == expected, "oracle": oracle,
            "execution_scope": "local Python reference model"}


def candidate_source(checks):
    """Emit a reviewable fixed template; model text is never executed as code."""
    lines = ["from qa_workflow_lab.harness import run_check", ""]
    for check in checks:
        expected = CHECKS[check][0]
        lines.extend([f"def test_{check}():", f"    result = run_check({check!r})",
                      f"    assert result['actual'] == {expected!r}", ""])
    return "\n".join(lines)

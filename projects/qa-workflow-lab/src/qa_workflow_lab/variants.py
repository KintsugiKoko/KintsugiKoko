"""Small fictional handoff variants; expected outcomes live in tests, not inputs."""

from copy import deepcopy

from .fixtures import sample_bundle
from .models import InputError


# Each variant starts from the same valid diamond: 1 -> (2, 3) -> 4.
VARIANTS = {
    "parallel-valid": {},
    "parallel-missing-ack": {"TASK-2": {"receiving_acknowledgement": False}},
    "independent-blocker": {"TASK-2": {"capacity": 0}, "TASK-4": {"dependencies": ["TASK-3"]}},
    "duplicate-work-key": {"TASK-2": {"work_key": "shared-investigation"},
                           "TASK-3": {"work_key": "shared-investigation"}},
    "blank-owner": {"TASK-1": {"owner": "   "}},
    "dependency-cycle": {"TASK-1": {"dependencies": ["TASK-4"]}},
    "missing-prerequisite": {"TASK-3": {"dependencies": ["TASK-99"]}},
}


def variant_bundle(name):
    if name not in VARIANTS:
        raise InputError("Unknown coordination variant.")
    bundle = sample_bundle("corrected-model")
    bundle.metadata.update(case=name, source_revision="coordination-variants-1")
    bundle.get("TASK-2")["data"]["dependencies"] = ["TASK-1"]
    bundle.get("TASK-3")["data"]["dependencies"] = ["TASK-1"]
    bundle.get("TASK-4")["data"]["dependencies"] = ["TASK-2", "TASK-3"]
    for task_id, fields in VARIANTS[name].items():
        bundle.get(task_id)["data"].update(deepcopy(fields))
    return bundle

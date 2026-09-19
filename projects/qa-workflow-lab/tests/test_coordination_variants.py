"""Graph topology, independence and valid controls for the handoff review."""

from itertools import permutations
import json

import pytest

from qa_workflow_lab.agents import run_agent
from qa_workflow_lab.cli import main
from qa_workflow_lab.models import InputError
from qa_workflow_lab.variants import VARIANTS, variant_bundle


EXPECTED = {
    "parallel-valid": {"TASK-1": [], "TASK-2": [], "TASK-3": [], "TASK-4": []},
    "parallel-missing-ack": {"TASK-1": [], "TASK-2": ["receiving acknowledgement and evidence"],
                             "TASK-3": [], "TASK-4": ["TASK-2"]},
    "independent-blocker": {"TASK-1": [], "TASK-2": ["owner capacity"], "TASK-3": [], "TASK-4": []},
    "duplicate-work-key": {"TASK-1": [], "TASK-2": ["duplicate work key"],
                           "TASK-3": ["duplicate work key"], "TASK-4": ["TASK-2", "TASK-3"]},
    "blank-owner": {"TASK-1": ["receiving owner"], "TASK-2": ["TASK-1"],
                     "TASK-3": ["TASK-1"], "TASK-4": ["TASK-2", "TASK-3"]},
}


def blockers(result):
    return {row["source"]: sorted(row["blockers"]) for row in result.details["task_register"]}


@pytest.mark.parametrize("name", EXPECTED)
def test_variant_has_exact_local_and_downstream_blockers(name):
    bundle = variant_bundle(name)
    before = bundle.fingerprint
    result = run_agent(bundle, "AI8")
    assert result.status == "review_required"
    assert result.review_status == "pending"
    assert blockers(result) == EXPECTED[name]
    assert bundle.fingerprint == before


@pytest.mark.parametrize("name", EXPECTED)
def test_all_24_task_orderings_preserve_the_same_decisions(name):
    bundle = variant_bundle(name)
    tasks = bundle.select("task")
    evidence = [row for row in bundle.records if row["kind"] != "task"]
    for ordering in permutations(tasks):
        bundle.records = [*evidence, *ordering]
        assert blockers(run_agent(bundle, "AI8")) == EXPECTED[name]


@pytest.mark.parametrize("name,message", [("dependency-cycle", "cycle"),
                                           ("missing-prerequisite", "missing from the register")])
def test_invalid_graph_stops_without_available_task_claims(name, message):
    result = run_agent(variant_bundle(name), "AI8")
    assert result.status == "blocked" and result.product_verdict == "unverified"
    assert "task_register" not in result.details
    assert message in result.trace[-1]["output"]["error"]


def test_repaired_acknowledgement_clears_only_the_derived_blockers():
    bundle = variant_bundle("parallel-missing-ack")
    original = run_agent(bundle, "AI8")
    bundle.get("TASK-2")["data"]["receiving_acknowledgement"] = True
    repaired = run_agent(bundle, "AI8")
    assert blockers(original) == EXPECTED["parallel-missing-ack"]
    assert blockers(repaired) == EXPECTED["parallel-valid"]
    assert repaired.details["execution"]["input_sha256"] != original.details["execution"]["input_sha256"]
    assert all(row["state"] == "accepted" for row in repaired.details["task_register"][:3])


def test_variant_inputs_are_isolated_between_runs():
    first = variant_bundle("parallel-valid")
    first.get("TASK-4")["data"]["dependencies"].clear()
    assert variant_bundle("parallel-valid").get("TASK-4")["data"]["dependencies"] == ["TASK-2", "TASK-3"]
    with pytest.raises(InputError, match="Unknown"):
        variant_bundle("not-a-variant")


@pytest.mark.parametrize("value", [None, "", " ", 17])
def test_invalid_owner_never_makes_downstream_work_available(value):
    bundle = variant_bundle("parallel-valid")
    bundle.get("TASK-1")["data"]["owner"] = value
    assert blockers(run_agent(bundle, "AI8")) == EXPECTED["blank-owner"]


@pytest.mark.parametrize("value", [True, None, "1", -1, 0.5, float("nan"), float("inf")],
                         ids=["boolean", "null", "text", "negative", "fractional", "nan", "infinity"])
def test_capacity_must_be_a_nonnegative_integer_slot_count(value):
    bundle = variant_bundle("parallel-valid")
    bundle.get("TASK-2")["data"]["capacity"] = value
    result = run_agent(bundle, "AI8")
    assert result.status == "blocked" and result.product_verdict == "unverified"
    assert "capacity" in result.trace[-1]["output"]["error"].lower()


@pytest.mark.parametrize("dependencies", ["TASK-1", None, [""], [None], ["TASK-1", "TASK-1"]])
def test_dependency_list_contract_is_explicit(dependencies):
    bundle = variant_bundle("parallel-valid")
    bundle.get("TASK-2")["data"]["dependencies"] = dependencies
    result = run_agent(bundle, "AI8")
    assert result.status == "blocked"
    assert "dependenc" in result.trace[-1]["output"]["error"].lower()


def test_duplicate_work_resolution_restores_valid_parallel_control():
    bundle = variant_bundle("duplicate-work-key")
    assert blockers(run_agent(bundle, "AI8")) == EXPECTED["duplicate-work-key"]
    bundle.get("TASK-3")["data"]["work_key"] = "separate-regression-work"
    assert blockers(run_agent(bundle, "AI8")) == EXPECTED["parallel-valid"]


@pytest.mark.parametrize("name", VARIANTS)
def test_each_variant_cli_writes_inspectable_evidence(tmp_path, name):
    output = tmp_path / name
    expected_exit = 2 if name in ("dependency-cycle", "missing-prerequisite") else 0
    assert main(["demo", "--variant", name, "--output", str(output)]) == expected_exit
    run = json.loads((output / "run.json").read_text(encoding="utf-8"))
    assert run["metadata"]["case"] == name and run["metadata"]["fictional"] is True
    result = run["workflows"][7]
    assert result["workflow"] == "AI8"
    if name in EXPECTED:
        assert {row["source"]: sorted(row["blockers"]) for row in result["details"]["task_register"]} == EXPECTED[name]
    else:
        assert result["product_verdict"] == "unverified"
    assert (output / "index.html").exists() and (output / "manifest.json").exists()


def test_cli_rejects_ambiguous_case_and_variant_selection(tmp_path):
    with pytest.raises(SystemExit) as error:
        main(["demo", "--case", "candidate", "--variant", "parallel-valid", "--output", str(tmp_path / "unused")])
    assert error.value.code == 2
    assert not (tmp_path / "unused").exists()


@pytest.mark.parametrize("value", ["", "   ", 7, ["task"]])
def test_invalid_work_key_has_an_explicit_contract_error(value):
    bundle = variant_bundle("parallel-valid")
    bundle.get("TASK-2")["data"]["work_key"] = value
    result = run_agent(bundle, "AI8")
    assert result.status == "blocked"
    assert "work_key" in result.trace[-1]["output"]["error"]


def test_work_key_whitespace_does_not_hide_duplicate_assignment():
    bundle = variant_bundle("duplicate-work-key")
    bundle.get("TASK-2")["data"]["work_key"] = " shared-investigation "
    assert blockers(run_agent(bundle, "AI8")) == EXPECTED["duplicate-work-key"]


def test_variant_showcase_contains_all_cases_and_preserves_ordinary_showcase(tmp_path):
    variants = tmp_path / "variants.html"
    ordinary = tmp_path / "ordinary.html"
    assert main(["showcase", "--variants", "--output", str(variants)]) == 0
    assert main(["showcase", "--output", str(ordinary)]) == 0
    from html.parser import HTMLParser

    class RunData(HTMLParser):
        def __init__(self):
            super().__init__()
            self.active = False
            self.text = ""

        def handle_starttag(self, tag, attrs):
            self.active = tag == "script" and dict(attrs).get("id") == "run-data"

        def handle_endtag(self, tag):
            if tag == "script":
                self.active = False

        def handle_data(self, data):
            if self.active:
                self.text += data

    parsed = RunData()
    parsed.feed(variants.read_text(encoding="utf-8"))
    entries = json.loads(parsed.text)
    assert [entry["run"]["metadata"]["case"] for entry in entries] == list(VARIANTS)
    assert all(len(entry["run"]["workflows"]) == 8 for entry in entries)
    parsed = RunData()
    parsed.feed(ordinary.read_text(encoding="utf-8"))
    assert [entry["run"]["metadata"]["case"] for entry in json.loads(parsed.text)] == ["candidate", "evidence-gaps", "corrected-model"]

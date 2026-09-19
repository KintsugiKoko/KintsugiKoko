import hashlib
import json
from pathlib import Path
import posixpath
import re
import zipfile
import pytest
from qa_workflow_lab.agents import run_all
from qa_workflow_lab.cli import main, package_project, project_root
from qa_workflow_lab.evaluation import evaluate
from qa_workflow_lab.fixtures import sample_bundle, sample_data
from qa_workflow_lab.models import InputError
from qa_workflow_lab.reports import render_showcase, write_run


def test_reports_have_real_assertions_queries_and_hashes(tmp_path):
    run = run_all(sample_bundle())
    out = tmp_path / "run"
    manifest = write_run(run, out, template=project_root() / "web/review.html")
    assert (out / "test_regression_candidate.py").exists()
    assert "Power reaches 20" in (out / "defect-proposals.md").read_text()
    assert "trace evidence" in (out / "remote-assignment.md").read_text()
    for name, expected_hash in manifest["files"].items():
        assert hashlib.sha256((out / name).read_bytes()).hexdigest() == expected_hash
        assert b"\r\n" not in (out / name).read_bytes()
    assert json.loads((out / "run.json").read_text())["workflows"][4]["details"]["queries"]
    with pytest.raises(InputError, match="already exists"):
        write_run(run, out)


def test_script_like_evidence_is_escaped_in_html():
    bundle = sample_bundle()
    bundle.get("SUBART-1-state")["data"]["content"] = '</script><script>alert("private")</script>'
    page = render_showcase([run_all(bundle)], project_root() / "web/review.html")
    assert '</script><script>alert("private")' not in page
    assert "\\u003c/script\\u003e" in page
    assert "textContent" in page


def test_no_em_dash_in_generated_artifacts(tmp_path):
    out = tmp_path / "run"
    write_run(run_all(sample_bundle()), out, template=project_root() / "web/review.html")
    assert all(chr(0x2014) not in p.read_text(encoding="utf-8") for p in out.iterdir())


def test_cli_complete_flow_and_nonzero_blocked_result(tmp_path):
    assert main(["demo", "--output", str(tmp_path / "candidate")]) == 0
    assert main(["demo", "--case", "evidence-gaps", "--output", str(tmp_path / "gaps")]) == 2
    assert main(["demo", "--case", "corrected-model", "--output", str(tmp_path / "corrected")]) == 0
    assert main(["review", "--run", str(tmp_path / "candidate/run.json"), "--workflow", "AI6",
                 "--reviewer", "Test Reviewer", "--decision", "accepted", "--note", "Test artifact acknowledgement"]) == 0
    review = json.loads((tmp_path / "candidate/reviews.jsonl").read_text())
    assert review["reviewer"] == "Test Reviewer"


@pytest.mark.parametrize("workflow", ["AI1", "AI2", "AI3", "AI4", "AI5", "AI6", "AI7", "AI8"])
def test_single_workflow_cli(tmp_path, workflow):
    path = tmp_path / "input.json"
    path.write_text(json.dumps(sample_data()))
    assert main(["run", "--input", str(path), "--workflow", workflow, "--output", str(tmp_path / workflow)]) == 0


def test_evaluation_cases_pass_without_labels_in_inputs():
    result = evaluate(project_root() / "tests/evaluation-cases.json")
    assert result["case_count"] == 12
    assert result["failed"] == 0
    assert "human" in result["scope"].lower()


def test_package_uses_explicit_file_allowlist(tmp_path):
    # The exporter includes source and review artifacts, never arbitrary repo files.
    archive = tmp_path / "showcase.zip"
    package_project(project_root(), archive)
    with zipfile.ZipFile(archive) as zipped:
        names = zipped.namelist()
        assert "qa-workflow-lab/reports/sample/index.html" in names
        assert "qa-workflow-lab/tests/evaluation-cases.json" in names
        assert not any(".env" in n or "__pycache__" in n or "career-materials" in n for n in names)


def test_package_has_self_contained_showcase_and_markdown_links(tmp_path):
    archive = tmp_path / "portable.zip"
    package_project(project_root(), archive)
    with zipfile.ZipFile(archive) as zipped:
        names = set(zipped.namelist())
        assert "qa-workflow-lab/Showcase.html" in names
        page = zipped.read("qa-workflow-lab/Showcase.html").decode("utf-8")
        for case in ("candidate", "evidence-gaps", "corrected-model"):
            assert case in page
        for name in names:
            if not name.endswith(".md"):
                continue
            for link in re.findall(r"\]\(([^)]+)\)", zipped.read(name).decode("utf-8")):
                if link.startswith(("https://", "http://", "#")):
                    continue
                target = posixpath.normpath(posixpath.join(posixpath.dirname(name), link.split("#")[0]))
                assert target in names, (name, link)

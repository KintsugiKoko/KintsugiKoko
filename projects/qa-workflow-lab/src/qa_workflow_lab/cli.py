"""Local entry points. Only explicitly selected model mode can use the network."""

import argparse
import json
from pathlib import Path
import tempfile
import zipfile
from .agents import TITLES, run_agent, run_all, review_record
from .fixtures import CASES, sample_bundle, sample_data
from .models import Bundle, InputError
from .reports import render_showcase, write_run
from .variants import VARIANTS, variant_bundle


def project_root():
    return Path(__file__).resolve().parents[2]


def package_project(root, output):
    output = Path(output)
    if output.exists():
        raise InputError("Package already exists. Choose a new path.")
    files = [root / "README.md", root / "pyproject.toml"]
    for directory in ("src", "tests", "sample-data", "docs", "web"):
        files += [p for p in (root / directory).rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix in (".py", ".md", ".json", ".html", ".cjs")]
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        run = run_all(sample_bundle())
        generated = Path(temporary) / "review"
        write_run(run, generated, template=root / "web" / "review.html")
        from .harness_evaluation import evaluate as evaluate_harnesses, write_results
        harness_report = Path(temporary) / "harnesses"
        write_results(evaluate_harnesses(root, mode="replay"), harness_report)
        with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(files):
                name = "qa-workflow-lab/" + path.relative_to(root).as_posix()
                if path == root / "README.md":
                    readme = path.read_text(encoding="utf-8").replace("../../docs/qa-workflow-lab.html", "Showcase.html")
                    archive.writestr(name, readme)
                else:
                    archive.write(path, name)
            archive.writestr("qa-workflow-lab/Showcase.html", render_showcase(
                [run_all(sample_bundle(case)) for case in CASES], root / "web" / "review.html"))
            for path in sorted(generated.iterdir()):
                archive.write(path, "qa-workflow-lab/reports/sample/" + path.name)
            for path in sorted(harness_report.iterdir()):
                archive.write(path, "qa-workflow-lab/reports/jev-harnesses/" + path.name)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run bounded QA workflows over local fictional evidence.")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="Evaluate an evidence bundle and preserve a review packet.")
    run.add_argument("--input", type=Path, required=True)
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--workflow", choices=["all", *TITLES], default="all")
    run.add_argument("--mode", choices=["offline", "model"], default="offline")
    run.add_argument("--allow-network", action="store_true", help="Explicitly permit model requests using the selected fictional evidence.")
    run.add_argument("--model", help="API model ID. Otherwise use OPENAI_MODEL.")
    demo = commands.add_parser("demo", help="Run a bundled fictional case without a network connection.")
    scenario = demo.add_mutually_exclusive_group()
    scenario.add_argument("--case", choices=CASES, default="candidate")
    scenario.add_argument("--variant", choices=list(VARIANTS), help="Run a focused coordination variant from the valid reference scenario.")
    demo.add_argument("--output", type=Path, required=True)
    fixtures = commands.add_parser("fixtures", help="Write reproducible fictional sample inputs.")
    fixtures.add_argument("--output", type=Path, required=True)
    showcase = commands.add_parser("showcase", help="Build a standalone review page from bundled offline cases.")
    showcase.add_argument("--output", type=Path, required=True)
    showcase.add_argument("--variants", action="store_true", help="Show the seven focused coordination variants instead of the three main cases.")
    package = commands.add_parser("package", help="Export source, tests, documentation and a sample run as a ZIP.")
    package.add_argument("--output", type=Path, required=True)
    evaluation = commands.add_parser("evaluate", help="Run labeled contract cases kept separate from demo inputs.")
    evaluation.add_argument("--cases", type=Path, default=project_root() / "tests" / "evaluation-cases.json")
    evaluation.add_argument("--output", type=Path, required=True)
    routing = commands.add_parser("route-evaluate", help="Compare QA intake suggestions against authored fictional labels; no workflow dispatch.")
    routing.add_argument("--mode", choices=["baseline", "replay", "jev"], default="baseline")
    routing.add_argument("--output", type=Path, required=True)
    routing.add_argument("--threshold", type=float, default=0.8, help="Illustrative confidence floor, not calibrated accuracy.")
    routing.add_argument("--allow-network", action="store_true", help="Permit sending the fictional routing reports to TypeSafe; API usage may cost money.")
    routing.add_argument("--dry-run", action="store_true", help="Preview Jev request bodies without reading credentials or making requests.")
    routing.add_argument("--model", default="jev-latest")
    routing.add_argument("--max-calls", type=int, default=20, help="Maximum request attempts, 1 to 20. No retry; stop on first provider failure.")
    harness = commands.add_parser("harness-evaluate", help="Run bounded investigation, intake and release-evidence harnesses.")
    harness.add_argument("--harness", choices=["all", "investigation", "intake", "release"], default="all")
    harness.add_argument("--case", help="Select one bundled fictional case, such as H01.")
    harness.add_argument("--mode", choices=["baseline", "replay", "jev"], default="baseline")
    harness.add_argument("--output", type=Path, required=True)
    harness.add_argument("--allow-network", action="store_true", help="Explicitly allow paid TypeSafe requests for selected fictional cases.")
    harness.add_argument("--dry-run", action="store_true", help="Preview Jev requests without credentials or network access.")
    harness.add_argument("--model", default="jev-latest")
    harness.add_argument("--max-calls", type=int, default=3, help="Jev request-attempt cap, 1 to 20. Default 3; no automatic retry.")
    review = commands.add_parser("review", help="Append a human artifact decision bound to the immutable run hash.")
    review.add_argument("--run", type=Path, required=True)
    review.add_argument("--workflow", choices=list(TITLES), required=True)
    review.add_argument("--reviewer", required=True)
    review.add_argument("--decision", choices=["accepted", "rejected"], required=True)
    review.add_argument("--note", required=True)
    args = parser.parse_args(argv)
    root = project_root()
    try:
        if args.command == "harness-evaluate":
            from .harness_evaluation import evaluate, exit_code, preview, write_results
            if args.output.exists():
                raise InputError("Harness output already exists. Choose a new directory.")
            if args.mode != "jev" and (args.allow_network or args.dry_run):
                raise InputError("Network and dry-run flags apply only to Jev mode.")
            classifier = None
            if args.mode == "jev":
                request_preview = preview(root, harness=args.harness, case_id=args.case,
                                          model=args.model, max_calls=args.max_calls)
                if args.dry_run:
                    write_results(request_preview, args.output)
                    print("Jev harness preview saved. No credentials read or network calls made.")
                    return 0
                from .jev_contracts import JevHarnessClassifier
                classifier = JevHarnessClassifier(enabled=args.allow_network, model=args.model, max_calls=args.max_calls)
            result = evaluate(root, mode=args.mode, harness=args.harness, case_id=args.case, classifier=classifier)
            write_results(result, args.output)
            metrics = result["metrics"]
            print(f"{args.mode}: {metrics['cases']} cases, {metrics['wrong_non_review_actions']} wrong actions, {metrics['deferrals']} deferrals, {metrics['failed_control_pairs']} failed control pairs, {metrics['contract_errors']} contract errors. Human review pending.")
            return exit_code(result)
        if args.command == "route-evaluate":
            from .routing_evaluation import dry_run, evaluate_routing, write_evaluation
            from .routing import unit_number
            if args.output.exists():
                raise InputError("Routing output already exists. Choose a new directory.")
            if not unit_number(args.threshold):
                raise InputError("Confidence threshold must be a finite number from 0 to 1.")
            if args.mode != "jev" and (args.allow_network or args.dry_run):
                raise InputError("Network and dry-run flags apply only to Jev mode.")
            router = None
            if args.mode == "jev":
                # Validate the complete local fixture and labels before any paid request.
                preview = dry_run(root, args.model, args.max_calls)
                if args.dry_run:
                    write_evaluation(preview, args.output)
                    print("Jev dry run: request preview saved; no credentials read or network calls made.")
                    return 0
                from .jev import JevRouter
                router = JevRouter(enabled=args.allow_network, model=args.model, max_calls=args.max_calls)
            result = evaluate_routing(root, mode=args.mode, threshold=args.threshold, router=router)
            write_evaluation(result, args.output)
            counts = result["selected_metrics"]
            print(f"{args.mode}: {counts['specialist_suggestions']} suggestions, {counts['wrong_specialist']} wrong against authored labels, {counts['human_review']} human-review deferrals. No workflow dispatched.")
            failed = any(row["selected"]["reason"] == "adapter_or_contract_error" for row in result["rows"])
            return 2 if failed else 0
        if args.command == "evaluate":
            from .evaluation import evaluate
            evaluated = evaluate(args.cases)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(json.dumps(evaluated, indent=2) + "\n")
            print(f"Contract evaluation: {evaluated['passed']}/{evaluated['case_count']} passed.")
            return 1 if evaluated["failed"] else 0
        if args.command == "fixtures":
            args.output.mkdir(parents=True, exist_ok=True)
            for case in CASES:
                path = args.output / (case + ".json")
                path.write_text(json.dumps(sample_data(case), indent=2) + "\n", encoding="utf-8")
            print(f"Wrote {len(CASES)} fictional fixtures to {args.output}")
            return 0
        if args.command == "showcase":
            args.output.parent.mkdir(parents=True, exist_ok=True)
            bundles = [variant_bundle(name) for name in VARIANTS] if args.variants else [sample_bundle(case) for case in CASES]
            args.output.write_text(render_showcase([run_all(bundle) for bundle in bundles], root / "web" / "review.html"), encoding="utf-8")
            print(f"Review page: {args.output}")
            return 0
        if args.command == "package":
            package_project(root, args.output)
            print(f"Showcase package: {args.output}")
            return 0
        if args.command == "review":
            run_data = json.loads(args.run.read_text(encoding="utf-8"))
            record = review_record(run_data, args.workflow, args.reviewer, args.decision, args.note)
            with args.run.with_name("reviews.jsonl").open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(record) + "\n")
            print("Recorded artifact review. The original evidence and product verdict are unchanged.")
            return 0
        policy = None
        if args.command == "run" and args.mode == "model":
            from .provider import OpenAIPolicy
            policy = OpenAIPolicy(enabled=args.allow_network, model=args.model)
        if args.command == "demo":
            bundle = variant_bundle(args.variant) if args.variant else sample_bundle(args.case)
        else:
            bundle = Bundle.load(args.input)
        if args.command == "run" and args.workflow != "all":
            result = run_agent(bundle, args.workflow, policy)
            run_data = {"schema_version": "1.0", "metadata": bundle.metadata, "input_sha256": bundle.fingerprint,
                        "records": bundle.records, "workflows": [result.to_dict()]}
        else:
            run_data = run_all(bundle, policy)
        if policy:
            run_data["model_usage"] = policy.usage
        write_run(run_data, args.output, template=root / "web" / "review.html")
        blocked = sum(r["status"] == "blocked" for r in run_data["workflows"])
        print(f"Wrote {len(run_data['workflows'])} workflow artifacts to {args.output}; blocked workflows: {blocked}.")
        return 2 if blocked else 0
    except (InputError, OSError, ValueError, KeyError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())

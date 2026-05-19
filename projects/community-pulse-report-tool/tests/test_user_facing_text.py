from pathlib import Path

from community_pulse.cli import build_parser


PROJECT_ROOT = Path(__file__).resolve().parents[1]
USER_FACING_PATHS = [
    PROJECT_ROOT / "README.md",
    PROJECT_ROOT / "pyproject.toml",
    PROJECT_ROOT / "reports",
    PROJECT_ROOT / "sample-data",
    PROJECT_ROOT / "src" / "community_pulse",
    PROJECT_ROOT / "tests",
]


def test_user_facing_files_do_not_use_em_dash() -> None:
    offenders = []
    for base_path in USER_FACING_PATHS:
        paths = [base_path] if base_path.is_file() else base_path.rglob("*")
        for path in paths:
            if path.is_file() and path.suffix in {".md", ".csv", ".py", ".txt", ".yml", ".toml"}:
                if "\u2014" in path.read_text(encoding="utf-8"):
                    offenders.append(str(path.relative_to(PROJECT_ROOT)))

    assert offenders == []


def test_cli_help_does_not_use_em_dash() -> None:
    help_text = build_parser().format_help()

    assert "\u2014" not in help_text

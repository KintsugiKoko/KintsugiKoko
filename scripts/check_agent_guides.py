"""Check repository agent guides for required operating rules.

This script is intentionally small and dependency-free so it can run in GitHub
Actions without installing the project packages.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def require_order(text: str, labels: list[tuple[str, str]]) -> None:
    last_index = -1
    for label, needle in labels:
        index = text.find(needle)
        if index == -1:
            raise AssertionError(f"Missing ordered item {label}: {needle}")
        if index <= last_index:
            raise AssertionError(f"Out of order item {label}: {needle}")
        last_index = index


def check_root_prompt_lanes(root_agents: str) -> None:
    require_contains(root_agents, "## Prompt Lane Rule", "Prompt Lane Rule section")
    require_contains(root_agents, "## Codex Response Rules", "Codex Response Rules section")
    require_contains(root_agents, "Codex Lane always comes first.", "Codex-first rule")
    require_contains(root_agents, "GPT Lane always comes second.", "GPT-second rule")
    require_contains(
        root_agents,
        "Do not interleave Codex and GPT prompts.",
        "no-interleaving rule",
    )
    require_contains(
        root_agents,
        "Do not provide only one rank unless the user explicitly asks for a single prompt.",
        "full-rank default rule",
    )
    require_contains(
        root_agents,
        "Do not include Wood prompts in Codex responses.",
        "no Wood prompts in Codex responses rule",
    )
    if "Wood / Codex" in root_agents:
        raise AssertionError("Wood / Codex should not appear in root AGENTS.md")

    require_order(
        root_agents,
        [
            ("Codex Lane", "1. Codex Lane"),
            ("Gold / Codex", "ELO 1400 — Gold / Codex"),
            ("Diamond / Codex", "ELO 1800 — Diamond / Codex"),
            ("GPT Lane", "2. GPT Lane"),
            ("Wood / GPT", "ELO 1000 — Wood / GPT"),
            ("Gold / GPT", "ELO 1400 — Gold / GPT"),
            ("Diamond / GPT", "ELO 1800 — Diamond / GPT"),
        ],
    )

    require_contains(root_agents, "## GPT Review Prompt", "GPT handoff heading")
    require_contains(
        root_agents,
        "Optional Gold / Codex or Diamond / Codex next step if needed",
        "optional Codex next step rule",
    )


def check_test_plan_agents(root_agents: str) -> None:
    require_contains(root_agents, "## Test Plan Agents", "Test Plan Agents section")
    for role in [
        "Test Plan Lead",
        "Scenario Designer",
        "Verification Runner",
        "Regression Scout",
        "Evidence Scribe",
    ]:
        require_contains(root_agents, role, f"Test Plan Agent role {role}")

    for phrase in [
        "They are not autonomous services",
        "Does not claim verification passed unless the check was actually run.",
        "Leads with evidence instead of hype.",
    ]:
        require_contains(root_agents, phrase, f"Test Plan Agent safety phrase {phrase}")


def check_project_guides() -> None:
    expected_guides = {
        "projects/qa-engineer-hyperbolic-time-chamber/AGENTS.md": [
            "QA Tooling Standards",
            "Verification Rules",
            "agent-supervised workflows",
        ],
        "projects/nyx/AGENTS.md": [
            "Project Nyx",
            "PIE",
            "Portfolio Safety Rules",
        ],
    }

    for path, phrases in expected_guides.items():
        guide = read(path)
        for phrase in phrases:
            require_contains(guide, phrase, f"{path} phrase {phrase}")


def main() -> None:
    root_agents = read("AGENTS.md")
    check_root_prompt_lanes(root_agents)
    check_test_plan_agents(root_agents)
    check_project_guides()
    print("Agent guide checks passed.")


if __name__ == "__main__":
    main()

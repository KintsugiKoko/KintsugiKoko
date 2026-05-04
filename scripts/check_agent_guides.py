"""Check repository agent guides for required operating rules.

This script is intentionally small and dependency-free so it can run in GitHub
Actions without installing the project packages.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WOOD_CODEX_LABEL = "Wood " + "/ Codex"


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


def agent_guides() -> list[Path]:
    return sorted(ROOT.rglob("AGENTS.md"))


def check_no_response_format_drift() -> None:
    disallowed_phrases = [
        WOOD_CODEX_LABEL,
        "Wood-ranked Codex",
        "Beginner ELO",
        "Intermediate ELO",
        "Expert ELO",
        "Beginner / Codex",
        "Intermediate / Codex",
        "Expert / Codex",
        "Beginner / GPT",
        "Intermediate / GPT",
        "Expert / GPT",
        "Do not provide only one rank unless",
        "If one option is recommended, still provide the full prompt pack",
        "GPT Lane always comes second.",
        "Wood, Gold, and Diamond for GPT follow-ups when useful",
    ]

    for path in agent_guides():
        text = path.read_text(encoding="utf-8")
        rel_path = path.relative_to(ROOT)
        for phrase in disallowed_phrases:
            if phrase in text:
                raise AssertionError(
                    f"Response-format drift in {rel_path}: {phrase}"
                )


def check_root_prompt_lanes(root_agents: str) -> None:
    require_contains(root_agents, "## Prompt Lane Rule", "Prompt Lane Rule section")
    require_contains(root_agents, "## Codex Response Rules", "Codex Response Rules section")
    require_contains(root_agents, "Codex Lane always comes first.", "Codex-first rule")
    require_contains(
        root_agents,
        "🧠 Brain / GPT comes second when a GPT handoff is included.",
        "GPT handoff second rule",
    )
    require_contains(
        root_agents,
        "Do not interleave Codex and GPT prompts.",
        "no-interleaving rule",
    )
    require_contains(
        root_agents,
        "GPT should provide the single best next answer or next-step prompt based on the current sprint goal.",
        "single best GPT handoff rule",
    )
    require_contains(
        root_agents,
        "GPT should not provide three rank options by default unless Keith explicitly asks.",
        "no default GPT rank menu rule",
    )
    require_contains(
        root_agents,
        "Do not include Wood prompts in Codex responses.",
        "no Wood prompts in Codex responses rule",
    )
    if WOOD_CODEX_LABEL in root_agents:
        raise AssertionError(f"{WOOD_CODEX_LABEL} should not appear in root AGENTS.md")

    require_order(
        root_agents,
        [
            ("Codex Lane", "1. Codex Lane"),
            ("Gold / Codex", "ELO 1400 — Gold / Codex"),
            ("Diamond / Codex", "ELO 1800 — Diamond / Codex"),
            ("Brain / GPT", "2. 🧠 Brain / GPT"),
            (
                "single best GPT prompt",
                "One best ChatGPT answer or next-step prompt based on the current sprint goal",
            ),
        ],
    )

    require_contains(root_agents, "## 🧠 Brain / GPT", "GPT handoff heading")
    require_contains(
        root_agents,
        "GPT handoff is separate from Codex guidance.",
        "separate GPT handoff rule",
    )
    require_contains(
        root_agents,
        "Diamond / Codex follow-up prompt for meaningful work where audit, hardening, branch review, or portfolio-signal review would help",
        "required Diamond / Codex next step rule",
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
    check_no_response_format_drift()
    check_root_prompt_lanes(root_agents)
    check_test_plan_agents(root_agents)
    check_project_guides()
    print("Agent guide checks passed.")


if __name__ == "__main__":
    main()

# Nyx Test Planner

Nyx Test Planner is a browser-based QA planning prototype that demonstrates how I turn early gameplay ideas into human-reviewed test scenarios, risk notes, and validation-ready Markdown plans before implementation gets messy.

It is built for public portfolio review and project planning. It does not connect to Unreal Engine, Jira, private studio tools, internal data, or automated test runners.

## What It Demonstrates

- Test planning before implementation gets too messy
- Scenario organization by gameplay area, risk, status, and validation type
- QA thinking around Nyx's WIP core loop
- Human-reviewed AI-assisted planning habits
- Plain HTML, CSS, and JavaScript without a framework

## QA Portfolio Signal

This tool is meant to show test-planning judgment, not completed Nyx gameplay. A reviewer should be able to see how a broad prototype idea becomes scoped checks, risk labels, PIE readiness notes, and a Markdown plan that still needs human review.

## Live Tool

[Open the Nyx Test Planner](https://kintsugikoko.github.io/KintsugiKoko/nyx-test-planner.html)

## Case Study

[Case study: turning one planned scenario into a human-reviewed QA validation pass](../../docs/nyx-test-planner-case-study.md)

## Best Reviewer Path

1. Open the live planner.
2. Scan the planning snapshot to see total, high-risk, ready, and blocked checks.
3. Filter by `Ready for PIE` or `High` risk to see the clearest validation targets.
4. Review the case study to see how one Starwell offering idea becomes a planned validation path.
5. Generate the Markdown draft and review the Method / Limitations section.
6. Treat the export as planning evidence, not proof that the Unreal pass has already run.

## Related Portfolio Docs

- [Unreal Test Levels And Scenarios](../../docs/unreal-test-levels-and-scenarios.md)
- [Tool Audit Report](../../docs/tool-audit-report.md)

## Current Scope

The planner starts with sample scenarios for:

- Fishing casts
- Bite, reel, and catch flow
- Inventory and economy checks
- Starwell offerings
- Save/load reliability
- Merchant and run progression
- Blueprint presentation refresh

The scenarios are planning examples, not proof that every Nyx system is complete.

## How To Use It

1. Open the live planner.
2. Filter scenarios by area, status, risk, or search text.
3. Add a draft scenario when a new QA question appears.
4. Generate a Markdown test plan from the current filtered board.
5. Review the exported plan before using it as project documentation.

## Data And Safety

- The tool uses public, portfolio-safe Nyx planning notes only.
- Added scenarios are stored in the browser through `localStorage`.
- No data leaves the browser.
- No proprietary or internal studio data should be entered.

## Known Limitations

- This is not an automated test runner.
- It does not read Unreal logs, assets, or build data.
- Added scenario steps use a simple notes field.
- There is no multi-user sync.
- The exported Markdown is a draft that still needs human review.

## Future Improvements

- Add severity and priority fields.
- Add setup requirements for PIE test passes.
- Add screenshot or evidence placeholders.
- Add import/export JSON.
- Add a separate checklist view for smoke, regression, and presentation passes.

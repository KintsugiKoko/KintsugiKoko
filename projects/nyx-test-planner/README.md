# Nyx Test Planner

The Nyx Test Planner is a small live browser tool for turning Nyx gameplay ideas into a visible QA plan.

It is built for public portfolio review and project planning. It does not connect to Unreal Engine, Jira, private studio tools, internal data, or automated test runners.

## What It Demonstrates

- Test planning before implementation gets too messy
- Scenario organization by gameplay area, risk, status, and validation type
- QA thinking around Nyx's WIP core loop
- Human-reviewed AI-assisted planning habits
- Plain HTML, CSS, and JavaScript without a framework

## Live Tool

[Open the Nyx Test Planner](https://kintsugikoko.github.io/KintsugiKoko/nyx-test-planner.html)

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

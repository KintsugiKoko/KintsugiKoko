const handoff = {
  feature: "Mount Equipment Visual Validation",
  build: "Mock-0.9.42",
  environment: "PC development build, mock external QA environment",
  testWindow: "Two-day external QA pass",
  testOwner: "QA Lead",
  externalTeam: "Mock External QA Vendor A",
  objective: "Validate that mount equipment visuals attach, swap, hide, and persist correctly across common player-facing flows.",
  setupSteps: "1. Launch the mock development build.\n2. Use the test account with mount equipment unlocked.\n3. Enter the Mount Visual Validation test area.\n4. Capture screenshots or video for every blocking or high-risk issue.",
  dataRequirements: "Test account with three mount types, three equipment variants, one empty equipment slot, and one known issue reference list.",
  debugNotes: "Use documented test setup notes only. Do not use private studio commands. Record build, platform, scenario, and capture timestamp.",
  inScope: "Mount equipment attach points, visual swaps, spawn/despawn, inventory equip flow, screenshot/video evidence, and duplicate checks.",
  outOfScope: "Balance, economy tuning, final art approval, animation polish sign-off, and production pipeline validation.",
  knownIssues: "Known Issue A: saddle icon mismatch in inventory only.\nKnown Issue B: cosmetic preview lighting is under separate review.",
  dailySummary: "Summarize tested scenarios, blocker/high bugs, evidence gaps, duplicate trends, and release-readiness risk.",
  scenarios: [
    ["Equip saddle variant A", "High", "PC", "Screenshot + repro steps", "Art / QA", "Ready", "Validate attach point and material visibility."],
    ["Swap equipment while mounted", "High", "PC", "Video + repro rate", "Engineering / QA", "Ready", "Watch for stale mesh or wrong variant."],
    ["Spawn mount after zone reload", "Medium", "PC", "Screenshot", "Engineering", "Ready", "Check persistence after reload."],
    ["Empty equipment slot", "Medium", "PC", "Screenshot", "Design / QA", "Ready", "Confirm fallback visuals are understandable."],
    ["Known issue duplicate sweep", "High", "PC", "Known issue reference", "QA", "Ready", "Prevent duplicate bug noise."]
  ],
  bugStandards: [
    "Build number",
    "Platform",
    "Exact repro steps",
    "Expected result",
    "Actual result",
    "Repro rate",
    "Screenshot/video",
    "Logs/telemetry if available",
    "Severity suggestion",
    "Known issue/duplicate check"
  ],
  intakeChecklist: [
    "Repro steps clear",
    "Evidence attached",
    "Duplicate checked",
    "Known issue checked",
    "Severity reasonable",
    "Correct owner/routing",
    "Needs more info",
    "Ready for Jira/dev review"
  ]
};

const incomingBugs = [
  {
    id: "EXT-001",
    title: "Saddle variant B stays visible after unequip",
    build: "Mock-0.9.42",
    platform: "PC",
    scenario: "Swap equipment while mounted",
    steps: "Equip saddle B, mount up, unequip saddle, rotate camera.",
    expected: "Saddle mesh hides after unequip.",
    actual: "Saddle B remains visible until remount.",
    reproRate: "4/4",
    evidence: true,
    reference: "video_mount_swap_001.mp4 @ 00:18",
    severity: "High",
    knownIssue: false,
    owner: "Engineering",
    notes: "Strong repro and clear capture."
  },
  {
    id: "EXT-002",
    title: "Mount preview lighting looks too dark",
    build: "Mock-0.9.42",
    platform: "PC",
    scenario: "Inventory preview",
    steps: "Open inventory preview.",
    expected: "Preview remains readable.",
    actual: "Preview is dark.",
    reproRate: "2/4",
    evidence: false,
    reference: "",
    severity: "Medium",
    knownIssue: true,
    owner: "Art",
    notes: "Matches known issue B."
  },
  {
    id: "EXT-003",
    title: "Mount gear clips through armor set after zone reload",
    build: "Mock-0.9.42",
    platform: "PC",
    scenario: "Spawn mount after zone reload",
    steps: "Equip armor set C and saddle A, reload zone, summon mount.",
    expected: "Armor and mount equipment do not visibly intersect.",
    actual: "Saddle edge clips through leg armor during idle.",
    reproRate: "3/5",
    evidence: true,
    reference: "screenshot_clip_003.png",
    severity: "Medium",
    knownIssue: false,
    owner: "Tech Art",
    notes: "Needs owner review but evidence is usable."
  },
  {
    id: "EXT-004",
    title: "Cosmetic disappears sometimes",
    build: "",
    platform: "PC",
    scenario: "Unknown",
    steps: "It happened after swapping a few things.",
    expected: "",
    actual: "Cosmetic missing.",
    reproRate: "",
    evidence: false,
    reference: "",
    severity: "High",
    knownIssue: false,
    owner: "QA",
    notes: "Too vague for developer review."
  },
  {
    id: "EXT-005",
    title: "Wrong icon shown for empty saddle slot",
    build: "Mock-0.9.42",
    platform: "PC",
    scenario: "Empty equipment slot",
    steps: "Remove saddle equipment and inspect inventory.",
    expected: "Empty slot icon appears.",
    actual: "Previous saddle icon remains in inventory only.",
    reproRate: "5/5",
    evidence: true,
    reference: "empty_slot_icon_005.png",
    severity: "Low",
    knownIssue: true,
    owner: "UI",
    notes: "Known issue A."
  },
  {
    id: "EXT-006",
    title: "Mount equipment material flickers during spawn",
    build: "Mock-0.9.42",
    platform: "PC",
    scenario: "Mount spawn VFX",
    steps: "Equip saddle C, trigger mount spawn five times in test area.",
    expected: "Material remains stable during spawn.",
    actual: "Gold trim flickers for one frame during spawn.",
    reproRate: "3/5",
    evidence: true,
    reference: "video_spawn_flicker_006.mp4 @ 00:07",
    severity: "Medium",
    knownIssue: false,
    owner: "Tech Art",
    notes: "Good candidate for Tech Art review."
  }
];

const decisions = new Map();

function $(id) {
  return document.getElementById(id);
}

function setValue(id, value) {
  const node = $(id);
  if (node) node.value = value;
}

function initializeBuilder() {
  Object.entries(handoff).forEach(([key, value]) => {
    if (typeof value === "string") setValue(key, value);
  });
  $("scenario-table").innerHTML = handoff.scenarios.map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`).join("");
  $("bug-standards").innerHTML = handoff.bugStandards.map((item) => `<li>${item}</li>`).join("");
  $("intake-checklist").innerHTML = handoff.intakeChecklist.map((item) => `<li>${item}</li>`).join("");
  updateHandoffMarkdown();
}

function formValue(id) {
  return $(id)?.value.trim() || "";
}

function scenarioMarkdown() {
  const header = "| Scenario | Priority | Platform | Evidence | Owner | Status | Notes |\n| --- | --- | --- | --- | --- | --- | --- |";
  const rows = handoff.scenarios.map((row) => `| ${row.join(" | ")} |`);
  return [header, ...rows].join("\n");
}

function listMarkdown(items) {
  return items.map((item) => `- ${item}`).join("\n");
}

function generateHandoffMarkdown() {
  return `# External QA Handoff Packet

## Handoff Overview

- Feature / Test Area: ${formValue("feature")}
- Build Number: ${formValue("build")}
- Platform / Environment: ${formValue("environment")}
- Test Window: ${formValue("testWindow")}
- Test Owner: ${formValue("testOwner")}
- External QA Team: ${formValue("externalTeam")}

## Objective

${formValue("objective")}

## Setup Instructions

${formValue("setupSteps")}

## Account / Character / Data Requirements

${formValue("dataRequirements")}

## Debug Commands Or Test Setup Notes

${formValue("debugNotes")}

## Scope

### In Scope

${formValue("inScope")}

### Out Of Scope

${formValue("outOfScope")}

### Known Issues

${formValue("knownIssues")}

## Scenario Matrix

${scenarioMarkdown()}

## Bug Standards

${listMarkdown(handoff.bugStandards)}

## Evidence Requirements

- Screenshot or video reference for visible issues
- Build number, platform, scenario, and timestamp
- Repro rate and exact setup path
- Logs or telemetry only when available
- Known issue and duplicate check before escalation

## Escalation Rules

- Blocker or crash risk: escalate same day.
- High player-facing visual regression: include video and likely owner routing.
- Missing evidence: return to external QA for more information.
- Known issue match: link to known issue notes instead of creating duplicate noise.

## Daily Summary Template

${formValue("dailySummary")}

## QA Lead Intake Review Checklist

${listMarkdown(handoff.intakeChecklist)}
`;
}

function updateHandoffMarkdown() {
  $("handoff-output").value = generateHandoffMarkdown();
}

function evaluateBug(bug) {
  if (bug.knownIssue) return "Duplicate / Known Issue";
  const keyFields = [bug.build, bug.platform, bug.steps, bug.expected, bug.actual, bug.reproRate, bug.owner];
  const completeFields = keyFields.filter(Boolean).length;
  if (completeFields >= keyFields.length && bug.evidence) return "Ready for Dev Review";
  return "Needs More Info";
}

function renderScenarioCards() {
  $("scenario-cards").innerHTML = handoff.scenarios.slice(0, 5).map((row) => `
    <article class="scenario-card">
      <span>${row[1]} priority</span>
      <strong>${row[0]}</strong>
      <p>${row[6]}</p>
    </article>
  `).join("");
}

function renderBugCards() {
  $("bug-list").innerHTML = incomingBugs.map((bug) => {
    const state = decisions.get(bug.id) || "Unreviewed";
    return `
      <article class="bug-card" data-state="${state}">
        <span>${bug.id} / ${bug.scenario}</span>
        <h4>${bug.title}</h4>
        <p><strong>Build:</strong> ${bug.build || "Missing"} / <strong>Platform:</strong> ${bug.platform || "Missing"}</p>
        <p><strong>Steps:</strong> ${bug.steps || "Missing clear steps"}</p>
        <p><strong>Expected:</strong> ${bug.expected || "Missing"}<br><strong>Actual:</strong> ${bug.actual || "Missing"}</p>
        <p><strong>Repro:</strong> ${bug.reproRate || "Missing"} / <strong>Evidence:</strong> ${bug.evidence ? bug.reference : "Missing"}</p>
        <p><strong>Severity:</strong> ${bug.severity} / <strong>Owner:</strong> ${bug.owner}</p>
        <p><strong>QA Note:</strong> ${bug.notes}</p>
        <span class="bug-status">${state}</span>
        <div class="bug-actions">
          <button type="button" data-id="${bug.id}" data-decision="Ready for Dev Review">Ready for Dev Review</button>
          <button type="button" data-id="${bug.id}" data-decision="Needs More Info">Needs More Info</button>
          <button type="button" data-id="${bug.id}" data-decision="Duplicate / Known Issue">Duplicate / Known Issue</button>
        </div>
      </article>
    `;
  }).join("");
}

function summaryCounts() {
  const values = [...decisions.values()];
  return {
    reviewed: values.length,
    ready: values.filter((value) => value === "Ready for Dev Review").length,
    needsInfo: values.filter((value) => value === "Needs More Info").length,
    duplicate: values.filter((value) => value === "Duplicate / Known Issue").length
  };
}

function updateSummary() {
  const counts = summaryCounts();
  const readiness = incomingBugs.length ? Math.round((counts.reviewed / incomingBugs.length) * 100) : 0;
  $("readiness-score").textContent = `${readiness}%`;
  $("meter-bar").style.width = `${readiness}%`;
  $("review-count").textContent = `${counts.reviewed} reviewed`;
  $("ready-count").textContent = counts.ready;
  $("needs-info-count").textContent = counts.needsInfo;
  $("duplicate-count").textContent = counts.duplicate;
  $("coverage-gaps").innerHTML = [
    "Confirm mount equipment reload persistence on all target platforms.",
    "Ask external QA for clearer capture on vague cosmetic disappearance reports.",
    "Keep known issue matching visible in daily summaries."
  ].map((item) => `<li>${item}</li>`).join("");
  $("top-risks").innerHTML = [
    "High-confidence stale mesh repro should reach Engineering with video evidence.",
    "Material flicker needs Tech Art review before release-readiness signoff.",
    "Bug noise increases if missing-evidence reports bypass intake review."
  ].map((item) => `<li>${item}</li>`).join("");
}

function generateSummaryMarkdown() {
  const counts = summaryCounts();
  const bugRows = incomingBugs.map((bug) => {
    const decision = decisions.get(bug.id) || "Unreviewed";
    return `| ${bug.id} | ${bug.title} | ${bug.severity} | ${bug.owner} | ${decision} |`;
  }).join("\n");

  return `# QA Lead Intake Summary

## Review Snapshot

- Feature: ${handoff.feature}
- Build: ${handoff.build}
- Reviewed bug cards: ${counts.reviewed}/${incomingBugs.length}
- Ready for Dev Review: ${counts.ready}
- Needs More Info: ${counts.needsInfo}
- Duplicate / Known Issue: ${counts.duplicate}

## Intake Decisions

| ID | Title | Severity | Suggested Owner | Decision |
| --- | --- | --- | --- | --- |
${bugRows}

## Coverage Gaps

- Confirm mount equipment reload persistence on all target platforms.
- Ask external QA for clearer capture on vague cosmetic disappearance reports.
- Keep known issue matching visible in daily summaries.

## Top Risks

- High-confidence stale mesh repro should reach Engineering with video evidence.
- Material flicker needs Tech Art review before release-readiness signoff.
- Bug noise increases if missing-evidence reports bypass intake review.

## QA Lead Notes

This summary uses mock portfolio-safe data. It is meant to demonstrate QA lead intake discipline, evidence standards, owner routing, and release-readiness communication. It does not connect to Jira or any private studio workflow.
`;
}

function initializeDemo() {
  renderScenarioCards();
  renderBugCards();
  updateSummary();
  $("summary-output").value = generateSummaryMarkdown();
}

function copyFrom(id) {
  const node = $(id);
  node.select();
  if (navigator.clipboard) {
    navigator.clipboard.writeText(node.value).catch(() => document.execCommand("copy"));
  } else {
    document.execCommand("copy");
  }
}

function downloadMarkdown(id, filename) {
  const blob = new Blob([$(id).value], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

document.addEventListener("click", (event) => {
  const tabButton = event.target.closest(".tab-button");
  if (tabButton) {
    document.querySelectorAll(".tab-button").forEach((button) => button.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach((panel) => panel.classList.remove("active"));
    tabButton.classList.add("active");
    $(tabButton.dataset.tab).classList.add("active");
  }

  const decisionButton = event.target.closest("[data-decision]");
  if (decisionButton) {
    decisions.set(decisionButton.dataset.id, decisionButton.dataset.decision);
    renderBugCards();
    updateSummary();
    $("summary-output").value = generateSummaryMarkdown();
  }
});

document.addEventListener("input", (event) => {
  if (event.target.closest("#builder")) updateHandoffMarkdown();
});

$("copy-handoff").addEventListener("click", () => copyFrom("handoff-output"));
$("copy-summary").addEventListener("click", () => copyFrom("summary-output"));
$("download-handoff").addEventListener("click", () => downloadMarkdown("handoff-output", "external-qa-handoff-packet.md"));
$("download-summary").addEventListener("click", () => downloadMarkdown("summary-output", "qa-lead-intake-summary.md"));
$("generate-summary").addEventListener("click", () => {
  $("summary-output").value = generateSummaryMarkdown();
});

initializeBuilder();
initializeDemo();

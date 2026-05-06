const HANDOFF = {
  feature: "Nyx Starwell Offering First Pass",
  build: "Portfolio sample build / mock handoff packet",
  owner: "QA lead review",
  goal: "Validate that an offsite QA tester can understand the feature goal, run the right scenario checks, capture useful evidence, and send back Jira-ready bug reports for human review.",
  note: "Mock data only. This tool does not connect to Jira, vendor portals, private studio workflows, internal test plans, or live production data."
};

const SCENARIOS = [
  {
    title: "First successful offering updates progress once",
    area: "Core loop",
    risk: "High",
    status: "Ready for handoff",
    expected: "Offering one valid fish consumes one item, advances Starwell progress once, and shows readable feedback.",
    evidence: "Short clip from offer action through progress update, plus screenshot of inventory after the action."
  },
  {
    title: "Invalid offering is rejected with clear messaging",
    area: "Error handling",
    risk: "Medium",
    status: "Ready for handoff",
    expected: "An invalid item is not consumed and the player receives a readable reason the offering failed.",
    evidence: "Screenshot of message state and notes on input/item used."
  },
  {
    title: "Progress threshold does not double-fire reward",
    area: "Regression",
    risk: "High",
    status: "Needs setup",
    expected: "Reaching the threshold grants the reward one time and does not repeat after menu reopen or level reload.",
    evidence: "Clip showing threshold reach, reward state, menu reopen, and follow-up check."
  },
  {
    title: "Placeholder content is labeled clearly",
    area: "Presentation",
    risk: "Low",
    status: "Ready for handoff",
    expected: "Any temporary art, text, or tuning value is readable and does not imply final content.",
    evidence: "Screenshot of placeholder-facing UI or environment state."
  }
];

const BUG_STANDARDS = [
  "Clear title with feature area and player-facing impact",
  "Build, branch, platform/config, and test account/setup notes",
  "Repeatable steps with expected result and actual result",
  "Severity, priority suggestion, repro rate, and regression risk",
  "Screenshot or short clip with timestamp when visual behavior matters",
  "Follow-up note when the issue may need design, art, engineering, or QA owner review"
];

const EVIDENCE_REQUIREMENTS = [
  "Screenshot or short clip for each failed or unclear scenario",
  "Notes on the exact sample build/prototype version used",
  "Pass/fail/blocked status for each scenario",
  "One concise risk summary for QA lead intake",
  "Separate follow-up note for tuning feedback versus functional defects"
];

const INTAKE_CHECKLIST = [
  "Confirm the tester used the intended build and setup notes",
  "Check whether the reported issue has enough repro detail",
  "Separate valid bugs from tuning feedback and unclear observations",
  "Route likely ownership without pretending the export filed a Jira ticket",
  "Record any missing evidence before calling the pass complete"
];

function createCard(title, meta, body) {
  const article = document.createElement("article");
  article.className = "scenario-card";

  const heading = document.createElement("h3");
  heading.textContent = title;

  const pill = document.createElement("span");
  pill.className = "status-pill";
  pill.textContent = meta;

  const paragraph = document.createElement("p");
  paragraph.textContent = body;

  article.append(pill, heading, paragraph);
  return article;
}

function renderScenarios() {
  const list = document.querySelector("#scenario-list");
  list.innerHTML = "";

  SCENARIOS.forEach((scenario) => {
    const article = createCard(
      scenario.title,
      `${scenario.area} / ${scenario.risk} / ${scenario.status}`,
      `${scenario.expected} Evidence: ${scenario.evidence}`
    );
    article.dataset.risk = scenario.risk;
    list.append(article);
  });
}

function renderList(targetId, items, label) {
  const list = document.querySelector(targetId);
  list.innerHTML = "";

  items.forEach((item, index) => {
    list.append(createCard(`${label} ${index + 1}`, label, item));
  });
}

function updateSummary() {
  document.querySelector("#scenario-count").textContent = SCENARIOS.length;
  document.querySelector("#high-risk-count").textContent = SCENARIOS.filter((scenario) => scenario.risk === "High").length;
  document.querySelector("#evidence-count").textContent = EVIDENCE_REQUIREMENTS.length;
  document.querySelector("#intake-count").textContent = INTAKE_CHECKLIST.length;
}

function buildMarkdown() {
  const lines = [
    `# External QA Handoff: ${HANDOFF.feature}`,
    "",
    "## Handoff Context",
    "",
    `- Build/context: ${HANDOFF.build}`,
    `- Owner: ${HANDOFF.owner}`,
    `- Goal: ${HANDOFF.goal}`,
    `- Safety note: ${HANDOFF.note}`,
    "",
    "## Scenario Matrix",
    ""
  ];

  SCENARIOS.forEach((scenario) => {
    lines.push(`### ${scenario.title}`);
    lines.push(`- Area: ${scenario.area}`);
    lines.push(`- Risk: ${scenario.risk}`);
    lines.push(`- Status: ${scenario.status}`);
    lines.push(`- Expected result: ${scenario.expected}`);
    lines.push(`- Evidence needed: ${scenario.evidence}`);
    lines.push("");
  });

  lines.push("## Bug-Quality Standards", "");
  BUG_STANDARDS.forEach((standard) => lines.push(`- ${standard}`));
  lines.push("", "## Evidence Requirements", "");
  EVIDENCE_REQUIREMENTS.forEach((requirement) => lines.push(`- ${requirement}`));
  lines.push("", "## QA Lead Intake Checklist", "");
  INTAKE_CHECKLIST.forEach((item) => lines.push(`- [ ] ${item}`));
  lines.push(
    "",
    "## Portfolio-Safe Boundary",
    "",
    "This is a human-reviewed external QA planning artifact using mock data. It does not connect to Jira, vendor portals, private studio workflows, internal test plans, or live production data."
  );

  return lines.join("\n");
}

function generateMarkdown() {
  document.querySelector("#markdown-output").value = buildMarkdown();
}

async function copyMarkdown() {
  const output = document.querySelector("#markdown-output");
  if (!output.value) {
    generateMarkdown();
  }

  output.select();

  if (navigator.clipboard) {
    await navigator.clipboard.writeText(output.value);
  } else {
    document.execCommand("copy");
  }
}

function init() {
  updateSummary();
  renderScenarios();
  renderList("#bug-standards", BUG_STANDARDS, "Bug standard");
  renderList("#evidence-list", [...EVIDENCE_REQUIREMENTS, ...INTAKE_CHECKLIST], "Review item");
  generateMarkdown();

  document.querySelector("#export-markdown").addEventListener("click", generateMarkdown);
  document.querySelector("#copy-markdown").addEventListener("click", copyMarkdown);
}

init();

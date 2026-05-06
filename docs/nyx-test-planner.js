const STORAGE_KEY = "nyx-test-planner-scenarios-v1";

const AREAS = [
  "FTUE / First Session",
  "Fishing Cast",
  "Bite / Reel / Catch",
  "Inventory / Economy",
  "Starwell Offering",
  "Save / Load",
  "Merchant / Run Progression",
  "Blueprint Presentation"
];

const STATUSES = ["Planned", "Ready for PIE", "Blocked", "Passed", "Needs revision"];
const RISKS = ["High", "Medium", "Low"];
const TYPES = ["Smoke", "Regression", "Exploratory", "Validation", "Presentation"];

const SAMPLE_SCENARIOS = [
  {
    title: "Start a first fishing cast from a clean session",
    area: "Fishing Cast",
    type: "Smoke",
    risk: "High",
    status: "Ready for PIE",
    expected: "The player can begin a cast, see clear feedback, and return safely to Idle if the cast is cancelled.",
    steps: [
      "Open a clean PIE session.",
      "Start a fishing cast from the intended test location.",
      "Cancel the cast and confirm the component returns to Idle."
    ],
    notes: "Protects the first player-facing interaction in the loop."
  },
  {
    title: "Catch flow reaches inventory without duplicate rewards",
    area: "Bite / Reel / Catch",
    type: "Validation",
    risk: "High",
    status: "Planned",
    expected: "Completing a catch adds one valid fish entry and does not duplicate rewards or leave the cast active.",
    steps: [
      "Force or wait for a bite.",
      "Reel until the catch completes.",
      "Check inventory count and fishing state."
    ],
    notes: "Core loop risk: catch completion, inventory update, and state cleanup."
  },
  {
    title: "Offering fish updates Starwell progress once",
    area: "Starwell Offering",
    type: "Regression",
    risk: "High",
    status: "Ready for PIE",
    expected: "Offering a valid fish grants the intended reward and advances Starwell progress once.",
    steps: [
      "Start with at least one valid fish in inventory.",
      "Offer the fish to the Starwell.",
      "Confirm inventory, reward, threshold progress, and event feedback."
    ],
    notes: "Good candidate for repeated fix verification after economy or threshold changes."
  },
  {
    title: "Save/load normalizes active cast back to Idle",
    area: "Save / Load",
    type: "Smoke",
    risk: "High",
    status: "Ready for PIE",
    expected: "Durable progress persists, but transient active cast state does not restore into a fragile runtime state.",
    steps: [
      "Begin an active cast.",
      "Trigger save and reload.",
      "Confirm fishing state is safe and understandable after load."
    ],
    notes: "Documents the reliability rule already captured in the Nyx showcase."
  },
  {
    title: "Merchant/run progression communicates unavailable content clearly",
    area: "Merchant / Run Progression",
    type: "Exploratory",
    risk: "Medium",
    status: "Blocked",
    expected: "Unavailable or placeholder progression content is labeled clearly and does not imply a finished system.",
    steps: [
      "Open merchant or run-progression UI when available.",
      "Check locked, placeholder, or incomplete states.",
      "Record missing copy, unclear status, or misleading affordances."
    ],
    notes: "WIP honest labeling matters for both development and portfolio documentation."
  },
  {
    title: "Post-load presentation refresh does not replay one-time rewards",
    area: "Blueprint Presentation",
    type: "Presentation",
    risk: "Medium",
    status: "Planned",
    expected: "UI, VFX, audio, and world presentation refresh after load without replaying reward grants.",
    steps: [
      "Load a save with existing Starwell progress.",
      "Observe UI, VFX, audio, and world state.",
      "Confirm restoration events are separate from gameplay reward events."
    ],
    notes: "Keeps Blueprint presentation hooks separate from durable progress restoration."
  }
];

const state = {
  scenarios: loadScenarios(),
  filters: {
    search: "",
    area: "all",
    status: "all",
    risk: "all"
  }
};

const elements = {
  total: document.querySelector("#total-count"),
  highRisk: document.querySelector("#high-risk-count"),
  ready: document.querySelector("#ready-count"),
  blocked: document.querySelector("#blocked-count"),
  search: document.querySelector("#search-input"),
  areaFilter: document.querySelector("#area-filter"),
  statusFilter: document.querySelector("#status-filter"),
  riskFilter: document.querySelector("#risk-filter"),
  list: document.querySelector("#scenario-list"),
  form: document.querySelector("#scenario-form"),
  title: document.querySelector("#scenario-title"),
  area: document.querySelector("#scenario-area"),
  type: document.querySelector("#scenario-type"),
  risk: document.querySelector("#scenario-risk"),
  status: document.querySelector("#scenario-status"),
  notes: document.querySelector("#scenario-notes"),
  reset: document.querySelector("#reset-plan"),
  exportButton: document.querySelector("#export-markdown"),
  copyButton: document.querySelector("#copy-markdown"),
  markdown: document.querySelector("#markdown-output")
};

function loadScenarios() {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (!stored) {
    return SAMPLE_SCENARIOS;
  }

  try {
    const parsed = JSON.parse(stored);
    return Array.isArray(parsed) ? parsed : SAMPLE_SCENARIOS;
  } catch {
    return SAMPLE_SCENARIOS;
  }
}

function saveScenarios() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.scenarios));
}

function populateSelect(select, values, includeAll = false) {
  if (includeAll) {
    values = ["all", ...values];
  }

  select.innerHTML = "";
  values.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value === "all" ? select.dataset.allLabel || "All" : value;
    select.appendChild(option);
  });
}

function getFilteredScenarios() {
  const search = state.filters.search.trim().toLowerCase();
  return state.scenarios.filter((scenario) => {
    const searchable = [
      scenario.title,
      scenario.area,
      scenario.type,
      scenario.risk,
      scenario.status,
      scenario.expected,
      scenario.notes,
      ...(scenario.steps || [])
    ].join(" ").toLowerCase();

    return (!search || searchable.includes(search))
      && (state.filters.area === "all" || scenario.area === state.filters.area)
      && (state.filters.status === "all" || scenario.status === state.filters.status)
      && (state.filters.risk === "all" || scenario.risk === state.filters.risk);
  });
}

function renderSummary() {
  elements.total.textContent = state.scenarios.length;
  elements.highRisk.textContent = state.scenarios.filter((scenario) => scenario.risk === "High").length;
  elements.ready.textContent = state.scenarios.filter((scenario) => scenario.status === "Ready for PIE").length;
  elements.blocked.textContent = state.scenarios.filter((scenario) => scenario.status === "Blocked").length;
}

function renderScenarios() {
  const scenarios = getFilteredScenarios();
  elements.list.innerHTML = "";

  if (!scenarios.length) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent = "No scenarios match the current filters.";
    elements.list.appendChild(empty);
    return;
  }

  scenarios.forEach((scenario) => {
    const card = document.createElement("article");
    card.className = "scenario-card";
    card.dataset.risk = scenario.risk;

    const steps = (scenario.steps || []).map((step) => `<li>${escapeHtml(step)}</li>`).join("");
    card.innerHTML = `
      <span class="tag">${escapeHtml(scenario.area)}</span>
      <h3>${escapeHtml(scenario.title)}</h3>
      <p>${escapeHtml(scenario.expected)}</p>
      <div class="meta-row">
        <span class="status-pill">${escapeHtml(scenario.type)}</span>
        <span class="status-pill">Risk: ${escapeHtml(scenario.risk)}</span>
        <span class="status-pill">${escapeHtml(scenario.status)}</span>
      </div>
      <strong>Steps</strong>
      <ol class="steps-list">${steps}</ol>
      <p><strong>Notes:</strong> ${escapeHtml(scenario.notes || "No notes yet.")}</p>
    `;
    elements.list.appendChild(card);
  });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function generateMarkdown() {
  const scenarios = getFilteredScenarios();
  const lines = [
    "# Nyx Test Plan Draft",
    "",
    "This draft was generated from the browser-based Nyx Test Planner.",
    "",
    "Status: Draft planning artifact for human review. This export is not proof that a PIE validation pass has already run.",
    "",
    "## Summary",
    "",
    `- Total scenarios in current view: ${scenarios.length}`,
    `- High-risk scenarios: ${scenarios.filter((scenario) => scenario.risk === "High").length}`,
    `- Ready for PIE: ${scenarios.filter((scenario) => scenario.status === "Ready for PIE").length}`,
    `- Blocked: ${scenarios.filter((scenario) => scenario.status === "Blocked").length}`,
    "",
    "## Scenarios",
    ""
  ];

  scenarios.forEach((scenario, index) => {
    lines.push(`### ${index + 1}. ${scenario.title}`);
    lines.push("");
    lines.push(`- Area: ${scenario.area}`);
    lines.push(`- Type: ${scenario.type}`);
    lines.push(`- Risk: ${scenario.risk}`);
    lines.push(`- Status: ${scenario.status}`);
    lines.push(`- Expected result: ${scenario.expected}`);
    lines.push("- Steps:");
    (scenario.steps || []).forEach((step) => lines.push(`  - ${step}`));
    lines.push(`- Notes: ${scenario.notes || "None yet."}`);
    lines.push("");
  });

  lines.push("## Method / Limitations");
  lines.push("");
  lines.push("- This is a planning aid, not an automated Unreal test runner.");
  lines.push("- Scenarios use public, portfolio-safe Nyx project notes only.");
  lines.push("- Keith reviews and adjusts the plan before treating it as real validation scope.");
  lines.push("- Passing or failing results should be recorded only after a real manual PIE pass.");
  lines.push("");
  lines.push("## What This Does Not Prove");
  lines.push("");
  lines.push("- It does not validate the full Nyx gameplay loop.");
  lines.push("- It does not confirm final UI, art, VFX, audio, tuning, or progression.");
  lines.push("- It does not replace hands-on QA observation, bug notes, screenshots, clips, or follow-up risk review.");

  return lines.join("\n");
}

function addScenario(event) {
  event.preventDefault();
  const scenario = {
    title: elements.title.value.trim(),
    area: elements.area.value,
    type: elements.type.value,
    risk: elements.risk.value,
    status: elements.status.value,
    expected: "Expected result needs Keith review.",
    steps: elements.notes.value
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean),
    notes: "Draft scenario added from the planner form."
  };

  state.scenarios = [scenario, ...state.scenarios];
  saveScenarios();
  elements.form.reset();
  render();
}

function render() {
  renderSummary();
  renderScenarios();
}

function setup() {
  elements.areaFilter.dataset.allLabel = "All areas";
  elements.statusFilter.dataset.allLabel = "All statuses";
  elements.riskFilter.dataset.allLabel = "All risks";

  populateSelect(elements.areaFilter, AREAS, true);
  populateSelect(elements.statusFilter, STATUSES, true);
  populateSelect(elements.riskFilter, RISKS, true);
  populateSelect(elements.area, AREAS);
  populateSelect(elements.type, TYPES);
  populateSelect(elements.risk, RISKS);
  populateSelect(elements.status, STATUSES);

  elements.search.addEventListener("input", (event) => {
    state.filters.search = event.target.value;
    renderScenarios();
  });

  elements.areaFilter.addEventListener("change", (event) => {
    state.filters.area = event.target.value;
    renderScenarios();
  });

  elements.statusFilter.addEventListener("change", (event) => {
    state.filters.status = event.target.value;
    renderScenarios();
  });

  elements.riskFilter.addEventListener("change", (event) => {
    state.filters.risk = event.target.value;
    renderScenarios();
  });

  elements.form.addEventListener("submit", addScenario);

  elements.reset.addEventListener("click", () => {
    state.scenarios = SAMPLE_SCENARIOS;
    saveScenarios();
    render();
  });

  elements.exportButton.addEventListener("click", () => {
    elements.markdown.value = generateMarkdown();
  });

  elements.copyButton.addEventListener("click", async () => {
    if (!elements.markdown.value) {
      elements.markdown.value = generateMarkdown();
    }

    try {
      await navigator.clipboard.writeText(elements.markdown.value);
      elements.copyButton.textContent = "Copied";
      setTimeout(() => {
        elements.copyButton.textContent = "Copy Markdown";
      }, 1400);
    } catch {
      elements.markdown.focus();
      elements.markdown.select();
    }
  });

  render();
}

setup();

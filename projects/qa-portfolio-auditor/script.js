const FORBIDDEN_PHRASES = [
  "live Unreal automation",
  "Unreal plugin",
  "production-ready",
  "real studio telemetry",
  "private studio data",
  "real Jira integration",
  "automated engine validation",
  "replaces Tech Art review",
  "AI detects visual quality",
  "production pipeline integration"
];

const PORTFOLIO_TOOLS = [
  {
    name: "QA Bug Report Tool",
    category: "QA tooling / Python CLI",
    statusLabel: "First version",
    demoLink: "projects/qa-bug-report-tool/README.md",
    docsLink: "projects/qa-bug-report-tool/README.md",
    sampleOutput: "projects/qa-bug-report-tool/reports/001-inventory-count.md",
    oneLiner: "Converts rough QA notes into structured Markdown and JSON bug reports.",
    evidenceFocus: "Bug writing, repro quality, severity/priority thinking, pytest-backed validation, Markdown export.",
    disclaimer: "Portfolio-safe sample notes only; human-reviewed output and known limitations are documented.",
    requiredPhrases: ["portfolio-safe", "human-reviewed", "Markdown export"],
    requiredArtifacts: ["README", "sample-data", "reports", "tests", "pyproject.toml"],
    knownLimitations: "Practice QA CLI, not a production bug tracker or replacement for human triage.",
    claimsToAudit: "Structured Markdown and JSON bug report export with pytest coverage."
  },
  {
    name: "Nyx Test Planner",
    category: "QA planning / browser prototype",
    statusLabel: "Live planning prototype",
    demoLink: "docs/nyx-test-planner.html",
    docsLink: "projects/nyx-test-planner/README.md",
    sampleOutput: "docs/nyx-test-planner-case-study.md",
    oneLiner: "Turns early Nyx gameplay ideas into human-reviewed test scenarios, risk notes, status tracking, and Markdown test-plan exports.",
    evidenceFocus: "QA planning judgment, risk/status tracking, expected results, Markdown export, and planned PIE validation notes.",
    disclaimer: "Portfolio-safe browser prototype; does not connect to Unreal, Jira, private tools, studio data, or automated test runners.",
    requiredPhrases: ["portfolio-safe", "human-reviewed", "Markdown export"],
    requiredArtifacts: ["live planner page", "README", "case study", "Markdown export"],
    knownLimitations: "Planning aid only; manual PIE/prototype validation remains pending until actually run.",
    claimsToAudit: "Browser-based planning prototype with Markdown test-plan export."
  },
  {
    name: "Art Telemetry QA",
    category: "Art QA / Technical QA Python CLI",
    statusLabel: "MVP prototype",
    demoLink: "projects/art-telemetry-qa/README.md",
    docsLink: "projects/art-telemetry-qa/README.md",
    sampleOutput: "docs/art-qa-telemetry-report-showcase.md",
    oneLiner: "Parses mock Unreal-style telemetry into Art QA risk summaries, owner-routing notes, regression notes, and Jira-ready reports.",
    evidenceFocus: "Mock Unreal-style telemetry, Art QA evidence, risk summaries, owner routing, and Jira-ready reports.",
    disclaimer: "Uses mock data only for human-reviewed reports; not an Unreal plugin, not live Unreal automation, not real studio telemetry, and not Jira automation.",
    requiredPhrases: ["mock data", "mock Unreal-style telemetry", "human-reviewed", "Jira-ready reports", "risk summaries"],
    requiredArtifacts: ["README", "sample data", "reports", "tests", "report showcase"],
    knownLimitations: "Does not replace Tech Art, Performance, Engineering, or human QA judgment.",
    claimsToAudit: "Mock telemetry parsing and Jira-ready report drafting for human-reviewed Art QA evidence."
  },
  {
    name: "Community Pulse",
    category: "Community QA / Python CLI",
    statusLabel: "First version",
    demoLink: "projects/community-pulse-report-tool/README.md",
    docsLink: "projects/community-pulse-report-tool/README.md",
    sampleOutput: "projects/community-pulse-report-tool/reports/weekly-sentiment-report.md",
    oneLiner: "Turns mock player/playtest feedback into structured theme summaries, risk notes, and human-reviewed QA follow-up reports.",
    evidenceFocus: "Mock feedback grouping, repeated themes, readiness summary, risk notes, and Markdown export.",
    disclaimer: "Uses fictional sample feedback only and does not connect to private player data, forums, APIs, or internal tools.",
    requiredPhrases: ["mock", "human-reviewed", "risk notes", "Markdown export"],
    requiredArtifacts: ["README", "sample CSV", "report output", "tests"],
    knownLimitations: "Draft aid for human review, not a live social listening platform or automated community decision-maker.",
    claimsToAudit: "Mock feedback summarization and Markdown report export."
  },
  {
    name: "External QA Handoff Manager",
    category: "QA leadership / browser prototype",
    statusLabel: "First working version",
    demoLink: "docs/external-qa-handoff-manager.html",
    docsLink: "projects/external-qa-handoff-manager/README.md",
    sampleOutput: "Generated Markdown handoff draft",
    oneLiner: "Turns feature goals into outsource-ready test packets with scenario coverage, bug-quality standards, evidence requirements, intake review, and Markdown handoff exports.",
    evidenceFocus: "External QA coordination, evidence requirements, intake checklist, scenario coverage, and Markdown export.",
    disclaimer: "Mock data only for human-reviewed external QA coordination; does not connect to Jira, vendor portals, private studio workflows, internal test plans, or live production data.",
    requiredPhrases: ["mock data", "external QA coordination", "human-reviewed", "Markdown export"],
    requiredArtifacts: ["README", "browser prototype", "scenario matrix", "bug standards", "Markdown export"],
    knownLimitations: "Static MVP with hard-coded sample data and no live vendor/Jira integration.",
    claimsToAudit: "External QA handoff planning with human-reviewed Markdown export."
  }
];

const FORBIDDEN_SELF_CHECK_TEXT = "This fixture proves the checker can flag live Unreal automation and production-ready wording.";

function normalize(text) {
  return String(text || "").toLowerCase();
}

function includesPhrase(text, phrase) {
  return normalize(text).includes(normalize(phrase));
}

function findForbiddenClaims(text) {
  return FORBIDDEN_PHRASES.filter((phrase) => includesPhrase(text, phrase));
}

function findMissingSafeLanguage(tool) {
  const searchable = [
    tool.oneLiner,
    tool.evidenceFocus,
    tool.disclaimer,
    tool.knownLimitations
  ].join(" ");

  return tool.requiredPhrases.filter((phrase) => !includesPhrase(searchable, phrase));
}

function auditTool(tool) {
  const passedChecks = [];
  const missingItems = [];

  function requireCheck(condition, passLabel, missingLabel) {
    if (condition) {
      passedChecks.push(passLabel);
    } else {
      missingItems.push(missingLabel);
    }
  }

  requireCheck(Boolean(tool.oneLiner), "Has recruiter-readable one-liner", "Missing one-liner");
  requireCheck(Boolean(tool.statusLabel), "Has status label", "Missing status label");
  requireCheck(Boolean(tool.demoLink || tool.sampleOutput), "Has demo link or sample output", "Missing demo link or sample output");
  requireCheck(Boolean(tool.docsLink), "Has README/docs link", "Missing README/docs link");
  requireCheck(Boolean(tool.disclaimer), "Has portfolio-safe disclaimer", "Missing portfolio-safe disclaimer");
  requireCheck(Boolean(tool.evidenceFocus), "Has evidence focus", "Missing evidence focus");
  requireCheck(Boolean(tool.knownLimitations), "Has known limitations or safe boundary", "Missing known limitations or safe boundary");

  const missingSafeLanguage = findMissingSafeLanguage(tool);
  missingSafeLanguage.forEach((phrase) => missingItems.push(`Missing encouraged safe phrase: ${phrase}`));

  const overclaimRisks = findForbiddenClaims(tool.claimsToAudit || "");

  let overallStatus = "Pass";
  if (overclaimRisks.length > 0 || !tool.docsLink || !(tool.demoLink || tool.sampleOutput)) {
    overallStatus = "Needs Review";
  } else if (missingItems.length > 0) {
    overallStatus = "Pass with Notes";
  }

  const recommendedNextAction = getRecommendedNextAction(tool, overallStatus, missingItems, overclaimRisks);

  return {
    ...tool,
    overallStatus,
    passedChecks,
    missingItems,
    overclaimRisks,
    recommendedNextAction
  };
}

function getRecommendedNextAction(tool, overallStatus, missingItems, overclaimRisks) {
  if (overclaimRisks.length > 0) {
    return `Remove or reframe overclaim language before publishing: ${overclaimRisks.join(", ")}.`;
  }

  if (missingItems.length > 0) {
    return `Tighten ${tool.name} by addressing: ${missingItems.slice(0, 2).join("; ")}.`;
  }

  if (overallStatus === "Pass") {
    return "Keep current positioning; recheck links and claims before the next live publish.";
  }

  return "Review manually before publishing.";
}

function auditPortfolio() {
  return PORTFOLIO_TOOLS.map(auditTool);
}

function createSummaryCard(value, label) {
  const article = document.createElement("article");
  article.className = "summary-card";

  const strong = document.createElement("strong");
  strong.textContent = value;

  const span = document.createElement("span");
  span.textContent = label;

  article.append(strong, span);
  return article;
}

function renderSummary(audits) {
  const summary = document.querySelector("#summary-grid");
  summary.innerHTML = "";

  const passCount = audits.filter((tool) => tool.overallStatus === "Pass").length;
  const notesCount = audits.filter((tool) => tool.overallStatus === "Pass with Notes").length;
  const reviewCount = audits.filter((tool) => tool.overallStatus === "Needs Review").length;
  const selfCheckPassed = findForbiddenClaims(FORBIDDEN_SELF_CHECK_TEXT).length >= 2;

  summary.append(
    createSummaryCard(audits.length, "Tools audited"),
    createSummaryCard(passCount, "Pass"),
    createSummaryCard(notesCount, "Pass with notes"),
    createSummaryCard(reviewCount, "Needs review")
  );

  if (selfCheckPassed) {
    summary.append(createSummaryCard("Pass", "Forbidden phrase self-check"));
  }
}

function renderToolCards(audits) {
  const grid = document.querySelector("#tool-grid");
  grid.innerHTML = "";

  audits.forEach((tool) => {
    const article = document.createElement("article");
    article.className = "tool-card";
    article.dataset.status = tool.overallStatus;

    const statusClass = tool.overallStatus === "Pass"
      ? "pass"
      : tool.overallStatus === "Pass with Notes"
        ? "notes"
        : "review";

    const statusRow = document.createElement("div");
    statusRow.className = "status-row";
    statusRow.innerHTML = `
      <span class="status-pill ${statusClass}">${tool.overallStatus}</span>
      <span class="tag">${tool.statusLabel || "No status"}</span>
    `;

    const heading = document.createElement("h3");
    heading.textContent = tool.name;

    const oneLiner = document.createElement("p");
    oneLiner.textContent = tool.oneLiner || "No one-liner provided.";

    const metrics = document.createElement("ul");
    metrics.className = "metric-list";
    metrics.innerHTML = `
      <li><strong>Demo readiness:</strong> ${tool.demoLink || tool.sampleOutput ? "Ready for review" : "Missing demo/sample output"}</li>
      <li><strong>Documentation readiness:</strong> ${tool.docsLink ? "README/docs linked" : "Missing docs link"}</li>
      <li><strong>Recruiter clarity:</strong> ${tool.oneLiner && tool.evidenceFocus ? "Clear" : "Needs wording"}</li>
      <li><strong>Portfolio-safe disclaimer:</strong> ${tool.disclaimer ? "Present" : "Missing"}</li>
      <li><strong>Overclaim risk:</strong> ${tool.overclaimRisks.length ? tool.overclaimRisks.join(", ") : "No forbidden claims found in audited claim text"}</li>
      <li><strong>Evidence completeness:</strong> ${tool.requiredArtifacts.join(", ")}</li>
    `;

    const missing = document.createElement("ul");
    missing.className = "missing-list";
    const missingText = tool.missingItems.length
      ? tool.missingItems.map((item) => `<li><strong>Missing:</strong> ${item}</li>`).join("")
      : "<li>No missing required items from metadata checks.</li>";
    missing.innerHTML = `${missingText}<li><strong>Next action:</strong> ${tool.recommendedNextAction}</li>`;

    article.append(statusRow, heading, oneLiner, metrics, missing);
    grid.append(article);
  });
}

function buildMarkdownReport(audits) {
  const passCount = audits.filter((tool) => tool.overallStatus === "Pass").length;
  const notesCount = audits.filter((tool) => tool.overallStatus === "Pass with Notes").length;
  const reviewCount = audits.filter((tool) => tool.overallStatus === "Needs Review").length;

  const lines = [
    "# Portfolio Tool Audit Summary",
    "",
    "> Portfolio-safe QA self-audit generated from sample metadata. This does not replace manual review.",
    "",
    "## Summary",
    "",
    `- Tools audited: ${audits.length}`,
    `- Pass: ${passCount}`,
    `- Pass with Notes: ${notesCount}`,
    `- Needs Review: ${reviewCount}`,
    "- Scope: demo readiness, documentation coverage, recruiter-safe wording, evidence completeness, and overclaim risk.",
    "",
    "## Tool-by-tool Status",
    ""
  ];

  audits.forEach((tool) => {
    lines.push(`### ${tool.name}`);
    lines.push(`- Overall status: ${tool.overallStatus}`);
    lines.push(`- Category: ${tool.category}`);
    lines.push(`- Status label: ${tool.statusLabel || "Missing"}`);
    lines.push(`- Evidence focus: ${tool.evidenceFocus || "Missing"}`);
    lines.push(`- Demo/sample output: ${tool.demoLink || tool.sampleOutput || "Missing"}`);
    lines.push(`- README/docs: ${tool.docsLink || "Missing"}`);
    lines.push(`- Passed checks: ${tool.passedChecks.join("; ") || "None"}`);
    lines.push(`- Missing items: ${tool.missingItems.join("; ") || "None"}`);
    lines.push(`- Overclaim risks: ${tool.overclaimRisks.join("; ") || "None found in audited claim text"}`);
    lines.push(`- Recommended next action: ${tool.recommendedNextAction}`);
    lines.push("");
  });

  lines.push("## Final Recruiter-Readiness Summary", "");
  if (reviewCount === 0) {
    lines.push("The audited portfolio tools are reviewable as portfolio-safe QA artifacts, with human review still required before publishing.");
  } else {
    lines.push("One or more tools need wording or evidence cleanup before being used as a recruiter-facing proof point.");
  }
  lines.push("");
  lines.push("## Safety Boundary");
  lines.push("");
  lines.push("This audit does not use private studio data, does not perform full browser automation, does not connect to Unreal or Jira, and does not claim perfect validation.");

  return lines.join("\n");
}

function generateMarkdownReport(audits) {
  document.querySelector("#markdown-output").value = buildMarkdownReport(audits);
}

async function copyMarkdownReport(audits) {
  const output = document.querySelector("#markdown-output");
  if (!output.value) {
    generateMarkdownReport(audits);
  }

  output.select();

  if (navigator.clipboard) {
    await navigator.clipboard.writeText(output.value);
  } else {
    document.execCommand("copy");
  }
}

function init() {
  const audits = auditPortfolio();
  renderSummary(audits);
  renderToolCards(audits);
  generateMarkdownReport(audits);

  document.querySelector("#export-report").addEventListener("click", () => generateMarkdownReport(audits));
  document.querySelector("#copy-report").addEventListener("click", () => copyMarkdownReport(audits));
}

init();

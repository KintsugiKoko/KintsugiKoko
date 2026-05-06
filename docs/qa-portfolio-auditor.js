const forbiddenClaims = [
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

const encouragedLanguage = [
  "portfolio-safe",
  "mock data",
  "mock Unreal-style telemetry",
  "human-reviewed",
  "Markdown export",
  "Jira-ready reports",
  "risk summaries",
  "evidence packs",
  "external QA coordination"
];

const portfolioTools = [
  {
    name: "QA Bug Report Tool",
    category: "QA reporting CLI",
    demoLink: "",
    sampleOutput: "https://github.com/KintsugiKoko/KintsugiKoko/tree/master/projects/qa-bug-report-tool/reports",
    docsLink: "https://github.com/KintsugiKoko/KintsugiKoko/blob/master/projects/qa-bug-report-tool/README.md",
    oneLiner: "Turns rough QA notes into structured Markdown bug reports with repro steps, severity, priority, and expected vs. actual behavior.",
    statusLabel: "First version",
    evidenceFocus: "Bug quality, repro clarity, severity framing, Markdown output, pytest coverage",
    requiredPhrases: ["Markdown", "repro", "severity"],
    forbiddenPhrases: forbiddenClaims,
    requiredArtifacts: ["README", "sample data", "tests", "example output", "known limitations"],
    presentArtifacts: ["README", "sample data", "tests", "example output", "known limitations"],
    knownLimitations: "Local CLI prototype; human review still required.",
    safeLanguage: "portfolio-safe sample data, human-reviewed Markdown output"
  },
  {
    name: "Nyx Test Planner",
    category: "Browser QA planning prototype",
    demoLink: "https://kintsugikoko.github.io/KintsugiKoko/nyx-test-planner.html",
    sampleOutput: "",
    docsLink: "https://github.com/KintsugiKoko/KintsugiKoko/blob/master/projects/nyx-test-planner/README.md",
    oneLiner: "Turns early Nyx gameplay ideas into human-reviewed test scenarios, risk notes, status tracking, and Markdown test-plan exports.",
    statusLabel: "Live planning prototype",
    evidenceFocus: "QA planning, risk notes, scenario coverage, Markdown export",
    requiredPhrases: ["human-reviewed", "Markdown", "risk"],
    forbiddenPhrases: forbiddenClaims,
    requiredArtifacts: ["README", "live demo", "known limitations", "Markdown export"],
    presentArtifacts: ["README", "live demo", "known limitations", "Markdown export"],
    knownLimitations: "Browser planning board; does not run automated Unreal tests.",
    safeLanguage: "human-reviewed planning prototype, no automated Unreal testing claim"
  },
  {
    name: "Art Telemetry QA",
    category: "Technical QA / Art QA tool",
    demoLink: "",
    sampleOutput: "https://github.com/KintsugiKoko/KintsugiKoko/tree/master/projects/art-telemetry-qa/reports",
    docsLink: "https://github.com/KintsugiKoko/KintsugiKoko/blob/master/projects/art-telemetry-qa/README.md",
    oneLiner: "Parses mock Unreal-style art validation data into risk summaries, owner-routing notes, and Jira-ready reports for human-reviewed Art QA / Technical QA evidence work.",
    statusLabel: "MVP prototype",
    evidenceFocus: "Mock telemetry parsing, risk scoring, owner routing, Jira-ready reports",
    requiredPhrases: ["mock Unreal-style telemetry", "human-reviewed", "risk summaries", "Jira-ready reports"],
    forbiddenPhrases: forbiddenClaims,
    requiredArtifacts: ["README", "sample data", "tests", "sample output", "known limitations"],
    presentArtifacts: ["README", "sample data", "tests", "sample output", "known limitations"],
    knownLimitations: "No live Unreal integration; mock data only.",
    safeLanguage: "portfolio-safe mock Unreal-style telemetry and human-reviewed reports"
  },
  {
    name: "Community Pulse",
    category: "Community reporting CLI",
    demoLink: "",
    sampleOutput: "https://github.com/KintsugiKoko/KintsugiKoko/blob/master/projects/community-pulse-report-tool/reports/weekly-sentiment-report.md",
    docsLink: "https://github.com/KintsugiKoko/KintsugiKoko/blob/master/projects/community-pulse-report-tool/README.md",
    oneLiner: "Turns fictional community feedback CSVs into weekly sentiment reports with repeated themes, risk notes, and human follow-up items.",
    statusLabel: "First version",
    evidenceFocus: "CSV parsing, theme grouping, community reporting, human follow-up notes",
    requiredPhrases: ["fictional", "human", "report"],
    forbiddenPhrases: forbiddenClaims,
    requiredArtifacts: ["README", "sample data", "tests", "sample output", "known limitations"],
    presentArtifacts: ["README", "sample data", "tests", "sample output", "known limitations"],
    knownLimitations: "Uses fictional sample data only.",
    safeLanguage: "fictional sample data and human follow-up notes"
  },
  {
    name: "External QA Handoff Manager",
    category: "QA leadership browser prototype",
    demoLink: "https://kintsugikoko.github.io/KintsugiKoko/external-qa-handoff-manager.html",
    sampleOutput: "https://github.com/KintsugiKoko/KintsugiKoko/tree/master/projects/external-qa-handoff-manager/reports",
    docsLink: "https://github.com/KintsugiKoko/KintsugiKoko/blob/master/projects/external-qa-handoff-manager/README.md",
    oneLiner: "Turns feature goals into outsource-ready QA packets and lets reviewers live-demo external QA intake through mock bug cards, evidence checks, and Markdown summary exports.",
    statusLabel: "Portfolio-safe prototype",
    evidenceFocus: "External QA coordination, bug-quality standards, intake review, QA leadership",
    requiredPhrases: ["portfolio-safe", "mock", "Markdown", "external QA coordination"],
    forbiddenPhrases: forbiddenClaims,
    requiredArtifacts: ["README", "live demo", "sample data", "docs", "sample output", "known limitations"],
    presentArtifacts: ["README", "live demo", "sample data", "docs", "sample output", "known limitations"],
    knownLimitations: "No Jira integration, no private workflow, no production pipeline claim.",
    safeLanguage: "portfolio-safe mock workflow with clear Jira and pipeline boundary language"
  },
  {
    name: "QA Capture Review Board",
    category: "Watchlist / not present on current branch",
    demoLink: "",
    sampleOutput: "",
    docsLink: "",
    oneLiner: "",
    statusLabel: "Not present",
    evidenceFocus: "Planned capture review evidence packs, if added later",
    requiredPhrases: ["portfolio-safe", "mock data", "human-reviewed"],
    forbiddenPhrases: forbiddenClaims,
    requiredArtifacts: ["README", "sample data", "docs", "sample output", "known limitations"],
    presentArtifacts: [],
    knownLimitations: "",
    safeLanguage: "Watchlist entry only. If added later, it must avoid phrases like AI detects visual quality or production pipeline integration."
  }
];

function $(id) {
  return document.getElementById(id);
}

function includesText(haystack, needle) {
  return haystack.toLowerCase().includes(needle.toLowerCase());
}

function auditTool(tool) {
  const auditText = [
    tool.oneLiner,
    tool.statusLabel,
    tool.evidenceFocus,
    tool.knownLimitations,
    tool.safeLanguage
  ].join(" ");

  const checks = [
    ["Has one-liner", Boolean(tool.oneLiner)],
    ["Has status label", Boolean(tool.statusLabel)],
    ["Has demo link or sample output", Boolean(tool.demoLink || tool.sampleOutput)],
    ["Has README/docs link", Boolean(tool.docsLink)],
    ["Has portfolio-safe disclaimer", includesText(auditText, "portfolio-safe") || includesText(auditText, "mock") || includesText(auditText, "fictional")],
    ["Has evidence focus", Boolean(tool.evidenceFocus)],
    ["Has known limitations or safe boundary language", Boolean(tool.knownLimitations || tool.safeLanguage)],
    ["Avoids forbidden claims", forbiddenClaims.every((claim) => !includesText(auditText, claim))]
  ];

  const missingArtifacts = tool.requiredArtifacts.filter((artifact) => !tool.presentArtifacts.includes(artifact));
  const forbiddenHits = forbiddenClaims.filter((claim) => includesText(auditText, claim));
  const missingRequiredPhrases = tool.requiredPhrases.filter((phrase) => !includesText(auditText, phrase));
  const failedChecks = checks.filter(([, passed]) => !passed).map(([label]) => label);
  const missingItems = [...failedChecks, ...missingArtifacts.map((item) => `Missing artifact: ${item}`), ...missingRequiredPhrases.map((item) => `Missing phrase signal: ${item}`)];

  let status = "Pass";
  if (forbiddenHits.length || failedChecks.length >= 2 || missingArtifacts.length >= 2 || !tool.oneLiner) {
    status = "Needs Review";
  } else if (missingItems.length || missingRequiredPhrases.length) {
    status = "Pass with Notes";
  }

  const recommendedNextAction = status === "Pass"
    ? "Keep current positioning and re-check after the next public update."
    : status === "Pass with Notes"
      ? "Add the missing phrase or artifact signal before the next recruiter pass."
      : "Fix missing review basics or overclaim risk before publishing this as a proof project.";

  return {
    ...tool,
    checks,
    missingItems,
    forbiddenHits,
    status,
    recommendedNextAction
  };
}

function statusClass(value) {
  if (value === "Pass") return "ok";
  if (value === "Pass with Notes") return "note";
  return "risk";
}

function renderCards() {
  const filter = $("status-filter").value;
  const audits = portfolioTools.map(auditTool);
  const filtered = filter === "all" ? audits : audits.filter((audit) => audit.status === filter);

  $("audit-grid").innerHTML = filtered.map((audit) => `
    <article class="audit-card" data-status="${audit.status}">
      <span class="status-pill">${audit.status}</span>
      <h3>${audit.name}</h3>
      <p class="audit-meta">${audit.category} / ${audit.statusLabel || "No status label"}</p>
      <p>${audit.oneLiner || "No one-liner yet."}</p>
      <div class="check-list">
        ${audit.checks.map(([label, passed]) => `
          <div class="check-row"><span>${label}</span><strong class="${passed ? "ok" : "risk"}">${passed ? "Pass" : "Flag"}</strong></div>
        `).join("")}
        <div class="check-row"><span>Evidence completeness</span><strong class="${audit.missingItems.length ? "note" : "ok"}">${audit.missingItems.length ? "Notes" : "Pass"}</strong></div>
      </div>
      <p><strong>Evidence focus:</strong> ${audit.evidenceFocus || "Missing"}</p>
      <p><strong>Missing items:</strong> ${audit.missingItems.length ? audit.missingItems.join("; ") : "None"}</p>
      <p><strong>Overclaim risks:</strong> ${audit.forbiddenHits.length ? audit.forbiddenHits.join("; ") : "None detected"}</p>
      <p><strong>Recommended next action:</strong> ${audit.recommendedNextAction}</p>
      <div class="tag-list">
        ${audit.presentArtifacts.map((artifact) => `<span class="tag">${artifact}</span>`).join("")}
      </div>
      <div class="card-links">
        ${audit.demoLink ? `<a href="${audit.demoLink}">Demo</a>` : ""}
        ${audit.sampleOutput ? `<a href="${audit.sampleOutput}">Sample output</a>` : ""}
        ${audit.docsLink ? `<a href="${audit.docsLink}">README / docs</a>` : ""}
      </div>
    </article>
  `).join("");

  updateSummary(audits);
  $("audit-report").value = generateMarkdown(audits);
}

function updateSummary(audits) {
  $("tool-count").textContent = audits.length;
  $("pass-count").textContent = audits.filter((audit) => audit.status === "Pass").length;
  $("notes-count").textContent = audits.filter((audit) => audit.status === "Pass with Notes").length;
  $("review-count").textContent = audits.filter((audit) => audit.status === "Needs Review").length;
}

function generateMarkdown(audits) {
  const rows = audits.map((audit) => `| ${audit.name} | ${audit.status} | ${audit.missingItems.length ? audit.missingItems.join("; ") : "None"} | ${audit.forbiddenHits.length ? audit.forbiddenHits.join("; ") : "None detected"} | ${audit.recommendedNextAction} |`).join("\n");
  const passCount = audits.filter((audit) => audit.status === "Pass").length;
  const notesCount = audits.filter((audit) => audit.status === "Pass with Notes").length;
  const reviewCount = audits.filter((audit) => audit.status === "Needs Review").length;

  return `# Portfolio Tool Audit Summary

## Summary

- Tools audited: ${audits.length}
- Pass: ${passCount}
- Pass with Notes: ${notesCount}
- Needs Review: ${reviewCount}

## Tool-by-Tool Status

| Tool | Status | Missing Items | Overclaim Risks | Recommended Next Action |
| --- | --- | --- | --- | --- |
${rows}

## Passed Checks

- One-liner presence
- Status label presence
- Demo link or sample output presence
- README/docs link presence
- Portfolio-safe disclaimer signal
- Evidence focus signal
- Known limitations or safe boundary language
- Forbidden claim scan

## Overclaim Risks Checked

${forbiddenClaims.map((claim) => `- ${claim}`).join("\n")}

## Final Recruiter-Readiness Summary

This report is a portfolio-safe metadata audit. It helps identify whether the project work is easy to inspect, clearly framed, supported by evidence, and protected from inflated claims. It does not replace manual review and does not perform full browser automation.
`;
}

function copyReport() {
  const node = $("audit-report");
  node.select();
  if (navigator.clipboard) {
    navigator.clipboard.writeText(node.value).catch(() => document.execCommand("copy"));
  } else {
    document.execCommand("copy");
  }
}

function downloadReport() {
  const blob = new Blob([$("audit-report").value], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "qa-portfolio-audit-summary.md";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

$("status-filter").addEventListener("change", renderCards);
$("copy-report").addEventListener("click", copyReport);
$("download-report").addEventListener("click", downloadReport);

renderCards();

const fs = require("fs");
const path = require("path");

const repoRoot = path.resolve(__dirname, "..");
const metadataPath = path.join(repoRoot, "projects", "qa-portfolio-auditor", "samples", "portfolio_tools_sample.json");
const reportPath = path.join(repoRoot, "projects", "qa-portfolio-auditor", "reports", "local-artifact-check.md");

function normalizeStatus(status) {
  return ["Present", "Missing", "Needs Review"].includes(status) ? status : "Needs Review";
}

function readMetadata() {
  const raw = fs.readFileSync(metadataPath, "utf8");
  const parsed = JSON.parse(raw);
  return Array.isArray(parsed) ? parsed : parsed.tools;
}

function auditArtifact(tool, artifact) {
  const artifactPath = artifact.path || "";
  const absolutePath = path.join(repoRoot, artifactPath);
  const actualExists = artifactPath ? fs.existsSync(absolutePath) : false;
  const metadataStatus = normalizeStatus(artifact.status);
  const actualStatus = actualExists ? "Present" : "Missing";
  const statusMatchesMetadata = metadataStatus === actualStatus;

  return {
    toolName: tool.name,
    label: artifact.label || "Unnamed artifact",
    type: artifact.type || "unspecified",
    path: artifactPath || "Missing path",
    metadataStatus,
    actualStatus,
    statusMatchesMetadata,
    recommendedAction: artifact.recommended_action || artifact.recommendedAction || "Review this artifact before publishing."
  };
}

function buildReport(results) {
  const presentCount = results.filter((item) => item.actualStatus === "Present").length;
  const missingCount = results.filter((item) => item.actualStatus === "Missing").length;
  const mismatchCount = results.filter((item) => !item.statusMatchesMetadata).length;

  const lines = [
    "# QA Portfolio Auditor Local Artifact Check",
    "",
    "> Local filesystem check for portfolio-safe sample metadata. This does not crawl the live site, validate deployment health, connect to Jira, connect to Unreal, or replace manual review.",
    "",
    "## Summary",
    "",
    `- Artifacts checked: ${results.length}`,
    `- Present: ${presentCount}`,
    `- Missing: ${missingCount}`,
    `- Metadata mismatches: ${mismatchCount}`,
    "",
    "## Results",
    ""
  ];

  results.forEach((item) => {
    lines.push(`### ${item.toolName} - ${item.label}`);
    lines.push(`- Type: ${item.type}`);
    lines.push(`- Path: ${item.path}`);
    lines.push(`- Metadata status: ${item.metadataStatus}`);
    lines.push(`- Local filesystem status: ${item.actualStatus}`);
    lines.push(`- Status matches metadata: ${item.statusMatchesMetadata ? "Yes" : "No"}`);
    lines.push(`- Recommended action: ${item.recommendedAction}`);
    lines.push("");
  });

  lines.push("## Limitations");
  lines.push("");
  lines.push("- Checks local repository paths only.");
  lines.push("- Does not crawl the live site.");
  lines.push("- Does not validate external deployment health.");
  lines.push("- Does not inspect the quality or accuracy of the artifact content.");
  lines.push("- Human review is still required before publishing.");
  lines.push("");

  return lines.join("\n");
}

function main() {
  const tools = readMetadata();
  const results = tools.flatMap((tool) => (tool.expected_artifacts || []).map((artifact) => auditArtifact(tool, artifact)));
  const report = buildReport(results);

  fs.mkdirSync(path.dirname(reportPath), { recursive: true });
  fs.writeFileSync(reportPath, report, "utf8");

  const missingCount = results.filter((item) => item.actualStatus === "Missing").length;
  const mismatchCount = results.filter((item) => !item.statusMatchesMetadata).length;
  console.log(`Checked ${results.length} artifacts. Missing: ${missingCount}. Metadata mismatches: ${mismatchCount}.`);
  console.log(`Report written to ${path.relative(repoRoot, reportPath)}`);
}

main();

# Sample Output

Run:

```bash
python -m art_telemetry_qa.cli scan --input samples --output reports
```

Expected generated files:

- `reports/art_qa_summary.md`
- `reports/art_qa_failures.csv`
- `reports/jira_ready_bugs.md`

Example summary excerpt:

```markdown
# Art QA Telemetry Summary

## Executive Summary

- Assets scanned: **6**
- Findings generated: **25**
- Total risk points: **115**
- This report supports human Art QA / Technical QA review; it is not final Tech Art, Performance, or Engineering sign-off.
```

Example Jira-ready draft heading:

```markdown
## 1. [Critical] VFX_Starwell_Offering_Burst - Soak test warning spike
```

The exact counts may change as rules evolve. The important behavior is that the tool generates readable, human-reviewed report drafts from mock telemetry.

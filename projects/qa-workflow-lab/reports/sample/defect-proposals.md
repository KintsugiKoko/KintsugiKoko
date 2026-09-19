# Defect Proposals

Local drafts for QA review.

## Repeated upgrade request changes authoritative power twice

Source: BUG-1 | Build: demo-102
Severity suggestion: Critical | Status: draft_ready

### Reproduction

1. Start with power 10.
2. Apply upgrade request upgrade-7.
3. Retry the same request after acknowledgement.

Expected: Power remains 15 after duplicate delivery.

Actual: Power reaches 20 in the failing fixture.

Evidence: TRACE-1
Possible related reports: BUG-2
Missing: None in the structured field check

Fix verification: pending QA review and execution.

## Upgrade icon briefly duplicates after recovery

Source: BUG-2 | Build: demo-102
Severity suggestion: High | Status: draft_ready

### Reproduction

1. Recover after an accepted upgrade.

Expected: One current icon.

Actual: Two icons are described in a fictional report; authoritative state is unknown.

Evidence: ART-3-PC
Possible related reports: BUG-1
Missing: None in the structured field check

Fix verification: pending QA review and execution.

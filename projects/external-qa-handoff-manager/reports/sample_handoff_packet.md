# External QA Handoff: Nyx Starwell Offering First Pass

## Handoff Context

- Build/context: Portfolio sample build / mock handoff packet
- Owner: QA lead review
- Goal: Validate that an offsite QA tester can understand the feature goal, run the right scenario checks, capture useful evidence, and send back Jira-ready bug reports for human review.
- Safety note: Mock data only. This sample does not connect to Jira, vendor portals, private studio workflows, internal test plans, outsourcing systems, or live production data.

## Scenario Matrix

### First successful offering updates progress once

- Area: Core loop
- Risk: High
- Status: Ready for handoff
- Expected result: Offering one valid fish consumes one item, advances Starwell progress once, and shows readable feedback.
- Evidence needed: Short clip from offer action through progress update, plus screenshot of inventory after the action.

### Invalid offering is rejected with clear messaging

- Area: Error handling
- Risk: Medium
- Status: Ready for handoff
- Expected result: An invalid item is not consumed and the player receives a readable reason the offering failed.
- Evidence needed: Screenshot of message state and notes on input/item used.

### Progress threshold does not double-fire reward

- Area: Regression
- Risk: High
- Status: Needs setup
- Expected result: Reaching the threshold grants the reward one time and does not repeat after menu reopen or level reload.
- Evidence needed: Clip showing threshold reach, reward state, menu reopen, and follow-up check.

### Placeholder content is labeled clearly

- Area: Presentation
- Risk: Low
- Status: Ready for handoff
- Expected result: Any temporary art, text, or tuning value is readable and does not imply final content.
- Evidence needed: Screenshot of placeholder-facing UI or environment state.

## Bug-Quality Standards

- Clear title with feature area and player-facing impact
- Build, branch, platform/config, and test account/setup notes
- Repeatable steps with expected result and actual result
- Severity, priority suggestion, repro rate, and regression risk
- Screenshot or short clip with timestamp when visual behavior matters
- Follow-up note when the issue may need design, art, engineering, or QA owner review

## Evidence Requirements

- Screenshot or short clip for each failed or unclear scenario
- Notes on the exact sample build/prototype version used
- Pass/fail/blocked status for each scenario
- One concise risk summary for QA lead intake
- Separate follow-up note for tuning feedback versus functional defects

## QA Lead Intake Checklist

- [ ] Confirm the tester used the intended build and setup notes
- [ ] Check whether the reported issue has enough repro detail
- [ ] Separate valid bugs from tuning feedback and unclear observations
- [ ] Route likely ownership without pretending the export filed a Jira ticket
- [ ] Record any missing evidence before calling the pass complete

## Portfolio-Safe Boundary

This is a human-reviewed external QA planning artifact using mock data. It does not connect to Jira, vendor portals, private studio workflows, internal test plans, outsourcing systems, or live production data.

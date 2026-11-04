# Worked proposal: a prospective follow-up experiment

This is a proposed experiment, rather than a campaign that ran. It sets out how a future owner could test a follow-up protocol. The historical comparison helps form the question, but cannot supply the treatment effect.

## Decision and population

Would one standardized additional follow-up after an unsuccessful first contact improve 30-day subscription outcomes enough to justify the additional workload?

For this worked scenario, a future campaign owner defines an eligible population of clients with one documented unsuccessful first contact, a valid contact permission and no do-not-contact restriction. Already subscribed or ineligible clients are excluded before randomization. A real campaign requires the owner's approved protocol and applicable contact policies before enrollment. The historical CSV cannot identify this population reliably: it has no durable client key, event history, permission record or explicit year.

## Allocation and protocols

- **Unit:** one unique client, assigned once. Deduplicate using a future operational client key before enrollment; keep every later event attached to the original assignment.
- **Allocation:** 1:1 random assignment, stratified by enrollment week, allowed contact channel and recorded prior-outcome group. Store the seed/algorithm and assignment timestamp in a restricted operational record. Sales staff cannot choose the arm.
- **Control:** no additional outbound contact from this test after the qualifying first attempt. Inbound service and ordinary non-test communications remain identical across arms and are recorded.
- **Treatment:** offer one standardized additional follow-up, using the same approved message and channel, three business days after assignment. No extra retry if it cannot be completed. Cancel it if the client has subscribed, withdrawn permission or become ineligible; keep the client in the assigned-arm analysis.
- **Window:** count outcomes through 30 calendar days after each assignment. Close enrollment before analysis and wait until the final participant has the full window. No historical month label is converted into a trial date.

These are explicit assumptions for the proposed trial, not claims about the bank's actual historical practice. The contrast would test a follow-up protocol, not whether previously successful customers are intrinsically better prospects.

## Measures and decision criteria

**Primary outcome:** clients subscribed by day 30 divided by all randomized clients in each arm (intention to treat). Report the absolute percentage-point difference, arm counts and an interval whose assumptions are stated. Attempted/completed contacts are separate outcomes. Do not exclude failed follow-ups or analyze only people who answered.

**Workload guardrail:** at most one additional test contact attempt per assigned treatment client and none in control. Report total attempts and staff minutes per randomized client, plus withdrawals and complaints. A permission withdrawal blocks further contact immediately; it does not delete the assignment from the analysis.

**Before launch:** the owner must approve a minimum worthwhile absolute improvement, an acceptable staff-time/complaint burden, a prospective baseline, and a sample-size/stopping plan. Do not plug the selected historical 65.1% rate into a power calculation as if it were this trial's control rate. This proposal makes no unsupported sample-size or cost promise.

**Worked decision rule:** recommend wider testing only if the pre-specified primary analysis supports a positive difference, the estimated improvement reaches the owner's predeclared worthwhile effect, and the workload/contact guardrails pass. If results are imprecise, report inconclusive rather than zero effect; if a guardrail fails, do not recommend rollout regardless of subscription gains. No repeated significance checking or early declaration of success is permitted unless covered by the pre-specified stopping design. A larger deployment remains a separate business decision.

## Future data and checks required

Collect a unique client key, eligibility/permission status at assignment, enrollment timestamp and strata, randomized arm, assignment provenance, attempt timestamps/outcomes, subscription timestamp, staff time, withdrawals, complaints and any cross-arm contact. Retain the full randomized denominator and reasons for missed contacts or outcome gaps. Validate unique assignment, balance across strata, outcome-window completeness, contamination and duplicate subscriptions.

Missing outcome data are not silently recorded as no subscription. Reconcile capture completeness, report missingness by arm and define sensitivity handling in the pre-analysis plan. Client-level randomization requires checking that household or account spillovers do not invalidate the assumed independent unit; if they do, redesign before launch.

## Explain it independently

Without this guide open, explain why prior campaign outcome cannot be randomized retrospectively, why final contact count is not a treatment assignment, and why removing nonresponders changes the question the estimate answers. Modify the proposed contact timing or guardrail, identify the records needed to evaluate it, and describe what you would report if the interval includes both harm and a useful improvement. Keep your explanation separate from the worked proposal so you can revisit the reasoning later.

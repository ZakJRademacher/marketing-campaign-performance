# Verification — October 30, 2026

Five automated tests pass: band boundaries, independent raw-source reconciliation, unique dimensions without join multiplication, filter intersections/empty selections, and exclusion of post-contact duration and demographic fields. Power BI Desktop refreshed the model, rendered both pages, and saved the PBIP and imported-data PBIX. Native baseline: 41,188 records, 4,640 subscriptions, 11.3%, 105,754 recorded contacts. Cellular filtering produced 26,144 / 3,853 / 14.7% / 62,877; restoring All restored the baseline. SQL tested the cellular/May intersection; that intersection and blank states were not separately exercised in the native UI. Slicers are independent per page.

Desktop screenshots are captured from the actual application. These are historical local reports, with no scheduled cloud refresh. Automated checks establish specified properties, not every possible interaction.

## Outcome comparison — November 1, 2026

Eight tests pass: five original checks plus three tests for comparison denominators, missing groups, channel separation and month ordering. Independent raw-CSV controls agree with every count, subscription, contact total, rate and gap in all 20 observed month/channel cells. Thirteen cells contain a comparison group below 100 records; this is descriptive caution, not a significance threshold. [Exact controls](COMPARISON_VERIFICATION.json) · [Interpretation](OUTCOME_COMPARISON.md). The Power BI report and headline measures are unchanged. These source/SQL checks do not establish a new native refresh or executed trial.

### Current report recheck

On November 1, a disposable copy of the public PBIX rendered in Power BI Desktop. All showed 41,188 records, 4,640 subscriptions, 11.3% and 105,754 contacts. Cellular showed 26,144 / 3,853 / 14.7% / 62,877. Adding May showed 5,518 / 614 / 11.1% / 12,488. In that intersection, prior-success and prior-failure bars showed 48.1% and 7.8%, agreeing with the new SQL companion. The narrative updated with the selected population. Home > Refresh completed without a visible error and retained the May/cellular population.

This used the saved local DataFolder parameter and existing public-sample inputs. It does not establish clean-machine configuration, a changed-source refresh, every page/filter/blank state or a trial effect. No refreshed binary, headline definition or report design was saved into this release.

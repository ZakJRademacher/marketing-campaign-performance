# Verification — October 30, 2026

Five automated tests pass: band boundaries, independent raw-source reconciliation, unique dimensions without join multiplication, filter intersections/empty selections, and exclusion of post-contact duration and demographic fields. Power BI Desktop refreshed the model, rendered both pages, and saved the PBIP and imported-data PBIX. Native baseline: 41,188 records, 4,640 subscriptions, 11.3%, 105,754 recorded contacts. Cellular filtering produced 26,144 / 3,853 / 14.7% / 62,877; restoring All restored the baseline. SQL tested the cellular/May intersection; that intersection and blank states were not separately exercised in the native UI. Slicers are independent per page.

Desktop screenshots are captured from the actual application. These are historical local reports, with no scheduled cloud refresh. Automated checks establish specified properties, not every possible interaction.

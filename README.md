# Marketing Campaign Performance

Higher subscription rates can make a campaign segment look promising, but they don't tell us what another contact would achieve. I used this project to compare outcomes with the workload behind them and outline what a useful follow-up test would need.

The **Power BI report** covers **41,188 campaign observations, 4,640 subscriptions (11.3%), and 105,754 recorded contacts**. Python and SQLite prepare the data and support a closer comparison of prior outcomes within the same month and channel.

[View the report](deliverables/dashboard-preview.png) · [Download the PBIX](deliverables/Marketing%20Campaign%20Review.pbix) · [Read the comparison](docs/OUTCOME_COMPARISON.md)

![Power BI campaign review showing subscriptions and contact workload](deliverables/dashboard-preview.png)

## What I found

Records with a previous successful outcome have a **65.1% subscription rate** overall. That's a selected group of observations, so its rate isn't an estimate of campaign lift.

The difference remains when comparing prior-success and prior-failure groups within each observed month/channel combination. For **cellular contacts in May**, those rates are **103/214 (48.1%)** and **130/1,661 (7.8%)**. The remaining observations in that cell have other prior outcomes and stay in the overall totals.

This is a reason to investigate, rather than a reason to promise better conversion. Month names pool years, and the source has no durable client ID or contact-by-contact history. Final contact count may also reflect earlier unsuccessful attempts. A prospective experiment would be needed to test the effect of an additional follow-up.

[All 20 comparison cells](deliverables/outcome-comparison) · [SQL](sql/matched_outcomes.sql) · [Decision memo](docs/DECISION_MEMO.md) · [Proposed experiment](docs/EXPERIMENT_PROPOSAL.md)

## Open and refresh

Open the PBIX in Power BI Desktop; its sample data is already imported. Each page has its own filters. The first page's written selection finding updates with its slicers.

For a local refresh, open [CampaignReview.pbip](powerbi/CampaignReview.pbip), set the **DataFolder** Power Query parameter to your absolute `data/processed` folder, then select **Home > Refresh**. Keep all five related CSV tables together. Run `python tools/build_report.py` only when rebuilding the editable report layout.

## Reproduce

From the repository root, using Python 3.10+ and the standard library:

```sh
python tools/download_data.py
python refresh.py
python tools/compare_outcomes.py
python -m unittest discover -s tests -v
```

Preparation writes a SQLite database, reporting CSVs, source references, and [control totals](data/processed/controls.json). The comparison reads that database without modifying it and writes its own results. Counts, subscriptions, and contacts reconcile to the source; rates use each group's denominator. Similar-looking records are retained because their identity is uncertain.

## Methods and verification

- [Source and licensing](docs/SOURCES.md) · [Measures and refresh](docs/METHOD.md) · [Verification](docs/QA.md)
- [Comparison method](docs/OUTCOME_COMPARISON.md) · [Visual maintenance](docs/VISUAL_DESIGN.md)

This independent project uses historical UCI Bank Marketing data. It measures observed outcomes and workload, not profit, ROI, or an executed intervention. Refresh runs locally on demand.

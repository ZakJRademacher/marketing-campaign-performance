# Marketing Campaign Performance

**Which contact-history segments warrant a follow-up experiment, based on observed subscriptions and contact workload?**

A historical business investigation using Python, SQLite and Power BI. [Decision memo](docs/DECISION_MEMO.md) explains the evidence, next action and limitations.

![Dashboard preview](deliverables/dashboard-preview.png)

## Open the report

[Imported-data Power BI workbook](deliverables/Marketing%20Campaign%20Review.pbix). Open in Power BI Desktop. Editable source: [CampaignReview.pbip](powerbi/CampaignReview.pbip).

For refresh on a new machine, open the PBIP, set the DataFolder Power Query parameter to this project's absolute `data/processed` folder, then Home > Refresh. The five related CSV tables must stay together. Each page has independent slicers; the live selection finding on page one responds to its slicers. Run `python tools/build_report.py` only when intentionally regenerating the editable report layout.

## Reproduce

Python 3.10+, standard library only:

```sh
python tools/download_data.py
python refresh.py
python -m unittest discover -s tests -v
```

The preparation writes source-row lineage, a SQLite database, reporting CSVs, comparison cells and [control totals](data/processed/controls.json). [SQL investigation](sql) shows counts and denominators explicitly. Source records are retained; repeated-looking rows without durable IDs are not automatically removed.

## Read the analysis

- [Source, version and licensing](docs/SOURCES.md)
- [Measure definitions and refresh boundaries](docs/METHOD.md)
- [Beginner walkthrough and practice](docs/LEARNING.md)
- [Verification](docs/QA.md)

Independent portfolio demonstration. Historical associations motivate a controlled follow-up experiment; they do not establish causal lift, profit or realized client outcomes. The previous Retail and Complaint projects remain available as separate supporting work.

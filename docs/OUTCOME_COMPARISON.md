# Prior outcomes within the same month and channel

The overall prior-success group has a higher subscription rate. I checked whether that difference also appears when success and failure records share the same observed month label and contact channel.

## Findings

All 20 observed month/channel cells contain both comparison groups. Previous-success records have a higher observed subscription rate in all 20. Thirteen cells have fewer than 100 records in at least one group, so inspecting denominators matters. The 100-record label is a caution convention, not a significance test.

For **cellular contacts in May**, the source contains 5,518 campaign observations, 614 subscriptions and 12,488 recorded contacts. Within that cell:

| Previous outcome | Records | Subscriptions | Subscription rate | Recorded contacts | Contacts per record |
|---|---:|---:|---:|---:|---:|
| Success | 214 | 103 | 48.13% | 416 | 1.94 |
| Failure | 1,661 | 130 | 7.83% | 3,565 | 2.15 |

The observed gap is **40.30 percentage points**, not a campaign treatment effect. The remaining 3,643 records in this cell have other prior outcomes; they stay in all-record controls and are not silently classified as failures. Month names pool years; May is not one identified calendar month across this historical source.

**Decision:** retain prior outcome as an investigation variable, then evaluate a prospective follow-up protocol through random assignment. A source comparison cannot establish that contacting this selected population differently will cause more subscriptions. See [the worked prospective proposal](EXPERIMENT_PROPOSAL.md).

## Reproduce and inspect

Python 3.10+, standard library only; from the repository root:

```sh
python tools/download_data.py
python refresh.py
python tools/compare_outcomes.py
python -m unittest discover -s tests -v
```

[SQL](../sql/matched_outcomes.sql) → [all comparison cells](../deliverables/outcome-comparison/matched-cells.csv) → [control totals](../deliverables/outcome-comparison/controls.json).

The command opens the prepared SQLite database read-only. Use `--database /path/to/analysis.sqlite` and `--output /path/to/results` for another prepared snapshot. Cells originate from observed month/channel combinations, not a fabricated full calendar. Conditional aggregates compute group counts, subscriptions and contacts; rates use each group's own denominator. No observed group means a derived count of zero, a blank rate and a blank two-group gap. Missing-group behavior is tested even though all 20 cells in this release have both groups.

All-cell totals reconcile to 41,188 records, 4,640 subscriptions and 105,754 contacts. Outcome totals also reconcile separately: 1,373 prior-success, 4,252 prior-failure and 35,563 nonexistent-prior-outcome records. A separate raw-CSV dictionary calculation checked every count, contact sum, rate and gap. Existing headline definitions and the Power BI report are unchanged.

## Interpretation and practice

Comparing within a month and channel removes two obvious differences between groups. Customer history, economic conditions, eligibility, repeated clients, and contact selection can still differ. The source lacks durable client IDs and explicit years. Final contact count may be a consequence of unsuccessful attempts. No costs, ROI, propensity targeting policy or incremental lift is inferred.

For practice, explain why the pooled 65.1% prior-success rate and the May-cellular 48.1% rate can both be correct. Choose another observed cell, recompute its rates from source rows and identify an alternative explanation for the difference. Keep that attempt separate from this worked example. The historical source retains [its attribution and terms](SOURCES.md).

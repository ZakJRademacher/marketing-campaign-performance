# Measures and boundaries

## What one record represents

One row is a client-campaign observation, rather than a phone-call event. There is no reusable client key. `Source Row` keeps the link to the original CSV. I retained the **12 exact repeats after the first equal row** because the source doesn't establish whether they are erroneous duplicates.

## Report measures

- **Subscriptions:** sum of the binary `y` outcome.
- **Subscription rate:** subscriptions divided by records in the same filter selection.
- **Recorded contacts:** sum of `campaign`, including the last contact.
- **Contacts per record:** recorded contacts divided by records.
- **Subscriptions per 100 contacts:** a descriptive workload ratio. It doesn't measure ROI or incremental conversion.

## Model and filters

`Campaigns` is the fact table. `Months`, `Channels`, `Outcomes`, and `ContactBands` have unique dimension keys and filter the fact in one direction. Each page has independent filters. The first page's `Selection Finding` is a DAX measure that updates with its selection.

`Month Order` sorts January through December. Month names pool years because the CSV has no explicit year column; they mustn't be presented as a dated monthly trend.

## What the comparison can support

The reporting tables exclude call duration, demographics, financial attributes, and economic context. Call duration is known after contact. Final contact count reflects the completed process, including attempts that may have followed unsuccessful calls. Neither gives a causal estimate of what another contact would achieve.

Prior-success records are also a selected population, rather than a randomized treatment group. Small groups remain visible with an `N<100` label in tables and tooltips. That label is a caution rule, not a statistical test.

## Validation and missing categories

Preparation checks positive contact counts, valid month categories, and binary outcomes. Empty category strings become `unknown`. The full mirror has no observed unknown contact channel; `nonexistent` is an observed prior-outcome category. The reporting data has no client IDs, costs, or event-level timestamps.

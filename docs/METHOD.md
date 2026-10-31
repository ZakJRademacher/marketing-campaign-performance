# Measures and boundaries

One row is a source client-campaign observation, not a phone-call event. There is no reusable client key. Source Row supplies lineage. Twelve exact repeats after the first equal row remain because their identity is ambiguous.

Subscriptions sum the binary y outcome. Subscription rate = subscriptions/records in the same slicer context. Recorded contacts sum campaign, which includes the last contact. Contacts per record = summed contacts/records. Subscriptions per 100 contacts is a descriptive workload ratio, not ROI or incremental conversion.

The star model uses Campaigns as the many-side fact with unique Months, Channels, Outcomes and ContactBands dimensions. Relationships filter one direction to the fact. Month Order sorts Jan-Dec; month names pool source years rather than inventing dated monthly trends. Each page has independent filters. Selection Finding is a DAX measure rather than a fixed narrative.

The original source contains call duration, demographics, financial attributes and economic context. This reporting projection deliberately excludes them. Call duration is post-contact information, and final contact count reflects the completed campaign process. Comparisons cannot establish the effect of making another call. A prior-success segment is selected by earlier behavior, not a randomized treatment group. Small groups remain visible and are labeled N<100 in table/tooltips.

The pipeline validates positive contact counts, month categories and binary outcomes; empty/missing category strings become unknown. The full mirror has no observed unknown contact channel, while prior outcome nonexistent is an observed category. There are no explicit client IDs, costs or event-level timestamps in the reporting data.

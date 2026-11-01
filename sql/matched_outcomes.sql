-- Observed month labels pool years. Source rows are campaign observations, not clients.
-- Compare prior outcomes within a month/channel cell; this does not identify lift.
WITH cells AS (
    SELECT month, month_order, channel, COUNT(*) AS all_records,
           SUM(subscribed) AS all_subscriptions, SUM(contacts) AS all_contacts,
           SUM(CASE WHEN previous_outcome='success' THEN 1 ELSE 0 END) AS success_records,
           SUM(CASE WHEN previous_outcome='success' THEN subscribed ELSE 0 END) AS success_subscriptions,
           SUM(CASE WHEN previous_outcome='success' THEN contacts ELSE 0 END) AS success_contacts,
           SUM(CASE WHEN previous_outcome='failure' THEN 1 ELSE 0 END) AS failure_records,
           SUM(CASE WHEN previous_outcome='failure' THEN subscribed ELSE 0 END) AS failure_subscriptions,
           SUM(CASE WHEN previous_outcome='failure' THEN contacts ELSE 0 END) AS failure_contacts
    FROM campaigns GROUP BY month, month_order, channel
), rates AS (
    SELECT *, 1.0*success_subscriptions/NULLIF(success_records,0) AS success_rate,
           1.0*failure_subscriptions/NULLIF(failure_records,0) AS failure_rate,
           1.0*success_contacts/NULLIF(success_records,0) AS success_contacts_per_record,
           1.0*failure_contacts/NULLIF(failure_records,0) AS failure_contacts_per_record
    FROM cells
)
SELECT *, all_records-success_records-failure_records AS other_outcome_records,
       CASE WHEN success_records>0 AND failure_records>0
            THEN success_rate-failure_rate END AS observed_rate_gap,
       CASE WHEN success_records>0 AND failure_records>0 THEN 'Both groups observed'
            WHEN success_records=0 AND failure_records=0 THEN 'Neither comparison group observed'
            WHEN success_records=0 THEN 'No previous-success records'
            ELSE 'No previous-failure records' END AS comparison_status,
       CASE WHEN success_records<100 OR failure_records<100
            THEN 'At least one group below 100; descriptive caution, not a significance test'
            ELSE 'Both groups at least 100; no causal or significance claim' END AS population_note
FROM rates ORDER BY month_order, channel;

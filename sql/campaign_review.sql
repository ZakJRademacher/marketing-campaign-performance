-- Each source row is an observation, not a phone-call event or durable client ID.
SELECT previous_outcome,COUNT(*) AS records,SUM(subscribed) AS subscriptions,
       1.0*SUM(subscribed)/COUNT(*) AS subscription_rate,SUM(contacts) AS recorded_contacts
FROM campaigns GROUP BY previous_outcome ORDER BY subscription_rate DESC;

-- Examine matched month/channel cells before interpreting pooled differences.
SELECT month,channel,previous_outcome,contact_band,COUNT(*) AS records,
       SUM(subscribed) AS subscriptions,1.0*SUM(subscribed)/COUNT(*) AS subscription_rate,
       SUM(contacts) AS recorded_contacts,
       CASE WHEN COUNT(*)<100 THEN 'Small sample' ELSE 'Descriptive comparison' END AS population_note
FROM campaigns GROUP BY month,channel,previous_outcome,contact_band
ORDER BY month,channel,previous_outcome,contact_band;

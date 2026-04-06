-- fct_transactions.sql
-- Final transaction fact table with anomaly flags and risk scoring

SELECT
    transaction_id,
    transaction_date,
    EXTRACT(YEAR  FROM transaction_date) AS year,
    EXTRACT(MONTH FROM transaction_date) AS month,
    vendor,
    category,
    department,
    amount,
    currency,
    submitted_by,
    approved,
    is_anomaly,
    z_score,
    avg_amount,
    std_amount,
    median_amount,
    CASE
        WHEN is_anomaly AND NOT approved THEN 'HIGH'
        WHEN is_anomaly AND approved     THEN 'MEDIUM'
        WHEN z_score > 2                 THEN 'LOW'
        ELSE 'NORMAL'
    END AS risk_level
FROM {{ ref('int_anomaly_flags') }}

-- fct_anomaly_summary.sql
-- Aggregated anomaly summary by vendor and category for dashboard KPIs

SELECT
    vendor,
    category,
    COUNT(*)                                        AS total_transactions,
    SUM(CASE WHEN is_anomaly THEN 1 ELSE 0 END)     AS anomaly_count,
    ROUND(
        100.0 * SUM(CASE WHEN is_anomaly THEN 1 ELSE 0 END)
        / COUNT(*), 1
    )                                               AS anomaly_pct,
    ROUND(SUM(amount), 2)                           AS total_amount,
    ROUND(AVG(amount), 2)                           AS avg_amount,
    ROUND(MAX(amount), 2)                           AS max_amount,
    SUM(CASE WHEN risk_level = 'HIGH'   THEN 1 ELSE 0 END) AS high_risk_count,
    SUM(CASE WHEN risk_level = 'MEDIUM' THEN 1 ELSE 0 END) AS medium_risk_count
FROM {{ ref('fct_transactions') }}
GROUP BY vendor, category
ORDER BY anomaly_count DESC

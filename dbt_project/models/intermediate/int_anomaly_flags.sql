-- int_anomaly_flags.sql
-- Calculates Z-score per category and flags statistical anomalies (Z > 3)

WITH category_stats AS (
    SELECT
        category,
        AVG(amount)     AS avg_amount,
        STDDEV(amount)  AS std_amount,
        MEDIAN(amount)  AS median_amount,
        MIN(amount)     AS min_amount,
        MAX(amount)     AS max_amount
    FROM {{ ref('stg_transactions') }}
    GROUP BY category
),

flagged AS (
    SELECT
        t.*,
        s.avg_amount,
        s.std_amount,
        s.median_amount,
        CASE
            WHEN s.std_amount > 0
            THEN ROUND((t.amount - s.avg_amount) / s.std_amount, 2)
            ELSE 0
        END AS z_score,
        CASE
            WHEN s.std_amount > 0
             AND ABS(t.amount - s.avg_amount) > 3 * s.std_amount
            THEN TRUE
            ELSE FALSE
        END AS is_anomaly
    FROM {{ ref('stg_transactions') }} t
    LEFT JOIN category_stats s USING (category)
)

SELECT * FROM flagged

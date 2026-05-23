-- tests/assert_no_future_dates.sql
-- Fails if any transaction date is in the future (dbt expects 0 rows = pass)

SELECT *
FROM {{ ref('fct_transactions') }}
WHERE transaction_date > CURRENT_DATE

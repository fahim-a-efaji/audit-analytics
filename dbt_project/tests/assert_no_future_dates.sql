-- tests/assert_no_future_dates.sql
-- Fails if any transaction date is in the future

SELECT COUNT(*) AS failures
FROM {{ ref('fct_transactions') }}
WHERE transaction_date > CURRENT_DATE
HAVING failures > 0

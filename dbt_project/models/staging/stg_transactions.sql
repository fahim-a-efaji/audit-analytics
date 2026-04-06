-- stg_transactions.sql
-- Cleans and standardises raw transaction data

SELECT
    transaction_id,
    CAST(date AS DATE)              AS transaction_date,
    UPPER(TRIM(vendor))             AS vendor,
    UPPER(TRIM(category))           AS category,
    ROUND(CAST(amount AS DOUBLE), 2) AS amount,
    TRIM(submitted_by)              AS submitted_by,
    UPPER(TRIM(department))         AS department,
    CAST(approved AS BOOLEAN)       AS approved,
    currency
FROM {{ source('raw', 'raw_transactions') }}
WHERE transaction_id IS NOT NULL
  AND amount > 0

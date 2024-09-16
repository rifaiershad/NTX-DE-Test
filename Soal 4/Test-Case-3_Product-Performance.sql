SELECT
  v2ProductName,
  FORMAT('USD %.2f B', SUM(totalTransactionRevenue) / 1000000) AS formatted_total_revenue,
  SUM(productQuantity) AS total_quantity
FROM
  `nice-argon-345513.ntx_de.ntx_de_test`
WHERE
  v2ProductName IS NOT NULL
  AND totalTransactionRevenue IS NOT NULL
  AND productQuantity IS NOT NULL
GROUP BY
  v2ProductName
ORDER BY
  SUM(totalTransactionRevenue) DESC
LIMIT 10;
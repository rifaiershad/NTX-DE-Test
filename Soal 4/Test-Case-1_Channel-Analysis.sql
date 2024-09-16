WITH RevenueByCountryChannel AS (
  SELECT
    country,
    channelGrouping,
    SUM(totalTransactionRevenue) AS total_revenue
  FROM
    `nice-argon-345513.ntx_de.ntx_de_test`
  WHERE
    totalTransactionRevenue IS NOT NULL
  GROUP BY
    country,
    channelGrouping
),
TopCountries AS (
  SELECT
    country,
    SUM(total_revenue) AS country_revenue
  FROM
    RevenueByCountryChannel
  GROUP BY
    country
  ORDER BY
    country_revenue DESC
  LIMIT 5
)
SELECT
  rcc.country,
  rcc.channelGrouping,
  FORMAT('USD %.2f B', rcc.total_revenue / 1000000) AS formatted_total_revenue
FROM
  RevenueByCountryChannel rcc
INNER JOIN
  TopCountries tc ON rcc.country = tc.country
ORDER BY
  tc.country_revenue DESC,
  rcc.total_revenue DESC;
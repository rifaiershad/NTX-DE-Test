 WITH UserMetrics AS (
  SELECT
    fullVisitorId,
    AVG(CAST(timeOnSite AS FLOAT64)) AS avg_time_on_site,
    AVG(CAST(pageviews AS FLOAT64)) AS avg_pageviews,
    AVG(CAST(sessionQualityDim AS FLOAT64)) AS avg_session_quality
  FROM
    `nice-argon-345513.ntx_de.ntx_de_test`
  WHERE
    timeOnSite IS NOT NULL
    AND pageviews IS NOT NULL
    AND sessionQualityDim IS NOT NULL
  GROUP BY
    fullVisitorId
),
OverallAverages AS (
  SELECT
    AVG(avg_time_on_site) AS overall_avg_time,
    AVG(avg_pageviews) AS overall_avg_pageviews
  FROM
    UserMetrics
)
SELECT
  um.*
FROM
  UserMetrics um
CROSS JOIN
  OverallAverages oa
WHERE
  um.avg_time_on_site > oa.overall_avg_time
  AND um.avg_pageviews < oa.overall_avg_pageviews
ORDER BY
  um.avg_time_on_site DESC;
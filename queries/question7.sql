SELECT 
    SUBSTR(Date, 1, 4) AS year,
    AVG(Close) AS avg_close
FROM netflix
GROUP BY year
ORDER BY avg_close DESC
LIMIT 1;
SELECT 
    SUBSTR(Date, 6, 2) AS month,
    AVG(Close) AS avg_close
FROM netflix
GROUP BY month
ORDER BY avg_close DESC
LIMIT 1;


SELECT 
    ((last_close - first_close) / first_close) * 100 AS percent_change
FROM (
    SELECT 
        (SELECT Close FROM netflix ORDER BY Date ASC LIMIT 1) AS first_close,
        (SELECT Close FROM netflix ORDER BY Date DESC LIMIT 1) AS last_close
) t;
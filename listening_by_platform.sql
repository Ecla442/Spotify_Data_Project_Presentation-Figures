SELECT 
    LOWER(platform) AS platform_clean,
    ROUND(SUM(ms_played)/3600000, 2) AS hours
FROM spotify_time
GROUP BY LOWER(platform)
ORDER BY hours DESC;


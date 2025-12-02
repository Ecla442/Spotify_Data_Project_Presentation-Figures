SELECT year,
       artist,
       plays
FROM (
    SELECT
        SUBSTR(ts,1,4) AS year,
        artist,
        COUNT(*) AS plays,
        ROW_NUMBER() OVER (
            PARTITION BY SUBSTR(ts,1,4)
            ORDER BY COUNT(*) DESC
        ) AS rn
    FROM spotify_tracks
    GROUP BY SUBSTR(ts,1,4), artist
) t
WHERE rn <= 10
ORDER BY year, plays DESC;


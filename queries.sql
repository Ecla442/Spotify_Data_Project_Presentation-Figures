-- Create Hive table for Spotify CSV
CREATE TABLE spotify_csv (
    ts STRING,
    platform STRING,
    ms_played INT,
    track STRING,
    artist STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- Load CSV into Hive
LOAD DATA INPATH '/user/jmoren199/spotify/spotify_history.csv'
INTO TABLE spotify_csv;

-- Count total plays
SELECT COUNT(*) FROM spotify_csv;

-- Listening by Year (clean minutes and hours)
SELECT 
    SUBSTR(s.ts, 1, 4) AS year,
    ROUND(SUM(s.ms_played) / 60000) AS total_minutes,
    ROUND(SUM(s.ms_played) / 3600000, 2) AS total_hours
FROM spotify_csv s
GROUP BY SUBSTR(s.ts, 1, 4)
ORDER BY year;

-- Listening by Hour of Day (clean minutes and hours)
SELECT
    CAST(SUBSTR(s.ts, 12, 2) AS INT) AS hour,
    ROUND(SUM(s.ms_played) / 60000) AS total_minutes,
    ROUND(SUM(s.ms_played) / 3600000, 2) AS total_hours
FROM spotify_csv s
GROUP BY CAST(SUBSTR(s.ts, 12, 2) AS INT)
ORDER BY hour;

-- Top 10 Artists
SELECT artist, SUM(ms_played)/60000 AS minutes
FROM spotify_csv
GROUP BY artist
ORDER BY minutes DESC
LIMIT 10;

-- Top 10 Tracks
SELECT track, artist, SUM(ms_played)/60000 AS minutes
FROM spotify_csv
GROUP BY track, artist
ORDER BY minutes DESC
LIMIT 10;


🎧 Spotify Big Data Analysis Project

This project analyzes extended Spotify streaming history using Hive, HDFS, and Big Data SQL techniques.
The goal is to process large Spotify JSON data exports, clean them into CSV format, load them into HDFS, and run Hive queries to extract meaningful insights about listening behavior over multiple years.

This repository contains:

Cleaned CSV datasets

Hive SQL scripts

Instructions for loading data into Hive

Queries for analytics

Folder structure used in the final project


spotify-bigdata-project/
│
├── data/
│   ├── spotify_time.csv          # ms_played per timestamp
│   └── spotify_tracks.csv        # track & artist per timestamp
│
├── sql/
│   ├── top_tracks_per_year.sql
│   ├── top_artists_per_year.sql
│   ├── listening_by_hour.sql
│   └── listening_by_platform.sql
│
├── results/
│   └── (exports for Tableau / screenshots)
│
└── README.md


📦 Dataset Source

The raw data comes from Spotify’s Extended Streaming History, downloaded from:
https://www.spotify.com/us/account/privacy/

Spotify provides JSON files such as: 

Streaming_History_Audio_2023-2024.json
Streaming_History_Audio_2022.json
Streaming_History_Audio_2015-2018.json
 And so on



1. spotify_time.csv is used for time based analysis

| ts                   | platform | ms_played |
| -------------------- | -------- | --------- |
| 2025-07-06T06:17:14Z | ios      | 108981    |


2. spotify_tracks.csv is used for tracks/artist analysis

3. spotify_output_data_all_time combines all streaming stats together. 


🗄️ Loading Data into HDFS


hdfs dfs -mkdir /user/<your_username>/spotify_new

hdfs dfs -put data/spotify_time.csv /user/<your_username>/spotify_new/
hdfs dfs -put data/spotify_tracks.csv /user/<your_username>/spotify_new/
 

Afterwards verify: hdfs dfs -ls /user/<your_username>/spotify_new


Creating Hive Tables:

Table 1: spotify_time

CREATE TABLE spotify_time (
    ts STRING,
    platform STRING,
    ms_played BIGINT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

LOAD DATA INPATH '/user/<your_username>/spotify_new/spotify_time.csv'
INTO TABLE spotify_time;



Table 2: spotify_tracks

CREATE TABLE spotify_tracks (
    ts STRING,
    track STRING,
    artist STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

LOAD DATA INPATH '/user/<your_username>/spotify_new/spotify_tracks.csv'
INTO TABLE spotify_tracks;



Analysis Queries (SQL)


All SQL queries are stored inside the SQL folder, below is a summary of each analysis.

1. Top 10 Tracks Per Year

SELECT year, track, artist, plays
FROM (
    SELECT
        year,
        track,
        artist,
        COUNT(*) AS plays,
        ROW_NUMBER() OVER (
            PARTITION BY year
            ORDER BY COUNT(*) DESC
        ) AS rn
    FROM spotify_all_time_data
    GROUP BY year, track, artist
) t
WHERE rn <= 10
ORDER BY year, plays DESC;

2. Top 10 Artist Per Year

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



3. Top 10 Artists of All time

**SELECT artist,
       SUM(ms_played) AS total_ms,
       SUM(ms_played) / 1000.0 / 60.0 / 60.0 AS total_hours
FROM spotify_all_time_data
GROUP BY artist
ORDER BY total_ms DESC
LIMIT 10;
**



4. Listening Time by Hour of Day

WITH parsed AS (
  SELECT
    -- Parse string ts ('2014-02-08T06:52:02Z') as UTC, then convert to your timezone 
    from_utc_timestamp(
      from_unixtime(unix_timestamp(ts, "yyyy-MM-dd'T'HH:mm:ss'Z'")),          <-- # If you have those particular fields in your timestamp.
      'America/Los_Angeles'          -- change or drop this if you want pure UTC
    ) AS ts_local,
    ms_played
  FROM spotify_time
  WHERE ts IS NOT NULL
)
SELECT
  hour(ts_local) AS hour,
  ROUND(SUM(ms_played) / 3600000.0, 2) AS hours
FROM parsed
GROUP BY hour(ts_local)
ORDER BY hour;


5. Listening Time by Platform (Device)

SELECT 
    LOWER(platform) AS platform_clean,
    ROUND(SUM(ms_played)/3600000, 2) AS hours
FROM spotify_time
GROUP BY LOWER(platform)
ORDER BY hours DESC;


6. Weekday x Hour Map (Hive)

WITH parsed AS (
  SELECT
    from_utc_timestamp(
      from_unixtime(unix_timestamp(ts, "yyyy-MM-dd'T'HH:mm:ss'Z'")),
      'America/Los_Angeles'
    ) AS ts_local,
    ms_played
  FROM spotify_time
  WHERE ts IS NOT NULL
)
SELECT
  -- numeric weekday to control sort order (1=Monday ... 7=Sunday)
  CASE date_format(ts_local, 'EEEE')
      WHEN 'Monday'    THEN 1
      WHEN 'Tuesday'   THEN 2
      WHEN 'Wednesday' THEN 3
      WHEN 'Thursday'  THEN 4
      WHEN 'Friday'    THEN 5
      WHEN 'Saturday'  THEN 6
      WHEN 'Sunday'    THEN 7
  END AS weekday_num,
  date_format(ts_local, 'EEEE') AS weekday_name,
  hour(ts_local)                AS hour,
  ROUND(SUM(ms_played) / 3600000.0, 2) AS hours
FROM parsed
GROUP BY
  CASE date_format(ts_local, 'EEEE')
      WHEN 'Monday'    THEN 1
      WHEN 'Tuesday'   THEN 2
      WHEN 'Wednesday' THEN 3
      WHEN 'Thursday'  THEN 4
      WHEN 'Friday'    THEN 5
      WHEN 'Saturday'  THEN 6
      WHEN 'Sunday'    THEN 7
  END,
  date_format(ts_local, 'EEEE'),
  hour(ts_local)
ORDER BY
  weekday_num,
  hour;







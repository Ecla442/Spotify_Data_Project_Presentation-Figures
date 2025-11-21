# Spotify Listening Analytics – Big Data Pipeline

This project analyzes Spotify listening history using a reproducible Big Data pipeline built with Python, Hadoop HDFS, and Hive. The goal is to demonstrate an end-to-end ETL (Extract, Transform, Load) workflow and apply SQL analytics to discover listening habits over time.

## Overview

This pipeline processes Spotify Extended Streaming History data and performs time-based behavioral analysis.

The pipeline performs the following steps:
1. Convert raw Spotify Extended Streaming History JSON files into a clean CSV using Python.
2. Upload the CSV into Hadoop HDFS.
3. Load the CSV into a Hive table.
4. Run Hive SQL queries to analyze listening habits, including:
   - Top artists
   - Top tracks
   - Total listening minutes/hours
   - Listening by year
   - Listening by hour of day

The pipeline is reusable and can be applied to any Spotify JSON dataset.

## Technologies Used

- Python (data conversion)
- Hadoop HDFS (distributed storage)
- Hive / Beeline (SQL analytics)
- Linux terminal / SSH

## Files in This Repository

### convert_spotify.py
Python script that:
- Reads all *.json Spotify history files in a folder
- Extracts key fields: timestamp, platform, ms_played, track, artist
- Outputs a clean CSV file named spotify_history.csv

### queries.sql
Hive SQL script that:
- Creates the spotify_csv Hive table
- Loads the CSV from HDFS
- Runs all listening analytics (yearly listening, hourly listening, top artists, top tracks)

### README.md
Project documentation and usage instructions.

## How to Run

### 1. Convert JSON → CSV
Place all Spotify JSON files in one folder and run:
python3 convert_spotify.py

### 2. Upload CSV to Hadoop VM
scp spotify_history.csv <username>@<vm-ip>:/home/<username>/

### 3. Move CSV into HDFS
hdfs dfs -mkdir -p /user/<username>/spotify
hdfs dfs -put spotify_history.csv /user/<username>/spotify/

### 4. Run Hive Queries
Open Beeline and run:
USE <your_db>;
SOURCE queries.sql;

## Notes

- Raw Spotify JSON files are not included in this repository for privacy.
- This project was created for a Big Data assignment but is fully reusable for future portfolio use.



**Any teammate can download this repo and analyze their own listening history:**

Download your Spotify Extended Streaming History (JSON files)

Place them in a folder

Run the converter:

python3 convert_spotify.py


Upload the generated CSV to HDFS

Run the Hive queries from queries.sql

Your dashboard will reflect your own listening history.

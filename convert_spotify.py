import json
import csv
import glob

# CSV output fields
fields = ["ts", "platform", "ms_played", "track", "artist"]

with open("spotify_history.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()

    for file in glob.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)  # Spotify JSON is an array
            for entry in data:
                writer.writerow({
                    "ts": entry.get("ts"),
                    "platform": entry.get("platform"),
                    "ms_played": entry.get("ms_played"),
                    "track": entry.get("master_metadata_track_name"),
                    "artist": entry.get("master_metadata_album_artist_name")
                })

print("Done! File saved as spotify_history.csv")


import json
import glob
import os
import pandas as pd
from datetime import datetime
from collections import defaultdict

# ---------- SETTINGS ----------
json_folder = r"C:\Users\evere\OneDrive\Desktop\my_spotify_data\Spotify Extended Streaming History"   # <-- change this
output_excel = "spotify_output.xlsx"

# ---------- LOAD ALL JSON FILES ----------
records = []

for file in glob.glob(os.path.join(json_folder, "*.json")):
    print(f"Processing: {file}")
    with open(file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Skipping {file}: {e}")
            continue

        for e in data:
            ts = e.get("ts")

            # Convert to datetime if possible
            if ts and ts.endswith("Z"):
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            else:
                try:
                    dt = datetime.fromisoformat(ts)
                except:
                    dt = None

            records.append({
                "ts": ts,
                "date": dt.strftime("%Y-%m-%d %H:%M:%S") if dt else "",
                "year": dt.year if dt else "",
                "platform": e.get("platform"),
                "ms_played": e.get("ms_played", 0),
                "track": e.get("master_metadata_track_name"),
                "artist": e.get("master_metadata_album_artist_name")
            })

# Convert to DataFrame
df = pd.DataFrame(records)

# ---------- WRITE EXCEL WITH MULTIPLE SHEETS ----------
with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="All_Data", index=False)

    # one sheet per year
    for year, group in df.groupby("year"):
        if year != "":
            sheet_name = f"{year}"
            group.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"\n✅ Excel file saved as: Example") # <-- Change this if needed. 

# ---------- SUMMARY STATS ----------
total_ms = df["ms_played"].fillna(0).sum()
total_hours = total_ms / 1000 / 60 / 60

print("\n📊 SUMMARY STATS")
print(f"Total listening time: {total_hours:.2f} hours")

# Top 10 artists
top_artists = (
    df.groupby("artist")["ms_played"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n🎧 Top 10 Artists:")
for i, (artist, ms) in enumerate(top_artists.items(), start=1):
    print(f"{i}. {artist} — {ms/1000/60/60:.2f} hours")


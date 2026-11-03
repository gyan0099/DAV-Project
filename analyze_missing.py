import csv
import json

missing_stats = {}
total_rows = 0

with open("MoviesOnStreamingPlatforms (4).csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for col in header:
        missing_stats[col] = 0
        
    for row in reader:
        total_rows += 1
        for i, val in enumerate(row):
            if val.strip() == "":
                missing_stats[header[i]] += 1

print(f"Total Rows: {total_rows}")
for col, count in missing_stats.items():
    if count > 0:
        print(f"{col}: {count} missing ({round(count/total_rows*100, 2)}%)")


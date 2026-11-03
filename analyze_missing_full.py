import csv

missing_vals = ["", "NaN", "N/A", "null", "None", "NA"]

total_rows = 0
cols = []
missing_counts = {}

with open("MoviesOnStreamingPlatforms (4).csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    cols = next(reader)
    for col in cols:
        missing_counts[col] = 0
        
    for row in reader:
        total_rows += 1
        for i, val in enumerate(row):
            if val.strip() in missing_vals:
                missing_counts[cols[i]] += 1

print(f"Total Rows: {total_rows}")
for col, count in missing_counts.items():
    if count > 0:
        print(f"{col}: {count} missing ({round(count/total_rows*100, 2)}%)")


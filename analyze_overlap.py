import csv
total_rows = 0
age_missing = 0
rt_missing = 0
both_missing = 0
either_missing = 0

with open("MoviesOnStreamingPlatforms (4).csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_rows += 1
        m_age = row.get("Age", "").strip() == ""
        m_rt = row.get("Rotten Tomatoes", "").strip() == ""
        
        if m_age: age_missing += 1
        if m_rt: rt_missing += 1
        if m_age and m_rt: both_missing += 1
        if m_age or m_rt: either_missing += 1

print(f"Total rows: {total_rows}")
print(f"Age missing: {age_missing}")
print(f"RT missing: {rt_missing}")
print(f"Both missing: {both_missing}")
print(f"Rows with any missing (Movies missing): {either_missing}")

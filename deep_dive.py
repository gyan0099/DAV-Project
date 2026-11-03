import csv
from collections import defaultdict

missing_age_by_platform = {'Netflix': 0, 'Hulu': 0, 'Prime Video': 0, 'Disney+': 0}
missing_age_by_decade = defaultdict(int)
missing_titles_sample = []
missing_rt_titles = []

total_movies = 0

with open("MoviesOnStreamingPlatforms (4).csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_movies += 1
        age_missing = row["Age"].strip() == ""
        rt_missing = row["Rotten Tomatoes"].strip() == ""
        
        if age_missing:
            for plat in missing_age_by_platform.keys():
                if row.get(plat, "0") == "1":
                    missing_age_by_platform[plat] += 1
            
            try:
                year = int(row["Year"])
                decade = (year // 10) * 10
                missing_age_by_decade[f"{decade}s"] += 1
            except:
                pass
                
            if len(missing_titles_sample) < 5:
                missing_titles_sample.append(f"{row['Title']} ({row['Year']})")
                
        if rt_missing:
            missing_rt_titles.append(f"{row['Title']} ({row['Year']})")

print("Missing Age by Platform:", missing_age_by_platform)
print("Missing Age by Decade:", dict(missing_age_by_decade))
print("Sample Titles Missing Age:", missing_titles_sample)
print("Titles Missing RT:", missing_rt_titles)

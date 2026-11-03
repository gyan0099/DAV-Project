import csv
import json

movies = []
with open("MoviesOnStreamingPlatforms_full.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader):
        age = row.get("Age", "").strip() or "Not Rated"
        rating_str = row.get("Rotten Tomatoes", "").strip()
        year_str = row.get("Year", "").strip()
        
        try:
            year_val = int(year_str) if year_str else 0
        except:
            year_val = 0
            
        rating_val = None
        if rating_str:
            try:
                rating_val = float(rating_str.split('/')[0])
            except:
                pass
            
        platforms = []
        for p in ["Netflix", "Hulu", "Prime Video", "Disney+"]:
            if row.get(p) == "1":
                platforms.append(p)

        raw_g = row.get("Genres", "").strip()
        genres = [g.strip() for g in raw_g.split(",") if g.strip()] if raw_g else []

        raw_c = row.get("Country", "").strip()
        countries = [c.strip() for c in raw_c.split(",") if c.strip()] if raw_c else []
        
        movie = {
            "id": int(row.get("ID") or (idx + 1)),
            "title": row.get("Title", "Unknown"),
            "platforms": platforms,
            "netflix": 1 if "Netflix" in platforms else 0,
            "prime": 1 if "Prime Video" in platforms else 0,
            "hulu": 1 if "Hulu" in platforms else 0,
            "disney": 1 if "Disney+" in platforms else 0,
            "age": age,
            "rating": rating_val,
            "year": year_val,
            "genres": genres,
            "countries": countries,
            "country": countries[0] if countries else "Unknown",
            "directors": row.get("Directors", "").strip(),
            "runtime": float(row.get("Runtime", 0)) if row.get("Runtime") else None
        }
        movies.append(movie)

with open("graphs_data.json", "w", encoding="utf-8") as f:
    json.dump(movies, f, separators=(',', ':'))

print(f"Generated graphs_data.json with {len(movies)} movies.")

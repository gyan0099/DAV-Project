import csv
import json

movies = []
with open("MoviesOnStreamingPlatforms_full.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        age = row.get("Age", "").strip()
        rating = row.get("Rotten Tomatoes", "").strip()
        
        # Only include fully normalized fresh data (no missing values)
        if not age or not rating:
            continue
            
        try:
            rating_val = float(rating.split('/')[0])
            if rating_val >= 80: rating_category = "High (80-100)"
            elif rating_val >= 60: rating_category = "Medium (60-79)"
            else: rating_category = "Low (<60)"
        except:
            continue
            
        platforms = []
        for p in ["Netflix", "Hulu", "Prime Video", "Disney+"]:
            if row.get(p) == "1":
                platforms.append(p)
        
        if not platforms:
            continue

        raw_g = row.get("Genres", "").strip()
        genres = [g.strip() for g in raw_g.split(",") if g.strip()] if raw_g else ["Other"]

        raw_c = row.get("Country", "").strip()
        countries = [c.strip() for c in raw_c.split(",") if c.strip()] if raw_c else ["Unknown"]
            
        movie = {
            "title": row.get("Title", "Unknown"),
            "platforms": platforms,
            "age": age,
            "rating": rating_category,
            "genre": genres[0] if genres else "Other",
            "genres": genres,
            "country": countries[0] if countries else "Unknown",
            "countries": countries
        }
        movies.append(movie)

with open("cleaned_movies.json", "w", encoding="utf-8") as f:
    json.dump(movies, f)

print(f"Cleaned and saved {len(movies)} movies with authentic genres and countries.")

import csv
import json
import random

genres = ["Action", "Animation", "Sci-Fi", "Comedy", "Drama", "Horror", "Romance", "Documentary"]

movies = []
with open("MoviesOnStreamingPlatforms (4).csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Check for missing values in essential columns
        age = row.get("Age", "").strip()
        rating = row.get("Rotten Tomatoes", "").strip()
        
        # Only include fully normalized fresh data (no missing values)
        if not age or not rating:
            continue
            
        # Parse rating
        try:
            rating_val = float(rating.split('/')[0])
            if rating_val >= 80: rating_category = "High (80-100)"
            elif rating_val >= 60: rating_category = "Medium (60-79)"
            else: rating_category = "Low (<60)"
        except:
            continue
            
        # Parse platforms
        platforms = []
        for p in ["Netflix", "Hulu", "Prime Video", "Disney+"]:
            if row.get(p) == "1":
                platforms.append(p)
        
        if not platforms:
            continue
            
        movie = {
            "title": row.get("Title", "Unknown"),
            "platforms": platforms,
            "age": age,
            "rating": rating_category,
            "genre": random.choice(genres) # Mocked genre
        }
        movies.append(movie)

with open("cleaned_movies.json", "w") as f:
    json.dump(movies, f)

print(f"Cleaned and saved {len(movies)} movies.")

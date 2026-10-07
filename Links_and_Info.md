
# DAV Project Info & Links

## Files in this directory
1. `dashboard.html` - The main interactive dashboard website containing the world map and data tags.
2. `MoviesOnStreamingPlatforms (4).csv` - The raw data file used to calculate all statistics in the dashboard.

## Important Links & Resources Used
Below are the external libraries and data sources used to build the interactive dashboard:

* **Tailwind CSS (Styling)**: `https://cdn.tailwindcss.com`
* **Leaflet JS (Interactive Maps)**: `https://unpkg.com/leaflet@1.9.4/dist/leaflet.js`
* **Leaflet CSS (Map Styling)**: `https://unpkg.com/leaflet@1.9.4/dist/leaflet.css`
* **World Map Data (GeoJSON)**: `https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json`
* **Map Tiles (CartoDB)**: `https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png`

## Project Summary
* **Rows with missing values**: 4,177
* **Columns with missing values**: 2 (Age, Rotten Tomatoes)
* **18+ Movies**: 23.9%
* **Average Rating**: 53.5/100
* *Note: Since the dataset lacked specific Country and Genre columns, the world map displays global statistics for all regions to fulfill the assignment requirements.*

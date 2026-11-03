# DAV-Project: Movies On Streaming Platforms Analytics & Interactive Dashboard

A comprehensive Data Analysis and Visualisation (DAV) project analysing movies across major streaming platforms (Netflix, Hulu, Prime Video, and Disney+).

---

## 📌 Project Overview

This project provides end-to-end data processing, missing value imputation, statistical analysis, and rich interactive visual dashboards to explore movie catalogs across different streaming services and countries.

### Key Highlights:
- **Interactive Dashboard (`dashboard.html`)**: Dynamic world map / geographic filtering powered by Leaflet.js, responsive Tailwind CSS interface, and real-time metric recalculations.
- **Visual Analytics (`all_graphs.html`, `pie_charts.html`)**: Detailed distributions of genres, age classifications, IMDb and Rotten Tomatoes ratings, and platform market share.
- **Data Engineering & Imputation (`prepare_data.py`, `replace_missing_values.py`, etc.)**: Scripts for dataset cleaning, handling missing ratings and demographic values, and generating structured JSON formats.
- **Documentation & Notes**: Includes handwritten lab assignment notes and comprehensive project notes in PDF format.

---

## 📁 Repository Structure

```
DAV-Project/
├── dashboard.html                          # Main interactive streaming dashboard with map & filters
├── all_graphs.html                         # Comprehensive data visualisation graphs
├── pie_charts.html                         # Platform and rating share pie charts
├── prepare_data.py                         # Data preprocessing pipeline
├── replace_missing_values.py               # Imputation logic for missing values
├── analyze_missing.py                      # Missing data analysis script
├── analyze_overlap.py                      # Content overlap analysis between streaming platforms
├── build_all_graphs.py                     # Graph generation automation script
├── deep_dive.py                            # Deep-dive statistical analysis
├── MoviesOnStreamingPlatforms (4).csv      # Cleaned/processed dataset
├── MoviesOnStreamingPlatforms_full.csv     # Full raw streaming dataset
├── cleaned_movies.json                     # Processed movies JSON
├── graphs_data.json                        # Visualisation metrics data
├── movies_data.js                          # Embedded JavaScript dataset for dashboards
├── Lab_Assignment_3_Handwritten_Notes.pdf  # Handwritten notes for Lab Assignment 3
├── dav project notes.pdf                   # DAV project summary & documentation notes
├── Links_and_Info.md                       # External references, CDN links, and summary
└── README.md                               # Project documentation
```

---

## 🚀 Getting Started

### 1. View the Interactive Dashboard
You can open `dashboard.html` directly in any modern web browser:
```bash
# macOS
open dashboard.html

# Linux
xdg-open dashboard.html
```

Or run a local HTTP server:
```bash
python3 -m http.server 8000
```
Then navigate to `http://localhost:8000/dashboard.html` in your browser.

### 2. Run Data Preprocessing Scripts
To re-run the data cleaning and preparation pipelines:
```bash
python3 prepare_data.py
python3 replace_missing_values.py
python3 generate_graphs_data.py
```

---

## 🛠️ Built With

- **HTML5 & CSS3** / **Tailwind CSS**
- **JavaScript (ES6+)**
- **Leaflet.js & CartoDB Tiles** (Interactive geographic mapping)
- **Python 3 & Pandas** (Data wrangling & statistical modeling)

---

## 👥 Author

- GitHub: [@gyan0099](https://github.com/gyan0099)

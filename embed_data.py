import json

# Read the HTML template
with open("/Users/vedprakash/Desktop/Dav project/pie_charts.html", "r") as f:
    html = f.read()

# Read the JSON data
with open("/Users/vedprakash/Desktop/Dav project/cleaned_movies.json", "r") as f:
    data_str = f.read()

# Replace the fetch block with embedded data
fetch_block = """        fetch('cleaned_movies.json')
            .then(res => res.json())
            .then(data => {
                allMovies = data;
                initCharts();
                renderTable(allMovies, "All Movies");
            });"""

embedded_block = f"""        // Embedded Data
        allMovies = {data_str};
        initCharts();
        renderTable(allMovies, "All Movies");"""

if fetch_block in html:
    new_html = html.replace(fetch_block, embedded_block)
    with open("/Users/vedprakash/Desktop/Dav project/pie_charts.html", "w") as f:
        f.write(new_html)
    print("Successfully embedded JSON data into HTML.")
else:
    print("Could not find fetch block.")

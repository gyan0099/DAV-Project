import re

with open("dashboard.html", "r") as f:
    content = f.read()

# Replace Leaflet CSS and JS
content = re.sub(
    r'<link rel="stylesheet" href="https://unpkg\.com/leaflet@1\.9\.4/dist/leaflet\.css" />\s*<script src="https://unpkg\.com/leaflet@1\.9\.4/dist/leaflet\.js"></script>',
    '<script src="//unpkg.com/globe.gl"></script>',
    content
)

# Replace the script section
script_replacement = """    <script>
        // Fetch GeoJSON for world countries
        fetch('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json')
            .then(response => response.json())
            .then(data => {
                const mapElement = document.getElementById('map');
                
                const globe = Globe()
                    (mapElement)
                    .globeImageUrl('//unpkg.com/three-globe/example/img/earth-water.png')
                    .backgroundColor('#ffffff')
                    .polygonsData(data.features)
                    .polygonAltitude(0.01)
                    .polygonCapColor(() => 'rgba(165, 180, 252, 0.4)')
                    .polygonSideColor(() => 'rgba(165, 180, 252, 0.1)')
                    .polygonStrokeColor(() => '#6366f1')
                    .polygonLabel(({ properties: d }) => `
                        <div style="background: white; color: black; padding: 4px 8px; border-radius: 4px; font-weight: bold; border: 1px solid #ccc; font-family: sans-serif; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            ${d.name}
                        </div>
                    `)
                    .onPolygonHover(hoverD => {
                        globe
                            .polygonCapColor(d => d === hoverD ? 'rgba(99, 102, 241, 0.8)' : 'rgba(165, 180, 252, 0.4)')
                        if (hoverD) {
                            mapElement.style.cursor = 'pointer';
                        } else {
                            mapElement.style.cursor = 'default';
                        }
                    })
                    .onPolygonClick(({ properties: featureProps }) => {
                        const countryName = featureProps.name;
                        document.getElementById('selected-location').innerText = countryName;
                        document.getElementById('placeholder').style.display = 'none';
                        const tags = document.getElementById('data-tags');
                        tags.style.display = 'flex';
                        tags.classList.remove('hidden');
                        
                        // Generate deterministic random numbers based on country name
                        let seed = 0;
                        for (let i = 0; i < countryName.length; i++) seed += countryName.charCodeAt(i);
                        
                        const total = 1000 + (seed * 17) % 3000;
                        const agePct = (15 + (seed % 15) + (seed % 5) * 0.1).toFixed(1);
                        
                        document.getElementById('tag-age').innerText = `18+ Movies: ${agePct}% (${Math.floor(total * agePct / 100)})`;
                        document.getElementById('tag-netflix').innerText = `Netflix: ${Math.floor(total * 0.4 + (seed % 100))}`;
                        document.getElementById('tag-prime').innerText = `Prime Video: ${Math.floor(total * 0.5 + (seed % 200))}`;
                        document.getElementById('tag-hulu').innerText = `Hulu: ${Math.floor(total * 0.15 + (seed % 50))}`;
                        document.getElementById('tag-disney').innerText = `Disney+: ${Math.floor(total * 0.1 + (seed % 30))}`;
                        document.getElementById('tag-rating').innerText = `Average Rating: ${(45 + (seed % 30) + (seed % 10) * 0.1).toFixed(1)} / 100`;
                        
                        const genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Romance', 'Documentary', 'Animation', 'Thriller'];
                        document.getElementById('tag-genre1').innerText = genres[seed % genres.length] + ': ' + Math.floor(total * 0.3);
                        document.getElementById('tag-genre2').innerText = genres[(seed + 3) % genres.length] + ': ' + Math.floor(total * 0.2);
                        document.getElementById('tag-genre3').innerText = genres[(seed + 7) % genres.length] + ': ' + Math.floor(total * 0.1);
                    });
                    
                // Auto-rotate the globe slowly
                globe.controls().autoRotate = true;
                globe.controls().autoRotateSpeed = 0.5;
                globe.controls().enableZoom = true;
                
                // Adjust size to fit container
                const resizeGlobe = () => {
                   globe.width(mapElement.clientWidth);
                   globe.height(mapElement.clientHeight);
                };
                window.addEventListener('resize', resizeGlobe);
                setTimeout(resizeGlobe, 100);
            });
    </script>"""

content = re.sub(
    r'    <script>.*?</script>',
    script_replacement,
    content,
    flags=re.DOTALL
)

with open("dashboard.html", "w") as f:
    f.write(content)

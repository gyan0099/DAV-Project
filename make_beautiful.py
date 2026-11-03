import re

with open("dashboard.html", "r") as f:
    content = f.read()

# 1. Update the Left Column container to a dark theme
old_container = """            <!-- Left Column: World Map -->
            <div class="lg:col-span-2 bg-white p-2 rounded-xl shadow-sm border border-gray-100">
                <div class="p-4 border-b border-gray-100 mb-2">
                    <h2 class="text-xl font-bold text-gray-800">Interactive World Map</h2>
                    <p class="text-sm text-gray-500 mt-1">Click on any country to view data for that location.</p>
                </div>
                <div id="map"></div>
            </div>"""

new_container = """            <!-- Left Column: World Map -->
            <div class="lg:col-span-2 bg-gray-900 p-2 rounded-xl shadow-xl border border-gray-800">
                <div class="p-4 border-b border-gray-800 mb-2">
                    <h2 class="text-xl font-bold text-white">Interactive World Map</h2>
                    <p class="text-sm text-indigo-300 mt-1">Click on any country to view data for that location.</p>
                </div>
                <div id="map"></div>
            </div>"""

content = content.replace(old_container, new_container)

# 2. Update the Globe config for a beautiful dark look
old_globe_config = """                const globe = Globe()
                    (mapElement)
                    .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-water.png')
                    .backgroundColor('#ffffff')
                    .polygonsData(data.features)
                    .polygonAltitude(0.01)
                    .polygonCapColor(() => 'rgba(165, 180, 252, 0.4)')
                    .polygonSideColor(() => 'rgba(165, 180, 252, 0.1)')
                    .polygonStrokeColor(() => '#6366f1')"""

new_globe_config = """                const globe = Globe()
                    (mapElement)
                    .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-night.jpg')
                    .bumpImageUrl('https://unpkg.com/three-globe/example/img/earth-topology.png')
                    .backgroundImageUrl('https://unpkg.com/three-globe/example/img/night-sky.png')
                    .backgroundColor('#111827')
                    .showAtmosphere(true)
                    .atmosphereColor('#4f46e5')
                    .atmosphereAltitude(0.15)
                    .polygonsData(data.features)
                    .polygonAltitude(0.015)
                    .polygonCapColor(() => 'rgba(79, 70, 229, 0.4)')
                    .polygonSideColor(() => 'rgba(79, 70, 229, 0.1)')
                    .polygonStrokeColor(() => '#818cf8')"""

content = content.replace(old_globe_config, new_globe_config)

# 3. Update the polygon hover color to match the new dark theme
old_hover = """                    .onPolygonHover(hoverD => {
                        globe
                            .polygonCapColor(d => d === hoverD ? 'rgba(99, 102, 241, 0.8)' : 'rgba(165, 180, 252, 0.4)')"""

new_hover = """                    .onPolygonHover(hoverD => {
                        globe
                            .polygonCapColor(d => d === hoverD ? 'rgba(255, 255, 255, 0.8)' : 'rgba(79, 70, 229, 0.4)')"""

content = content.replace(old_hover, new_hover)

# 4. Update the tooltip style to fit the dark theme
old_tooltip = """                        <div style="background: white; color: black; padding: 4px 8px; border-radius: 4px; font-weight: bold; border: 1px solid #ccc; font-family: sans-serif; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">"""
new_tooltip = """                        <div style="background: rgba(17, 24, 39, 0.9); color: white; padding: 6px 10px; border-radius: 6px; font-weight: bold; border: 1px solid #4f46e5; font-family: sans-serif; box-shadow: 0 4px 6px rgba(0,0,0,0.3); backdrop-filter: blur(4px);">"""
content = content.replace(old_tooltip, new_tooltip)

with open("dashboard.html", "w") as f:
    f.write(content)

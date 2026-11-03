import json
import os

# Script to build all_graphs.html dynamically connected to movies_data.js

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive Data Visualizations - Country-Filtered Analytics</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <script src="movies_data.js"></script>
    <style>
        .plot-container { width: 100%; height: 380px; }
        .chart-card { transition: box-shadow 0.2s ease, transform 0.2s ease; }
        .chart-card:hover { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04); }
        /* Custom scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
    </style>
</head>
<body class="bg-gray-50 p-4 md:p-6 font-sans text-gray-800">
    <div class="max-w-7xl mx-auto">
        <!-- Main Header -->
        <div class="mb-6 flex flex-wrap items-center justify-between gap-4 bg-white p-5 rounded-2xl shadow-sm border border-gray-100">
            <div>
                <div class="flex items-center gap-2">
                    <span class="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                    </span>
                    <h1 class="text-2xl font-black text-gray-900 tracking-tight">Movies Analytics Visualizations</h1>
                </div>
                <p class="text-xs text-gray-500 mt-1">Every chart, metric, and data table dynamically updates according to the active country selection.</p>
            </div>
            
            <div class="flex flex-wrap items-center gap-3">
                <div class="bg-indigo-50/70 border border-indigo-200/60 px-4 py-2 rounded-xl text-xs">
                    <span class="text-indigo-600 font-bold uppercase tracking-wider block text-3xs">Active Country Filter</span>
                    <span id="active-country-tag" class="text-indigo-900 font-extrabold text-sm flex items-center gap-1.5 mt-0.5">
                        <span>🌍</span> <span id="active-country-name">All Countries (Global Overview)</span>
                    </span>
                </div>
                <button id="btn-reset-filters" onclick="resetAllFilters()" class="text-xs font-bold text-gray-600 hover:text-indigo-600 bg-gray-100 hover:bg-gray-200 border border-gray-200 px-3 py-2.5 rounded-xl transition-all cursor-pointer flex items-center gap-1.5">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    <span>Reset All Filters</span>
                </button>
            </div>
        </div>

        <!-- Filter Controls Toolbar -->
        <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 mb-6 flex flex-wrap items-center justify-between gap-4 text-xs">
            <div class="flex flex-wrap items-center gap-4 flex-grow">
                <!-- Country Dropdown -->
                <div class="flex flex-col gap-1 min-w-[220px]">
                    <label class="font-bold text-gray-600 uppercase tracking-wider text-2xs">Country Selection</label>
                    <select id="country-dropdown" onchange="onCountrySelect(this.value)" class="bg-gray-50 border border-gray-300 rounded-lg px-3 py-2 font-medium text-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer">
                        <option value="ALL">🌍 All Countries (Global - 9,515 Titles)</option>
                    </select>
                </div>

                <!-- Platform Filter -->
                <div class="flex flex-col gap-1 min-w-[160px]">
                    <label class="font-bold text-gray-600 uppercase tracking-wider text-2xs">Streaming Platform</label>
                    <select id="platform-dropdown" onchange="onPlatformSelect(this.value)" class="bg-gray-50 border border-gray-300 rounded-lg px-3 py-2 font-medium text-gray-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer">
                        <option value="ALL">All Platforms</option>
                        <option value="Netflix">Netflix</option>
                        <option value="Prime Video">Prime Video</option>
                        <option value="Hulu">Hulu</option>
                        <option value="Disney+">Disney+</option>
                    </select>
                </div>

                <!-- Year Range Inputs -->
                <div class="flex flex-col gap-1">
                    <label class="font-bold text-gray-600 uppercase tracking-wider text-2xs">Release Year Range</label>
                    <div class="flex items-center gap-2">
                        <input type="number" id="min-year-input" min="1914" max="2021" value="1914" onchange="onYearChange()" class="w-20 bg-gray-50 border border-gray-300 rounded-lg px-2.5 py-1.5 text-center font-mono font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500" />
                        <span class="text-gray-400 font-bold">to</span>
                        <input type="number" id="max-year-input" min="1914" max="2021" value="2021" onchange="onYearChange()" class="w-20 bg-gray-50 border border-gray-300 rounded-lg px-2.5 py-1.5 text-center font-mono font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500" />
                    </div>
                </div>
            </div>

            <!-- Total matching count badge -->
            <div class="flex items-center gap-2">
                <span class="text-gray-500 font-medium">Matching Titles:</span>
                <span id="filtered-count-badge" class="bg-indigo-600 text-white font-black px-3 py-1 rounded-full text-xs shadow-sm">9,515</span>
            </div>
        </div>

        <!-- KPI Summary Cards Strip -->
        <div class="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between">
                <div>
                    <span class="text-2xs font-bold uppercase tracking-wider text-gray-400 block">Total Catalog Size</span>
                    <span id="kpi-total-titles" class="text-2xl font-black text-gray-900 mt-0.5 block">9,515</span>
                    <span id="kpi-total-sub" class="text-2xs text-gray-500 mt-0.5 block">100% of global library</span>
                </div>
                <div class="p-2.5 bg-blue-50 text-blue-600 rounded-xl">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z" />
                    </svg>
                </div>
            </div>

            <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between">
                <div>
                    <span class="text-2xs font-bold uppercase tracking-wider text-gray-400 block">Avg Critic Rating</span>
                    <span id="kpi-avg-rating" class="text-2xl font-black text-amber-600 mt-0.5 block">53.5 / 100</span>
                    <span id="kpi-rating-sub" class="text-2xs text-gray-500 mt-0.5 block">Rotten Tomatoes mean score</span>
                </div>
                <div class="p-2.5 bg-amber-50 text-amber-600 rounded-xl">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                    </svg>
                </div>
            </div>

            <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between">
                <div>
                    <span class="text-2xs font-bold uppercase tracking-wider text-gray-400 block">Top Platform</span>
                    <span id="kpi-top-platform" class="text-2xl font-black text-indigo-600 mt-0.5 block">Prime Video</span>
                    <span id="kpi-platform-sub" class="text-2xs text-gray-500 mt-0.5 block">4,113 titles</span>
                </div>
                <div class="p-2.5 bg-indigo-50 text-indigo-600 rounded-xl">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                </div>
            </div>

            <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-center justify-between">
                <div>
                    <span class="text-2xs font-bold uppercase tracking-wider text-gray-400 block">Dominant Demographic</span>
                    <span id="kpi-top-age" class="text-2xl font-black text-rose-600 mt-0.5 block">18+ (23.9%)</span>
                    <span id="kpi-age-sub" class="text-2xs text-gray-500 mt-0.5 block">2,276 certified films</span>
                </div>
                <div class="p-2.5 bg-rose-50 text-rose-600 rounded-xl">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                </div>
            </div>
        </div>

        <!-- No Data Available State Banner (Hidden by default) -->
        <div id="no-data-banner" class="hidden bg-amber-50 border-2 border-amber-200/80 rounded-2xl p-10 text-center my-8 shadow-sm">
            <div class="inline-flex p-3 bg-amber-100 text-amber-700 rounded-full mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
            </div>
            <h3 class="text-xl font-black text-amber-900 tracking-tight">No data available for the selected country.</h3>
            <p class="text-sm text-amber-700 max-w-lg mx-auto mt-2">
                There are no movie catalog records originating from <strong id="no-data-country-name">the selected region</strong> matching your current filter criteria in the streaming platforms dataset.
            </p>
            <div class="mt-5">
                <button onclick="resetAllFilters()" class="bg-amber-600 hover:bg-amber-700 text-white font-bold px-5 py-2.5 rounded-xl text-xs shadow transition-all cursor-pointer">
                    View All Countries (Global Catalog)
                </button>
            </div>
        </div>

        <!-- 8 Core Visualizations Grid -->
        <div id="charts-grid" class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <!-- 1. Pie Chart -->
            <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 chart-card">
                <h2 id="title-pie" class="text-base font-bold text-gray-800 text-center mb-1">1. Age Groups Distribution — Global (All Countries)</h2>
                <p class="text-2xs text-gray-400 text-center mb-3">Distribution of certified viewer age ratings</p>
                <div id="pie-chart" class="plot-container"></div>
            </div>

            <!-- 2. Bar Chart -->
            <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 chart-card">
                <h2 id="title-bar" class="text-base font-bold text-gray-800 text-center mb-1">2. Streaming Platforms Availability — Global (All Countries)</h2>
                <p class="text-2xs text-gray-400 text-center mb-3">Catalog count across Netflix, Hulu, Prime Video, and Disney+</p>
                <div id="bar-chart" class="plot-container"></div>
            </div>

            <!-- 3. Histogram -->
            <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 chart-card">
                <h2 id="title-histogram" class="text-base font-bold text-gray-800 text-center mb-1">3. Movie Releases by Year — Global (All Countries)</h2>
                <p class="text-2xs text-gray-400 text-center mb-3">Release frequency distribution across historical timeline</p>
                <div id="histogram" class="plot-container"></div>
            </div>

            <!-- 4. Line Chart -->
            <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 chart-card">
                <h2 id="title-line" class="text-base font-bold text-gray-800 text-center mb-1">4. Average Rating Trend Over Years — Global (All Countries)</h2>
                <p class="text-2xs text-gray-400 text-center mb-3">Longitudinal critic rating trajectory (Rotten Tomatoes / 100)</p>
                <div id="line-chart" class="plot-container"></div>
            </div>

            <!-- 5. Scatter Plot -->
            <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 chart-card">
                <h2 id="title-scatter" class="text-base font-bold text-gray-800 text-center mb-1">5. Release Year vs Critic Rating — Global (All Countries)</h2>
                <p class="text-2xs text-gray-400 text-center mb-3">Individual title score scatter plot (Hover to inspect title)</p>
                <div id="scatter-plot" class="plot-container"></div>
            </div>

            <!-- 6. Box Plot -->
            <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 chart-card">
                <h2 id="title-box" class="text-base font-bold text-gray-800 text-center mb-1">6. Rating Distribution by Age Group — Global (All Countries)</h2>
                <p class="text-2xs text-gray-400 text-center mb-3">Quartiles, median, and IQR score variance per certification</p>
                <div id="box-plot" class="plot-container"></div>
            </div>

            <!-- 7. Violin Plot -->
            <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 chart-card">
                <h2 id="title-violin" class="text-base font-bold text-gray-800 text-center mb-1">7. Rating Spread Across Platforms — Global (All Countries)</h2>
                <p class="text-2xs text-gray-400 text-center mb-3">Probability density of film quality per streaming service</p>
                <div id="violin-plot" class="plot-container"></div>
            </div>

            <!-- 8. Heat Map -->
            <div class="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 chart-card">
                <h2 id="title-heatmap" class="text-base font-bold text-gray-800 text-center mb-1">8. Platform vs Age Group Density — Global (All Countries)</h2>
                <p class="text-2xs text-gray-400 text-center mb-3">Cross-tabulation matrix of platform catalog focus</p>
                <div id="heat-map" class="plot-container"></div>
            </div>
        </div>

        <!-- Filtered Data Table Section -->
        <div id="table-container" class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-8">
            <div class="flex flex-wrap items-center justify-between gap-4 border-b border-gray-100 pb-4 mb-4">
                <div>
                    <h2 class="text-xl font-bold text-gray-900 flex items-center gap-2">
                        <span>Film Catalog Records</span>
                        <span id="table-country-tag" class="text-xs bg-indigo-50 text-indigo-700 font-bold px-2.5 py-0.5 rounded-full border border-indigo-200">Global Overview</span>
                    </h2>
                    <p class="text-xs text-gray-500 mt-0.5">Showing actual movie records from the filtered country dataset.</p>
                </div>
                <div class="flex items-center gap-3">
                    <input type="text" id="table-search" placeholder="Search title or director..." oninput="onTableSearch()" class="text-xs bg-gray-50 border border-gray-300 rounded-lg px-3 py-2 w-56 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
                    <span id="table-showing-badge" class="text-xs text-gray-500 font-medium">Showing 1-25</span>
                </div>
            </div>

            <div class="overflow-x-auto rounded-lg border border-gray-200">
                <table class="min-w-full divide-y divide-gray-200 text-xs text-left">
                    <thead class="bg-gray-50 text-gray-700 font-bold uppercase tracking-wider text-3xs">
                        <tr>
                            <th class="px-4 py-3">Title</th>
                            <th class="px-4 py-3">Year</th>
                            <th class="px-4 py-3">Age</th>
                            <th class="px-4 py-3">Rotten Tomatoes</th>
                            <th class="px-4 py-3">Platforms</th>
                            <th class="px-4 py-3">Top Genres</th>
                            <th class="px-4 py-3">Country</th>
                        </tr>
                    </thead>
                    <tbody id="movie-table-body" class="divide-y divide-gray-100 bg-white">
                        <!-- Populated dynamically via JS -->
                    </tbody>
                </table>
            </div>

            <!-- Table Pagination -->
            <div class="flex items-center justify-between mt-4 text-xs text-gray-600">
                <span id="table-pagination-info">Page 1</span>
                <div id="table-pagination-btns" class="flex items-center gap-1">
                    <!-- Pagination buttons -->
                </div>
            </div>
        </div>
    </div>

    <!-- Controller Script -->
    <script>
        // State
        let allMovies = window.MOVIES_DATA || [];
        let currentCountry = 'ALL';
        let currentPlatform = 'ALL';
        let currentMinYear = 1914;
        let currentMaxYear = 2021;
        let tableSearchQuery = '';
        let tablePage = 1;
        let tablePageSize = 20;
        let filteredRecords = [];

        // Plotly Layout Common Theme
        const layoutConfig = {
            margin: { t: 25, b: 45, l: 45, r: 25 },
            font: { family: 'ui-sans-serif, system-ui, -apple-system, sans-serif', size: 11, color: '#475569' },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            hovermode: 'closest',
            autosize: true
        };

        // Initialize on DOM load
        document.addEventListener('DOMContentLoaded', () => {
            initCountryDropdown();
            applyFilters();
            
            // Listen for postMessage from parent dashboard (globe clicks)
            window.addEventListener('message', (event) => {
                if (!event.data) return;
                if (event.data.action === 'setCountry') {
                    const country = event.data.country || 'ALL';
                    setCountryFilter(country, false);
                }
            });
        });

        // Initialize country dropdown with all unique countries and counts
        function initCountryDropdown() {
            const dropdown = document.getElementById('country-dropdown');
            if (!dropdown || !window.MOVIES_DATA) return;

            const countryCountMap = {};
            window.MOVIES_DATA.forEach(m => {
                if (m.countries) {
                    m.countries.forEach(c => {
                        countryCountMap[c] = (countryCountMap[c] || 0) + 1;
                    });
                }
            });

            // Sort countries by movie count descending
            const sortedCountries = Object.entries(countryCountMap)
                .sort((a, b) => b[1] - a[1]);

            let opts = `<option value="ALL">🌍 All Countries (Global - ${window.MOVIES_DATA.length.toLocaleString()} Titles)</option>`;
            sortedCountries.forEach(([country, count]) => {
                opts += `<option value="${country}">${country} (${count.toLocaleString()} movies)</option>`;
            });
            dropdown.innerHTML = opts;
        }

        // Match helper for country
        function movieMatchesCountry(m, targetCountry) {
            if (!targetCountry || targetCountry === 'ALL') return true;
            if (!m.countries || m.countries.length === 0) return false;
            
            // Direct comparison or synonym comparison
            const targetLower = targetCountry.toLowerCase();
            return m.countries.some(c => {
                const cLower = c.toLowerCase();
                if (cLower === targetLower) return true;
                if (window.COUNTRY_SYNONYMS && window.COUNTRY_SYNONYMS[targetLower] === c) return true;
                if (window.COUNTRY_SYNONYMS && window.COUNTRY_SYNONYMS[cLower] === targetCountry) return true;
                return false;
            });
        }

        // Apply all filters and update charts
        function applyFilters() {
            if (!window.MOVIES_DATA) return;

            filteredRecords = window.MOVIES_DATA.filter(m => {
                // 1. Country filter
                if (!movieMatchesCountry(m, currentCountry)) return false;

                // 2. Platform filter
                if (currentPlatform !== 'ALL') {
                    if (!m.platforms || !m.platforms.includes(currentPlatform)) return false;
                }

                // 3. Year filter
                if (m.year && (m.year < currentMinYear || m.year > currentMaxYear)) {
                    return false;
                }

                return true;
            });

            updateUI();
        }

        // Master UI Updater
        function updateUI() {
            const countryDisplayName = currentCountry === 'ALL' ? 'All Countries (Global Overview)' : currentCountry;
            const countrySuffix = currentCountry === 'ALL' ? 'Global (All Countries)' : currentCountry;

            // Update top labels and badges
            document.getElementById('active-country-name').innerText = countryDisplayName;
            document.getElementById('filtered-count-badge').innerText = filteredRecords.length.toLocaleString();
            document.getElementById('country-dropdown').value = currentCountry;
            document.getElementById('platform-dropdown').value = currentPlatform;
            document.getElementById('min-year-input').value = currentMinYear;
            document.getElementById('max-year-input').value = currentMaxYear;
            document.getElementById('table-country-tag').innerText = countryDisplayName;

            // Handle empty records state
            const noDataBanner = document.getElementById('no-data-banner');
            const chartsGrid = document.getElementById('charts-grid');
            const tableContainer = document.getElementById('table-container');

            if (filteredRecords.length === 0) {
                noDataBanner.classList.remove('hidden');
                document.getElementById('no-data-country-name').innerText = countryDisplayName;
                chartsGrid.classList.add('hidden');
                tableContainer.classList.add('hidden');
                updateKPICards(0, 0, 'N/A', 'N/A');
                return;
            } else {
                noDataBanner.classList.add('hidden');
                chartsGrid.classList.remove('hidden');
                tableContainer.classList.remove('hidden');
            }

            // Update Dynamic Titles
            document.getElementById('title-pie').innerText = `1. Age Groups Distribution — ${countrySuffix}`;
            document.getElementById('title-bar').innerText = `2. Streaming Platforms Availability — ${countrySuffix}`;
            document.getElementById('title-histogram').innerText = `3. Movie Releases by Year — ${countrySuffix}`;
            document.getElementById('title-line').innerText = `4. Average Rating Trend Over Years — ${countrySuffix}`;
            document.getElementById('title-scatter').innerText = `5. Release Year vs Critic Rating — ${countrySuffix}`;
            document.getElementById('title-box').innerText = `6. Rating Distribution by Age Group — ${countrySuffix}`;
            document.getElementById('title-violin').innerText = `7. Rating Spread Across Platforms — ${countrySuffix}`;
            document.getElementById('title-heatmap').innerText = `8. Platform vs Age Group Density — ${countrySuffix}`;

            // Aggregate metrics
            let ageCounts = {};
            let platformCounts = { "Netflix": 0, "Prime Video": 0, "Hulu": 0, "Disney+": 0 };
            let years = [];
            let ratings = [];
            let yearRatingSum = {};
            let yearCount = {};
            let heatmapData = { "Netflix": {}, "Prime Video": {}, "Hulu": {}, "Disney+": {} };

            filteredRecords.forEach(m => {
                // Age counts
                ageCounts[m.age] = (ageCounts[m.age] || 0) + 1;

                // Platforms & Heatmap
                if (m.platforms) {
                    m.platforms.forEach(p => {
                        if (platformCounts[p] !== undefined) {
                            platformCounts[p]++;
                            heatmapData[p][m.age] = (heatmapData[p][m.age] || 0) + 1;
                        }
                    });
                }

                // Years & Ratings
                if (m.year && m.year > 0) years.push(m.year);
                if (m.rating !== null && m.rating !== undefined) {
                    ratings.push(m.rating);
                    if (m.year && m.year > 0) {
                        yearRatingSum[m.year] = (yearRatingSum[m.year] || 0) + m.rating;
                        yearCount[m.year] = (yearCount[m.year] || 0) + 1;
                    }
                }
            });

            // Update KPI cards
            const avgRatingVal = ratings.length > 0 ? (ratings.reduce((a,b)=>a+b, 0) / ratings.length).toFixed(1) : 'N/A';
            const topPlat = Object.entries(platformCounts).sort((a,b)=>b[1]-a[1])[0];
            const topAge = Object.entries(ageCounts).sort((a,b)=>b[1]-a[1])[0];
            updateKPICards(filteredRecords.length, avgRatingVal, topPlat, topAge);

            // 1. Pie Chart (Age Groups)
            Plotly.react('pie-chart', [{
                values: Object.values(ageCounts),
                labels: Object.keys(ageCounts),
                type: 'pie',
                hole: 0.45,
                marker: { colors: ['#f87171', '#fbbf24', '#34d399', '#60a5fa', '#a78bfa', '#94a3b8'] },
                textinfo: 'label+percent',
                insidetextorientation: 'radial'
            }], layoutConfig);

            // 2. Bar Chart (Platforms)
            Plotly.react('bar-chart', [{
                x: Object.keys(platformCounts),
                y: Object.values(platformCounts),
                type: 'bar',
                marker: { color: ['#ef4444', '#3b82f6', '#10b981', '#8b5cf6'] },
                text: Object.values(platformCounts).map(v => v.toLocaleString()),
                textposition: 'auto'
            }], layoutConfig);

            // 3. Histogram (Release Years)
            Plotly.react('histogram', [{
                x: years,
                type: 'histogram',
                marker: { color: '#6366f1', opacity: 0.85 }
            }], {
                ...layoutConfig,
                xaxis: { title: 'Release Year' },
                yaxis: { title: 'Movie Count' }
            });

            // 4. Line Chart (Avg Rating per Year)
            const sortedYears = Object.keys(yearRatingSum).map(Number).sort((a,b) => a-b);
            const avgRatingsPerYear = sortedYears.map(y => yearRatingSum[y] / yearCount[y]);
            Plotly.react('line-chart', [{
                x: sortedYears,
                y: avgRatingsPerYear,
                type: 'scatter',
                mode: 'lines+markers',
                line: { color: '#f59e0b', width: 2.5 },
                marker: { size: 5, color: '#d97706' }
            }], {
                ...layoutConfig,
                xaxis: { title: 'Year' },
                yaxis: { title: 'Avg RT Rating (/100)', range: [0, 100] }
            });

            // 5. Scatter Plot (Year vs Rating)
            // Limit to 1000 for smooth rendering if global
            const scatterSubset = filteredRecords.length > 1000 
                ? [...filteredRecords].sort(() => 0.5 - Math.random()).slice(0, 1000) 
                : filteredRecords;
            const validScatter = scatterSubset.filter(m => m.year > 0 && m.rating !== null);

            Plotly.react('scatter-plot', [{
                x: validScatter.map(m => m.year),
                y: validScatter.map(m => m.rating),
                mode: 'markers',
                type: 'scatter',
                text: validScatter.map(m => `${m.title} (${m.year})<br>Rating: ${m.rating}/100<br>Age: ${m.age}`),
                marker: { size: 6, color: '#ec4899', opacity: 0.65 }
            }], {
                ...layoutConfig,
                xaxis: { title: 'Release Year' },
                yaxis: { title: 'Rotten Tomatoes Score', range: [0, 105] }
            });

            // 6. Box Plot (Rating by Age)
            const boxData = Object.keys(ageCounts).map(age => ({
                y: filteredRecords.filter(m => m.age === age && m.rating !== null).map(m => m.rating),
                type: 'box',
                name: age,
                boxpoints: 'outliers'
            }));
            Plotly.react('box-plot', boxData, {
                ...layoutConfig,
                yaxis: { title: 'Score Distribution' }
            });

            // 7. Violin Plot (Rating by Platform)
            const violinData = Object.keys(platformCounts).map(plat => ({
                y: filteredRecords.filter(m => m.platforms && m.platforms.includes(plat) && m.rating !== null).map(m => m.rating),
                type: 'violin',
                name: plat,
                box: { visible: true },
                meanline: { visible: true },
                line: { color: plat === 'Netflix' ? '#ef4444' : plat === 'Prime Video' ? '#3b82f6' : plat === 'Hulu' ? '#10b981' : '#8b5cf6' }
            }));
            Plotly.react('violin-plot', violinData, {
                ...layoutConfig,
                yaxis: { title: 'Rating Spread' }
            });

            // 8. Heat Map (Platform vs Age)
            const hmAges = Object.keys(ageCounts);
            const hmPlats = Object.keys(platformCounts);
            const zMatrix = hmPlats.map(p => hmAges.map(a => heatmapData[p][a] || 0));

            Plotly.react('heat-map', [{
                z: zMatrix,
                x: hmAges,
                y: hmPlats,
                type: 'heatmap',
                colorscale: 'Viridis'
            }], {
                ...layoutConfig,
                xaxis: { title: 'Age Group' }
            });

            // Render Table
            tablePage = 1;
            renderMovieTable();
        }

        // KPI cards updater
        function updateKPICards(total, avgRating, topPlat, topAge) {
            document.getElementById('kpi-total-titles').innerText = total.toLocaleString();
            document.getElementById('kpi-total-sub').innerText = currentCountry === 'ALL' 
                ? '100% of global library' 
                : `${((total / (window.MOVIES_DATA.length || 1)) * 100).toFixed(1)}% of total library`;

            document.getElementById('kpi-avg-rating').innerText = avgRating !== 'N/A' ? `${avgRating} / 100` : 'N/A';
            
            if (topPlat && topPlat[0]) {
                document.getElementById('kpi-top-platform').innerText = topPlat[0];
                document.getElementById('kpi-platform-sub').innerText = `${topPlat[1].toLocaleString()} titles available`;
            } else {
                document.getElementById('kpi-top-platform').innerText = 'N/A';
                document.getElementById('kpi-platform-sub').innerText = '0 titles';
            }

            if (topAge && topAge[0]) {
                const pct = total > 0 ? ((topAge[1] / total) * 100).toFixed(1) : 0;
                document.getElementById('kpi-top-age').innerText = `${topAge[0]} (${pct}%)`;
                document.getElementById('kpi-age-sub').innerText = `${topAge[1].toLocaleString()} titles`;
            } else {
                document.getElementById('kpi-top-age').innerText = 'N/A';
                document.getElementById('kpi-age-sub').innerText = '0 titles';
            }
        }

        // Table search and render
        function onTableSearch() {
            tableSearchQuery = (document.getElementById('table-search').value || '').toLowerCase().trim();
            tablePage = 1;
            renderMovieTable();
        }

        function renderMovieTable() {
            const tbody = document.getElementById('movie-table-body');
            if (!tbody) return;

            let displayed = filteredRecords;
            if (tableSearchQuery) {
                displayed = filteredRecords.filter(m => 
                    m.title.toLowerCase().includes(tableSearchQuery) || 
                    (m.directors && m.directors.toLowerCase().includes(tableSearchQuery)) ||
                    (m.genres && m.genres.some(g => g.toLowerCase().includes(tableSearchQuery)))
                );
            }

            const total = displayed.length;
            const startIdx = (tablePage - 1) * tablePageSize;
            const pageRecords = displayed.slice(startIdx, startIdx + tablePageSize);

            document.getElementById('table-showing-badge').innerText = total > 0 
                ? `Showing ${startIdx + 1}-${Math.min(startIdx + tablePageSize, total)} of ${total.toLocaleString()}` 
                : 'Showing 0 records';

            if (pageRecords.length === 0) {
                tbody.innerHTML = `<tr><td colspan="7" class="px-4 py-8 text-center text-gray-400">No matching movie records found.</td></tr>`;
                document.getElementById('table-pagination-btns').innerHTML = '';
                return;
            }

            tbody.innerHTML = pageRecords.map(m => `
                <tr class="hover:bg-indigo-50/30 transition-colors">
                    <td class="px-4 py-3 font-semibold text-gray-900">
                        ${m.title}
                        ${m.directors ? `<span class="block text-3xs text-gray-400 font-normal">Dir: ${m.directors}</span>` : ''}
                    </td>
                    <td class="px-4 py-3 text-gray-600 font-mono">${m.year || '—'}</td>
                    <td class="px-4 py-3">
                        <span class="px-2 py-0.5 rounded-full text-3xs font-bold ${
                            m.age === '18+' ? 'bg-red-100 text-red-800' :
                            m.age === '13+' ? 'bg-amber-100 text-amber-800' :
                            m.age === '7+' ? 'bg-green-100 text-green-800' :
                            m.age === 'all' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-700'
                        }">
                            ${m.age}
                        </span>
                    </td>
                    <td class="px-4 py-3 font-bold ${m.rating >= 80 ? 'text-green-600' : m.rating >= 60 ? 'text-blue-600' : 'text-amber-600'}">
                        ${m.rating !== null ? m.rating + '/100' : '—'}
                    </td>
                    <td class="px-4 py-3">
                        <div class="flex flex-wrap gap-1">
                            ${(m.platforms || []).map(p => `
                                <span class="px-1.5 py-0.5 rounded text-3xs font-medium ${
                                    p === 'Netflix' ? 'bg-red-50 text-red-700 border border-red-200' :
                                    p === 'Prime Video' ? 'bg-blue-50 text-blue-700 border border-blue-200' :
                                    p === 'Hulu' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' :
                                    'bg-indigo-50 text-indigo-700 border border-indigo-200'
                                }">${p}</span>
                            `).join('')}
                        </div>
                    </td>
                    <td class="px-4 py-3 text-gray-600">
                        ${(m.genres || []).slice(0, 3).join(', ') || '—'}
                    </td>
                    <td class="px-4 py-3 text-gray-700 font-medium">
                        ${(m.countries || []).slice(0, 2).join(', ') || 'Unknown'}
                    </td>
                </tr>
            `).join('');

            // Pagination Controls
            const totalPages = Math.ceil(total / tablePageSize) || 1;
            document.getElementById('table-pagination-info').innerText = `Page ${tablePage} of ${totalPages}`;

            let btns = '';
            btns += `<button onclick="goTablePage(1)" ${tablePage === 1 ? 'disabled class="px-2 py-1 bg-gray-100 text-gray-400 rounded cursor-not-allowed"' : 'class="px-2 py-1 bg-white border border-gray-200 hover:bg-gray-50 rounded"'}>&laquo;</button>`;
            btns += `<button onclick="goTablePage(${tablePage - 1})" ${tablePage === 1 ? 'disabled class="px-2 py-1 bg-gray-100 text-gray-400 rounded cursor-not-allowed"' : 'class="px-2 py-1 bg-white border border-gray-200 hover:bg-gray-50 rounded"'}>Prev</button>`;

            const startP = Math.max(1, tablePage - 2);
            const endP = Math.min(totalPages, startP + 4);
            for (let p = startP; p <= endP; p++) {
                btns += `<button onclick="goTablePage(${p})" class="px-2.5 py-1 rounded font-medium ${p === tablePage ? 'bg-indigo-600 text-white font-bold' : 'bg-white border border-gray-200 hover:bg-gray-50 text-gray-700'}">${p}</button>`;
            }

            btns += `<button onclick="goTablePage(${tablePage + 1})" ${tablePage === totalPages ? 'disabled class="px-2 py-1 bg-gray-100 text-gray-400 rounded cursor-not-allowed"' : 'class="px-2 py-1 bg-white border border-gray-200 hover:bg-gray-50 rounded"'}>Next</button>`;
            btns += `<button onclick="goTablePage(${totalPages})" ${tablePage === totalPages ? 'disabled class="px-2 py-1 bg-gray-100 text-gray-400 rounded cursor-not-allowed"' : 'class="px-2 py-1 bg-white border border-gray-200 hover:bg-gray-50 rounded"'}>&raquo;</button>`;

            document.getElementById('table-pagination-btns').innerHTML = btns;
        }

        function goTablePage(p) {
            tablePage = p;
            renderMovieTable();
        }

        // Country selection handler (from dropdown or postMessage)
        function setCountryFilter(country, notifyParent = true) {
            currentCountry = country || 'ALL';
            applyFilters();

            if (notifyParent && window.parent && window.parent !== window) {
                window.parent.postMessage({
                    action: 'countrySelectedInGraphs',
                    country: currentCountry === 'ALL' ? 'Global' : currentCountry
                }, '*');
            }
        }

        function onCountrySelect(val) {
            setCountryFilter(val, true);
        }

        function onPlatformSelect(val) {
            currentPlatform = val;
            applyFilters();
        }

        function onYearChange() {
            const minInput = parseInt(document.getElementById('min-year-input').value) || 1914;
            const maxInput = parseInt(document.getElementById('max-year-input').value) || 2021;
            currentMinYear = Math.min(minInput, maxInput);
            currentMaxYear = Math.max(minInput, maxInput);
            applyFilters();
        }

        function resetAllFilters() {
            currentCountry = 'ALL';
            currentPlatform = 'ALL';
            currentMinYear = 1914;
            currentMaxYear = 2021;
            tableSearchQuery = '';
            document.getElementById('table-search').value = '';
            setCountryFilter('ALL', true);
        }
    </script>
</body>
</html>
"""

with open("all_graphs.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Generated dynamic all_graphs.html successfully.")

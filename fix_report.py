import re

with open("dashboard.html", "r") as f:
    content = f.read()

new_report = """            <div id="missing-values-report" class="hidden mt-4 p-6 bg-white border border-gray-200 rounded-xl shadow-lg transition-all duration-300">
                <div class="flex justify-between items-start border-b pb-2 mb-4">
                    <h3 class="text-xl font-bold text-gray-800">Comprehensive Missing Values Report</h3>
                    <button onclick="document.getElementById('missing-values-report').classList.add('hidden')" class="text-gray-400 hover:text-gray-600">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                    </button>
                </div>
                
                <h4 class="text-md font-semibold text-gray-600 mb-3 uppercase tracking-wide">1. Missing Data Summary</h4>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div class="bg-red-50 p-4 rounded-lg border border-red-200">
                        <p class="text-xs font-bold text-red-800 uppercase mb-1">Total Rows Affected</p>
                        <p class="text-2xl font-black text-red-600">4,177</p>
                        <p class="text-xs text-red-500 mt-1">43.9% of all 9,515 movies</p>
                    </div>
                    <div class="bg-orange-50 p-4 rounded-lg border border-orange-200">
                        <p class="text-xs font-bold text-orange-800 uppercase mb-1">Columns with Missing Data</p>
                        <p class="text-2xl font-black text-orange-600">2 <span class="text-sm font-normal">/ 11</span></p>
                        <p class="text-xs text-orange-600 mt-1">Age & Rotten Tomatoes</p>
                    </div>
                    <div class="bg-green-50 p-4 rounded-lg border border-green-200">
                        <p class="text-xs font-bold text-green-800 uppercase mb-1">Complete Columns</p>
                        <p class="text-2xl font-black text-green-600">9 <span class="text-sm font-normal">/ 11</span></p>
                        <p class="text-xs text-green-600 mt-1">Title, Year, Platforms, etc.</p>
                    </div>
                    <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
                        <p class="text-xs font-bold text-blue-800 uppercase mb-1">Data Quality Post-Cleaning</p>
                        <p class="text-2xl font-black text-blue-600">100%</p>
                        <p class="text-xs text-blue-600 mt-1">Clean dataset: 5,338 movies</p>
                    </div>
                </div>

                <h4 class="text-md font-semibold text-gray-600 mb-3 uppercase tracking-wide">2. Detailed Column Data & Value Types Analysis</h4>
                <div class="bg-white border border-gray-200 rounded-lg overflow-hidden mb-6">
                    <table class="min-w-full divide-y divide-gray-200 text-sm">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data Attribute (Column)</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Missing Statistics</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Value Types Stored & Missing Context</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr>
                                <td class="px-6 py-4 whitespace-nowrap font-bold text-gray-900">Age Demographic</td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span class="text-red-600 font-bold block text-lg">4,177 Missing</span>
                                    <span class="text-gray-500 text-xs">(43.9% of Dataset)</span>
                                </td>
                                <td class="px-6 py-4 text-gray-700 text-sm">
                                    <p class="mb-2"><strong>Data Types Stored:</strong> This column stores categorical age ratings indicating the target audience for the movie.</p>
                                    <p class="mb-2"><strong>Valid Values Found:</strong> <span class="bg-gray-100 px-2 py-1 rounded border">18+</span>, <span class="bg-gray-100 px-2 py-1 rounded border">16+</span>, <span class="bg-gray-100 px-2 py-1 rounded border">13+</span>, <span class="bg-gray-100 px-2 py-1 rounded border">7+</span>, <span class="bg-gray-100 px-2 py-1 rounded border">all</span></p>
                                    <p class="text-gray-500 italic text-xs">Why missing? Many streaming platforms do not enforce or publicly list standardized maturity ratings (like TV-MA or R) for older, obscure, or internationally licensed movies, leaving this field entirely blank.</p>
                                </td>
                            </tr>
                            <tr>
                                <td class="px-6 py-4 whitespace-nowrap font-bold text-gray-900">Rotten Tomatoes Rating</td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span class="text-orange-600 font-bold block text-lg">7 Missing</span>
                                    <span class="text-gray-500 text-xs">(0.07% of Dataset)</span>
                                </td>
                                <td class="px-6 py-4 text-gray-700 text-sm">
                                    <p class="mb-2"><strong>Data Types Stored:</strong> This column stores critic review scores formatted as fractions out of 100.</p>
                                    <p class="mb-2"><strong>Valid Values Found:</strong> Ranging from <span class="bg-gray-100 px-2 py-1 rounded border">10/100</span> to <span class="bg-gray-100 px-2 py-1 rounded border">100/100</span> (e.g., 98/100, 43/100, etc.)</p>
                                    <p class="text-gray-500 italic text-xs">Why missing? These 7 specific movies likely did not receive enough critic reviews to generate an aggregate score on Rotten Tomatoes.</p>
                                </td>
                            </tr>
                            <tr class="bg-green-50">
                                <td class="px-6 py-4 whitespace-nowrap font-bold text-gray-900">Movie Metadata<br><span class="text-xs text-gray-500 font-normal">(ID, Title, Year)</span></td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span class="text-green-700 font-bold block text-lg">0 Missing</span>
                                    <span class="text-gray-500 text-xs">(100% Complete)</span>
                                </td>
                                <td class="px-6 py-4 text-gray-700 text-sm">
                                    <p class="mb-1"><strong>Data Types Stored:</strong></p>
                                    <ul class="list-disc list-inside text-xs text-gray-600">
                                        <li><strong>ID:</strong> Unique numerical identifier (e.g., 1, 2, 3...)</li>
                                        <li><strong>Title:</strong> Full movie string name (e.g., "The Irishman")</li>
                                        <li><strong>Year:</strong> 4-digit release year (e.g., 2019, 2001)</li>
                                    </ul>
                                </td>
                            </tr>
                            <tr class="bg-green-50">
                                <td class="px-6 py-4 whitespace-nowrap font-bold text-gray-900">Streaming Platforms<br><span class="text-xs text-gray-500 font-normal">(Netflix, Hulu, Prime, Disney+)</span></td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span class="text-green-700 font-bold block text-lg">0 Missing</span>
                                    <span class="text-gray-500 text-xs">(100% Complete)</span>
                                </td>
                                <td class="px-6 py-4 text-gray-700 text-sm">
                                    <p class="mb-2"><strong>Data Types Stored:</strong> Binary integer indicators showing availability.</p>
                                    <p class="mb-2"><strong>Valid Values Found:</strong> <span class="bg-gray-100 px-2 py-1 rounded border">1</span> (Available) or <span class="bg-gray-100 px-2 py-1 rounded border">0</span> (Not Available)</p>
                                </td>
                            </tr>
                            <tr class="bg-green-50">
                                <td class="px-6 py-4 whitespace-nowrap font-bold text-gray-900">Content Type</td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span class="text-green-700 font-bold block text-lg">0 Missing</span>
                                    <span class="text-gray-500 text-xs">(100% Complete)</span>
                                </td>
                                <td class="px-6 py-4 text-gray-700 text-sm">
                                    <p class="mb-2"><strong>Data Types Stored:</strong> Categorical binary indicator separating movies from TV shows.</p>
                                    <p class="mb-2"><strong>Valid Values Found:</strong> <span class="bg-gray-100 px-2 py-1 rounded border">0</span> (representing Movie)</p>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
                <h4 class="text-md font-semibold text-gray-600 mb-3 uppercase tracking-wide">3. Resolution & Imputation Formula</h4>
                <div class="bg-gray-50 p-5 rounded-lg border border-gray-200">
                    <div class="flex items-center gap-2 mb-3">
                        <span class="font-mono text-sm text-indigo-700 bg-indigo-50 px-3 py-1 rounded border border-indigo-100 font-bold">Formula: Listwise Deletion (Strict Row Removal)</span>
                    </div>
                    <p class="text-gray-700 text-sm mb-3">
                        Rather than attempting to guess or synthesize fake data (mean imputation), we applied a strict <strong>Listwise Deletion</strong> formula. Any movie row containing a blank cell in either the <strong>Age</strong> or <strong>Rotten Tomatoes</strong> column was completely excised from the visual dataset.
                    </p>
                    <p class="text-gray-700 text-sm">
                        <strong>Final Cleaned Result:</strong> The interactive globe and charts now run exclusively on a 100% complete, fully normalized subset of <strong class="text-green-600 text-lg">5,338</strong> movies, ensuring all visualizations are based on highly accurate data.
                    </p>
                </div>
            </div>"""

content = re.sub(r'<div id="missing-values-report".*?</div>\s*</div>\s*</div>\s*<!-- Dashboard Main: Map & Data Panel -->', 
                 new_report + "\n        </div>\n\n        <!-- Dashboard Main: Map & Data Panel -->", 
                 content, 
                 flags=re.DOTALL)

with open("dashboard.html", "w") as f:
    f.write(content)

print("Updated successfully")

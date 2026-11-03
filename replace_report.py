with open("dashboard.html", "r") as f:
    content = f.read()

import re

new_report = """            <div id="missing-values-report" class="hidden mt-4 p-6 bg-white border border-gray-200 rounded-xl shadow-lg transition-all duration-300">
                <div class="flex justify-between items-start border-b pb-2 mb-4">
                    <h3 class="text-xl font-bold text-gray-800">Comprehensive Missing Values Report</h3>
                    <button onclick="document.getElementById('missing-values-report').classList.add('hidden')" class="text-gray-400 hover:text-gray-600">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                    </button>
                </div>
                
                <h4 class="text-md font-semibold text-gray-600 mb-3 uppercase tracking-wide">1. Missing Data Breakdown</h4>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div class="bg-red-50 p-4 rounded-lg border border-red-200">
                        <p class="text-xs font-bold text-red-800 uppercase mb-1">Movie Rows Missing</p>
                        <p class="text-2xl font-black text-red-600">4,177</p>
                        <p class="text-xs text-red-500 mt-1">43.9% of all 9,515 movies</p>
                    </div>
                    <div class="bg-orange-50 p-4 rounded-lg border border-orange-200">
                        <p class="text-xs font-bold text-orange-800 uppercase mb-1">Columns Missing</p>
                        <p class="text-2xl font-black text-orange-600">2 <span class="text-sm font-normal">/ 11</span></p>
                        <p class="text-xs text-orange-600 mt-1">Age & Rotten Tomatoes</p>
                    </div>
                    <div class="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                        <p class="text-xs font-bold text-yellow-800 uppercase mb-1">Age Missing Values</p>
                        <p class="text-2xl font-black text-yellow-600">4,177</p>
                        <p class="text-xs text-yellow-600 mt-1">The primary missing factor</p>
                    </div>
                    <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
                        <p class="text-xs font-bold text-blue-800 uppercase mb-1">Rotten Tomatoes Missing</p>
                        <p class="text-2xl font-black text-blue-600">7</p>
                        <p class="text-xs text-blue-600 mt-1">All 7 also missing Age</p>
                    </div>
                </div>
                
                <h4 class="text-md font-semibold text-gray-600 mb-3 uppercase tracking-wide">2. Resolution & Imputation Formula</h4>
                <div class="bg-gray-50 p-5 rounded-lg border border-gray-200">
                    <div class="flex items-center gap-2 mb-3">
                        <span class="font-mono text-sm text-indigo-700 bg-indigo-50 px-3 py-1 rounded border border-indigo-100 font-bold">Formula: Listwise Deletion (Strict Row Removal)</span>
                    </div>
                    <p class="text-gray-700 text-sm mb-3">
                        Rather than attempting to guess or synthesize fake data (mean imputation), we applied a strict <strong>Listwise Deletion</strong> formula. Any movie row containing a blank cell in either the <strong>Age</strong> or <strong>Rotten Tomatoes</strong> column was completely excised from the visual dataset.
                    </p>
                    <div class="bg-gray-800 text-green-400 p-3 rounded font-mono text-xs mb-3 overflow-x-auto">
                        # Applied in Python Pipeline:<br>
                        if not row.get("Age") or not row.get("Rotten Tomatoes"):<br>
                        &nbsp;&nbsp;&nbsp;&nbsp;continue  # Drop entire movie row
                    </div>
                    <p class="text-gray-700 text-sm">
                        <strong>Final Cleaned Result:</strong> The interactive globe and charts now run exclusively on a 100% complete, fully normalized subset of <strong class="text-green-600 text-lg">5,338</strong> movies.
                    </p>
                </div>
            </div>"""

content = re.sub(r'<div id="missing-values-report".*?</div>\s*</div>\s*</div>\s*<!-- Dashboard Main: Map & Data Panel -->', 
                 new_report + "\n        </div>\n\n        <!-- Dashboard Main: Map & Data Panel -->", 
                 content, 
                 flags=re.DOTALL)

with open("dashboard.html", "w") as f:
    f.write(content)
print("Updated successfully.")

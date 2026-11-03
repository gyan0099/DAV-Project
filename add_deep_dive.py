import re

with open("dashboard.html", "r") as f:
    content = f.read()

deep_dive_html = """
                <h4 class="text-md font-semibold text-gray-600 mb-3 mt-6 uppercase tracking-wide">4. Deep-Dive: Missing Data Patterns & Examples</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <!-- Missing By Platform -->
                    <div class="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
                        <h5 class="font-bold text-gray-800 border-b pb-2 mb-3">Where is 'Age' Missing Most? (By Platform)</h5>
                        <p class="text-xs text-gray-500 mb-4">Movies missing Age demographics are highly concentrated on Prime Video and Netflix.</p>
                        
                        <div class="space-y-3">
                            <div>
                                <div class="flex justify-between text-xs mb-1"><span class="font-bold text-blue-800">Prime Video</span> <span class="text-gray-600">1,948 movies</span></div>
                                <div class="w-full bg-gray-200 rounded-full h-2"><div class="bg-blue-500 h-2 rounded-full" style="width: 46%"></div></div>
                            </div>
                            <div>
                                <div class="flex justify-between text-xs mb-1"><span class="font-bold text-red-800">Netflix</span> <span class="text-gray-600">1,797 movies</span></div>
                                <div class="w-full bg-gray-200 rounded-full h-2"><div class="bg-red-500 h-2 rounded-full" style="width: 43%"></div></div>
                            </div>
                            <div>
                                <div class="flex justify-between text-xs mb-1"><span class="font-bold text-green-800">Hulu</span> <span class="text-gray-600">329 movies</span></div>
                                <div class="w-full bg-gray-200 rounded-full h-2"><div class="bg-green-500 h-2 rounded-full" style="width: 8%"></div></div>
                            </div>
                            <div>
                                <div class="flex justify-between text-xs mb-1"><span class="font-bold text-indigo-800">Disney+</span> <span class="text-gray-600">197 movies</span></div>
                                <div class="w-full bg-gray-200 rounded-full h-2"><div class="bg-indigo-500 h-2 rounded-full" style="width: 4%"></div></div>
                            </div>
                        </div>
                    </div>

                    <!-- Examples of Missing Data -->
                    <div class="bg-white border border-gray-200 rounded-lg p-5 shadow-sm">
                        <h5 class="font-bold text-gray-800 border-b pb-2 mb-3">Real Examples from the Dataset</h5>
                        <p class="text-xs text-gray-500 mb-3">A look at actual movies where values were omitted by the platforms.</p>
                        
                        <div class="bg-gray-50 rounded p-3 mb-3 border border-gray-100">
                            <span class="text-xs font-bold text-gray-700 block mb-1">Titles Missing 'Age' Demographics:</span>
                            <ul class="list-disc list-inside text-xs text-gray-600 space-y-1">
                                <li>On Body and Soul (2017) - <em>Foreign/Indie</em></li>
                                <li>Special 26 (2013) - <em>International</em></li>
                                <li>Chasing Coral (2017) - <em>Documentary</em></li>
                                <li class="italic text-gray-500 list-none mt-1">(Most missing ages are concentrated in the 2010s era)</li>
                            </ul>
                        </div>

                        <div class="bg-gray-50 rounded p-3 border border-gray-100">
                            <span class="text-xs font-bold text-gray-700 block mb-1">Titles Missing 'Rotten Tomatoes':</span>
                            <ul class="list-disc list-inside text-xs text-gray-600 space-y-1">
                                <li>Amit Tandon: Family Tandoncies (2019)</li>
                                <li>ChuChuTV Bedtime Stories... (2019)</li>
                                <li class="italic text-gray-500 list-none mt-1">(These 7 are highly niche: Stand-up specials & Kids content)</li>
                            </ul>
                        </div>
                    </div>
                </div>
"""

# We need to insert this right before the closing </div> of the missing-values-report
# Let's find the "3. Resolution & Imputation Formula" and insert after its closing div

pattern = r'(<h4 class="text-md font-semibold text-gray-600 mb-3 uppercase tracking-wide">3\. Resolution & Imputation Formula</h4>.*?</div>)(\s*</div>\s*</div>\s*<!-- Dashboard Main: Map & Data Panel -->)'

new_content = re.sub(pattern, r'\1' + deep_dive_html + r'\2', content, flags=re.DOTALL)

with open("dashboard.html", "w") as f:
    f.write(new_content)

print("Added deep dive section")

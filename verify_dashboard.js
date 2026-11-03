const puppeteer = require('puppeteer');
const http = require('http');
const fs = require('fs');
const path = require('path');

// Simple static server
const server = http.createServer((req, res) => {
    let filePath = path.join(__dirname, decodeURIComponent(req.url.split('?')[0]));
    if (filePath.endsWith('/') || filePath === __dirname) filePath = path.join(filePath, 'dashboard.html');
    if (!fs.existsSync(filePath)) {
        res.writeHead(404);
        return res.end('Not found: ' + filePath);
    }
    const ext = path.extname(filePath);
    const mime = {
        '.html': 'text/html',
        '.js': 'text/javascript',
        '.css': 'text/css',
        '.json': 'application/json',
        '.png': 'image/png'
    }[ext] || 'text/plain';
    res.writeHead(200, { 'Content-Type': mime });
    fs.createReadStream(filePath).pipe(res);
});

server.listen(8091, async () => {
    console.log('Server running on http://localhost:8091');
    try {
        const browser = await puppeteer.launch({
            headless: 'new',
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();
        await page.setViewport({ width: 1400, height: 1200 });

        console.log('Navigating to dashboard...');
        await page.goto('http://localhost:8091/dashboard.html', { waitUntil: 'networkidle0', timeout: 30000 });

        // Check Initial Global State
        const initialLoc = await page.$eval('#selected-location', el => el.innerText);
        const tagAge = await page.$eval('#tag-age', el => el.innerText);
        const tagNetflix = await page.$eval('#tag-netflix', el => el.innerText);
        const tagTotal = await page.$eval('#tag-total-catalog', el => el.innerText);
        console.log('Initial Location:', initialLoc);
        console.log('Initial Demographics:', tagAge);
        console.log('Initial Netflix:', tagNetflix);
        console.log('Initial Total Catalog:', tagTotal);

        // Test 1: Select India via updateLocationStats('India')
        console.log('\n--- Testing Country Selection: India ---');
        await page.evaluate(() => updateLocationStats('India'));
        await new Promise(r => setTimeout(r, 1200));

        const indiaLoc = await page.$eval('#selected-location', el => el.innerText);
        const indiaAge = await page.$eval('#tag-age', el => el.innerText);
        const indiaNf = await page.$eval('#tag-netflix', el => el.innerText);
        const indiaPv = await page.$eval('#tag-prime', el => el.innerText);
        const indiaRating = await page.$eval('#tag-rating', el => el.innerText);
        const indiaG1 = await page.$eval('#tag-genre1', el => el.innerText);
        const indiaCountBadge = await page.$eval('#selected-count-badge', el => el.innerText);
        console.log('India Location:', indiaLoc);
        console.log('India Count Badge:', indiaCountBadge);
        console.log('India Demographics:', indiaAge);
        console.log('India Netflix:', indiaNf);
        console.log('India Prime Video:', indiaPv);
        console.log('India Rating:', indiaRating);
        console.log('India Top Genre:', indiaG1);

        // Check iframe charts for India
        const iframeHandle = await page.$('#graphs-iframe');
        const frame = await iframeHandle.contentFrame();
        const frameCountry = await frame.$eval('#active-country-name', el => el.innerText);
        const frameCount = await frame.$eval('#filtered-count-badge', el => el.innerText);
        const framePieTitle = await frame.$eval('#title-pie', el => el.innerText);
        const frameBarTitle = await frame.$eval('#title-bar', el => el.innerText);
        const frameLineTitle = await frame.$eval('#title-line', el => el.innerText);
        const frameKpiTotal = await frame.$eval('#kpi-total-titles', el => el.innerText);
        console.log('Iframe Country:', frameCountry);
        console.log('Iframe Count Badge:', frameCount);
        console.log('Iframe KPI Total Titles:', frameKpiTotal);
        console.log('Iframe Pie Title:', framePieTitle);
        console.log('Iframe Bar Title:', frameBarTitle);
        console.log('Iframe Line Title:', frameLineTitle);

        // Test 2: Select United States
        console.log('\n--- Testing Country Selection: United States ---');
        await page.evaluate(() => updateLocationStats('United States of America'));
        await new Promise(r => setTimeout(r, 1200));

        const usLoc = await page.$eval('#selected-location', el => el.innerText);
        const usNf = await page.$eval('#tag-netflix', el => el.innerText);
        const usPv = await page.$eval('#tag-prime', el => el.innerText);
        const usFrameCountry = await frame.$eval('#active-country-name', el => el.innerText);
        const usFrameCount = await frame.$eval('#filtered-count-badge', el => el.innerText);
        const usFrameTitle = await frame.$eval('#title-line', el => el.innerText);
        console.log('US Location:', usLoc);
        console.log('US Netflix:', usNf);
        console.log('US Prime Video:', usPv);
        console.log('US Iframe Country:', usFrameCountry);
        console.log('US Iframe Matching Titles:', usFrameCount);
        console.log('US Iframe Line Chart Title:', usFrameTitle);

        // Test 3: Select Japan
        console.log('\n--- Testing Country Selection: Japan ---');
        await page.evaluate(() => updateLocationStats('Japan'));
        await new Promise(r => setTimeout(r, 1200));

        const japanLoc = await page.$eval('#selected-location', el => el.innerText);
        const japanFrameCountry = await frame.$eval('#active-country-name', el => el.innerText);
        const japanFrameCount = await frame.$eval('#filtered-count-badge', el => el.innerText);
        const japanFrameTitle = await frame.$eval('#title-scatter', el => el.innerText);
        console.log('Japan Location:', japanLoc);
        console.log('Japan Iframe Country:', japanFrameCountry);
        console.log('Japan Iframe Matching Titles:', japanFrameCount);
        console.log('Japan Iframe Scatter Title:', japanFrameTitle);

        // Test 4: Select No-Data Country (e.g. Greenland)
        console.log('\n--- Testing Country Selection: Greenland (No data) ---');
        await page.evaluate(() => updateLocationStats('Greenland'));
        await new Promise(r => setTimeout(r, 1200));

        const glLoc = await page.$eval('#selected-location', el => el.innerText);
        const glNotice = await page.$eval('#no-data-notice', el => el.innerText);
        const glFrameBanner = await frame.$eval('#no-data-banner', el => el.classList.contains('hidden') ? 'Hidden' : 'Visible');
        console.log('Greenland Location:', glLoc);
        console.log('Greenland Notice:', glNotice.split('\n')[0]);
        console.log('Greenland Frame No-Data Banner:', glFrameBanner);

        // Test 5: Reset to Global
        console.log('\n--- Testing Reset to Global ---');
        await page.evaluate(() => updateLocationStats('Global'));
        await new Promise(r => setTimeout(r, 1200));

        const resetLoc = await page.$eval('#selected-location', el => el.innerText);
        const resetCount = await frame.$eval('#filtered-count-badge', el => el.innerText);
        console.log('Reset Location:', resetLoc);
        console.log('Reset Matching Titles:', resetCount);

        // Take high-res screenshots
        console.log('\n--- Capturing Screenshots ---');
        await page.evaluate(() => updateLocationStats('India'));
        await new Promise(r => setTimeout(r, 1500));
        await page.screenshot({ path: 'screenshot_dashboard_india.png', fullPage: true });
        console.log('Captured screenshot_dashboard_india.png');

        await page.evaluate(() => updateLocationStats('Global'));
        await new Promise(r => setTimeout(r, 1500));
        await page.screenshot({ path: 'screenshot.png', fullPage: true });
        console.log('Updated screenshot.png');

        await browser.close();
        server.close();
        console.log('\nAll verification tests completed successfully!');
        process.exit(0);
    } catch (err) {
        console.error('Test error:', err);
        server.close();
        process.exit(1);
    }
});

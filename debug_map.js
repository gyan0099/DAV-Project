const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch({headless: "new"});
    const page = await browser.newPage();
    page.on('console', msg => console.log('LOG:', msg.text()));
    page.on('requestfailed', request => {
      console.log(`Failed request: ${request.url()} - ${request.failure().errorText}`);
    });
    page.on('response', response => {
      if (!response.ok()) {
        console.log(`Error response: ${response.url()} - ${response.status()}`);
      }
    });
    await page.setViewport({width: 1200, height: 800});
    await page.goto('http://localhost:8000/dashboard.html', {waitUntil: 'networkidle0'});
    await page.screenshot({path: 'screenshot.png'});
    await browser.close();
})();

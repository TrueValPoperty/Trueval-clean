require('dotenv').config();
const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto('https://www.zoopla.co.uk/for-sale/property/cornwall/?q=Cornwall&results_sort=newest_listings', { waitUntil: 'networkidle2' });

    const properties = await page.evaluate(() => {
        const listings = [];
        const items = document.querySelectorAll('.dkr2t82');
        items.forEach(el => {
            const title = el.querySelector('h2')?.innerText || '';
            const price = el.querySelector('._1egbt4s3r p:last-child')?.innerText || '';
            const address = el.querySelector('address')?.innerText || '';
            const link = el.querySelector('a')?.href || '';
            listings.push({ title, price, address, link });
        });
        return listings;
    });

    console.log(properties);
    await browser.close();
})();
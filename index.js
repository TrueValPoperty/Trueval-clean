const puppeteer = require('puppeteer');

(async () => {
  console.log("Launching Puppeteer...");
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto("https://www.zoopla.co.uk/for-sale/property/south-west-england/", { waitUntil: "domcontentloaded" });

  const listings = await page.evaluate(() => {
    const properties = [];
    document.querySelectorAll(".dkr2t82").forEach(card => {
      const title = card.querySelector("h2")?.innerText || "";
      const address = card.querySelector("address")?.innerText || "";
      const price = card.querySelector("p")?.innerText || "";
      properties.push({ title, address, price });
    });
    return properties;
  });

  console.log("Scraped listings:", listings);
  await browser.close();
})();

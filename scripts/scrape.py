import asyncio
from playwright.async_api import async_playwright

# https://medium.com/@hasdata/how-to-scrape-websites-with-playwright-and-python-49a015fd00aa

async def scrape_table():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://citizens-initiative.europa.eu/initiatives/details/2024/000007_en")
        await page.wait_for_selector("table")
        rows = await page.query_selector_all("table tr")
        for row in rows:
            cells = await row.query_selector_all("td")
            cell_texts = [await cell.inner_text() for cell in cells]
            print(cell_texts)
        await browser.close()

asyncio.run(scrape_table())
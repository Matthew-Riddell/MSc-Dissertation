# Matthew Riddell
# D00245674
# MSc in Data Analytics
# Disseration
# Data Scraping Script

# To run: "py scrape.py" in cmd

import asyncio
from playwright.async_api import async_playwright
import pandas as pd

# https://medium.com/@hasdata/how-to-scrape-websites-with-playwright-and-python-49a015fd00aa

async def scrape_table():
    async with async_playwright() as p:
        # Launch Chromium headless
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Open the page
        await page.goto("https://citizens-initiative.europa.eu/initiatives/details/2024/000007_en")
        
        # Wait for table to load
        await page.wait_for_selector("table")
        
        # Get the table rows
        rows = await page.query_selector_all("table tr")
        
        data = []
        for row in rows:
            cells = await row.query_selector_all("th, td")  
            cell_texts = [await cell.inner_text() for cell in cells]
            if cell_texts:  # skip empty rows
                data.append(cell_texts)
        
        await browser.close()
    
    # --- Process the data ---
    
    headers = data[0]  # Headers 
    table_data = data[1:-1]  # all rows except header and last row (total)
    
    # Last row is the total
    total_row = data[-1]
    total_signatories = None
    if total_row[0].lower().startswith("total"): # Row for total signatures
        total_signatories = total_row[1] 
    
    # Dataframe
    df = pd.DataFrame(table_data, columns=headers)
    
    # Export to CSV
    df.to_csv("eci_table.csv", index=False)
    print("Table saved to eci_table.csv")
    if total_signatories:
        print(f"Total number of signatories: {total_signatories}")

# Run the scraper
asyncio.run(scrape_table())
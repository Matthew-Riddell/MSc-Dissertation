# Matthew Riddell
# D00245674
# MSc in Data Analytics
# Disseration
# Data Scraping Script

# To run: "py scrape.py" in cmd

import asyncio
from playwright.async_api import async_playwright
import pandas as pd

# Petitions:
# https://citizens-initiative.europa.eu/initiatives/details/2024/000001_en Ban on conversion practices in the European Union
# https://citizens-initiative.europa.eu/initiatives/details/2024/000002_en European Citizens' Initiative in Defence of Agriculture and Rural Economy in Europe
# https://citizens-initiative.europa.eu/initiatives/details/2024/000004_en My Voice, My Choice: For Safe And Accessible Abortion
# https://citizens-initiative.europa.eu/initiatives/details/2024/000006_en Air-Quotas
# https://citizens-initiative.europa.eu/initiatives/details/2024/000007_en Stop Destroying Videogames
# https://citizens-initiative.europa.eu/initiatives/details/2024/000008_en Stop Cruelty Stop Slaughter
# https://citizens-initiative.europa.eu/initiatives/details/2024/000009_en STOP FAKE FOOD: ORIGIN ON LABEL

# https://medium.com/@hasdata/how-to-scrape-websites-with-playwright-and-python-49a015fd00aa

async def scrape_table():
    async with async_playwright() as p:
        # Launch Chromium headless
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Open the page
        await page.goto("https://citizens-initiative.europa.eu/initiatives/details/2024/000009_en")
        
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
    
    headers = data[0]

    table_data = []
    total_signatories = None

    for row in data[1:]:
        if row[0].lower().startswith("total"):
            total_signatories = row[1]
            table_data.append(row)  # include total row
            break
        else:
            table_data.append(row) 
    
    # Dataframe
    df = pd.DataFrame(table_data, columns=headers)
    
    # Export to CSV
    df.to_csv("eci_table.csv", index=False)
    print("Table saved to eci_table.csv")
    if total_signatories:
        print(f"Total number of signatories: {total_signatories}")

# Run the scraper
asyncio.run(scrape_table())
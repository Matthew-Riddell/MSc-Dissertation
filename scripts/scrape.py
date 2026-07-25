# Matthew Riddell
# D00245674
# MSc in Data Analytics
# Disseration
# Data Scraping Script

# To run: "py scrape.py" in cmd

# For this part of the project, I need to scrape ECI petitions from the European Citizens Initiative website
# This file uses playwright to open a chromium session and extract the table manually 1 page at a time
# For this I place the link to the petition page and then run the file which then opens the session and waits for the table to load
# then it extracts the table and puts it into a dataframe and then writes it to a new csv file
# I repeat this process for each petition 


# Mahara Portfolio:
# https://mahara.dkit.ie/view/view.php?t=f816cb6da6dd833aaa2f

# Github Repository:
# https://github.com/Matthew-Riddell/MSc-Dissertation

import asyncio
from playwright.async_api import async_playwright
import pandas as pd

# Petitions:
# 2024

# ECI 01: https://citizens-initiative.europa.eu/initiatives/details/2024/000001_en Ban on conversion practices in the European Union
# ECI 02: https://citizens-initiative.europa.eu/initiatives/details/2024/000002_en European Citizens' Initiative in Defence of Agriculture and Rural Economy in Europe
# ECI 03: https://citizens-initiative.europa.eu/initiatives/details/2024/000004_en My Voice, My Choice: For Safe And Accessible Abortion
# ECI 04: https://citizens-initiative.europa.eu/initiatives/details/2024/000006_en Air-Quotas
# ECI 05: https://citizens-initiative.europa.eu/initiatives/details/2024/000007_en Stop Destroying Videogames
# ECI 06: https://citizens-initiative.europa.eu/initiatives/details/2024/000008_en Stop Cruelty Stop Slaughter
# ECI 07: https://citizens-initiative.europa.eu/initiatives/details/2024/000009_en STOP FAKE FOOD: ORIGIN ON LABEL
# ECI 08: https://citizens-initiative.europa.eu/initiatives/details/2024/000010_en ECI for a Water-Smart and Resilient Europe
# ECI 09: https://citizens-initiative.europa.eu/initiatives/details/2024/000011_en PsychedeliCare

# 2023

# ECI 10: https://citizens-initiative.europa.eu/initiatives/details/2023/000001_en Stop torture and inhuman treatment at Europe’s borders
# ECI 11: https://citizens-initiative.europa.eu/initiatives/details/2023/000002_en Ensuring a dignified reception of migrants in Europe
# ECI 12: https://citizens-initiative.europa.eu/initiatives/details/2023/000003_en End The Horse Slaughter Age
# ECI 13: https://citizens-initiative.europa.eu/initiatives/details/2023/000004_en Connecting all European capitals and people through a high-speed train network
# ECI 14: https://citizens-initiative.europa.eu/initiatives/details/2023/000005_en Effective implementation of the concept of judicial precedent in EU countries
# ECI 15: https://citizens-initiative.europa.eu/initiatives/details/2023/000006_en Taxing great wealth to finance the ecological and social transition
# ECI 16: https://citizens-initiative.europa.eu/initiatives/details/2023/000007_en Preservation and development of Ukrainian culture, education, language, and traditions in EU states
# ECI 17: https://citizens-initiative.europa.eu/initiatives/details/2023/000008_en EU Live Bus Stop Info
# ECI 18: https://citizens-initiative.europa.eu/initiatives/details/2023/000009_en Trust and Freedom
# ECI 19: https://citizens-initiative.europa.eu/initiatives/details/2023/000011_en Creation of a European Environment Authority

# 2022

# ECI 20: https://citizens-initiative.europa.eu/initiatives/details/2022/000001_en Win It On The Pitch 
# ECI 21: https://citizens-initiative.europa.eu/initiatives/details/2022/000002_en Fur Free Europe
# ECI 22: https://citizens-initiative.europa.eu/initiatives/details/2022/000003_en End The Slaughter Age
# ECI 23: https://citizens-initiative.europa.eu/initiatives/details/2022/000004_en Good Clothes, Fair Pay
# ECI 24: https://citizens-initiative.europa.eu/initiatives/details/2022/000007_en Protect the EU’s Rural Heritage, Food Security and Supply
# ECI 25: https://citizens-initiative.europa.eu/initiatives/details/2022/000008_en Focus on Specific Learning Disabilities on EU Level
# ECI 26: https://citizens-initiative.europa.eu/initiatives/details/2022/000009_en European Citizens’ Initiative for VEGAN MEAL
# ECI 27: https://citizens-initiative.europa.eu/initiatives/details/2022/000010_en European Day of "Whatever it Takes" 

# Code adapted from here:
# https://medium.com/@hasdata/how-to-scrape-websites-with-playwright-and-python-49a015fd00aa

async def scrape_table():
    async with async_playwright() as p:
        # Launch Chromium headless
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Open the page
        await page.goto("https://citizens-initiative.europa.eu/initiatives/details/2022/000010_en")
        
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
import aiohttp
import asyncio
import csv
import json
import os
import logging
import random
from bs4 import BeautifulSoup
from typing import List, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Updated page counts for each level
level_pages = {1: 7, 2: 34, 3: 175, 4: 428, 5: 279}
base_url = "https://www.fortiguard.com/encyclopedia?type=ips&risk={level}&page={page}"
max_retries = 5
initial_retry_delay = 2
max_retry_delay = 60

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

async def fetch_page(session: aiohttp.ClientSession, url: str) -> str:
    retry_delay = initial_retry_delay
    for attempt in range(max_retries):
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.text()
                elif response.status == 429:  # Too Many Requests
                    logging.warning(f"Rate limited on {url}. Retrying after delay.")
                else:
                    logging.warning(f"Received status code {response.status} for URL: {url}")
        except aiohttp.ClientError as e:
            logging.error(f"Error fetching {url}: {e}")
        
        # Exponential backoff with jitter
        sleep_time = min(max_retry_delay, retry_delay * (2 ** attempt) + random.uniform(0, 1))
        logging.info(f"Retrying in {sleep_time:.2f} seconds...")
        await asyncio.sleep(sleep_time)
    
    logging.error(f"Failed to fetch {url} after {max_retries} attempts")
    return ""

def parse_page(html: str, url: str) -> List[Tuple[str, str]]:
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    
    rows = soup.select('div.row[onclick^="location.href"]')
    logging.info(f"Found {len(rows)} entries on page: {url}")
    
    for row in rows:
        link = row.get('onclick').split("'")[1]
        full_link = f"https://www.fortiguard.com{link}"
        title_element = row.select_one('div.col-lg b')
        if title_element:
            title = title_element.text.strip()
            data.append((title, full_link))
            logging.debug(f"Extracted: {title} - {full_link}")
        else:
            logging.warning(f"Could not find title for entry on page: {url}")
    
    return data

async def scrape_level(session: aiohttp.ClientSession, level: int, max_page: int) -> Tuple[List[Tuple[str, str]], List[int]]:
    data = []
    skipped = []
    
    for page in range(1, max_page + 1):
        url = base_url.format(level=level, page=page)
        html = await fetch_page(session, url)
        
        if html:
            page_data = parse_page(html, url)
            data.extend(page_data)
            logging.info(f"Scraped {len(page_data)} entries from level {level}, page {page}")
        else:
            skipped.append(page)
            logging.warning(f"Skipped level {level}, page {page} due to empty response")
    
    return data, skipped

async def main():
    os.makedirs('datasets', exist_ok=True)
    skipped_pages = {}

    async with aiohttp.ClientSession() as session:
        for level, max_page in level_pages.items():
            logging.info(f"Starting to scrape level {level} with {max_page} pages")
            data, skipped = await scrape_level(session, level, max_page)
            
            if skipped:
                skipped_pages[level] = skipped
                logging.warning(f"Skipped pages for level {level}: {skipped}")

            csv_filename = f'datasets/forti_lists_{level}.csv'
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['title', 'link'])
                writer.writerows(data)
            
            logging.info(f"Completed level {level}. Saved {len(data)} entries to {csv_filename}")

    with open('datasets/skipped.json', 'w') as jsonfile:
        json.dump(skipped_pages, jsonfile)

    logging.info("Scraping completed. Check the datasets/ directory for results.")

if __name__ == "__main__":
    asyncio.run(main())
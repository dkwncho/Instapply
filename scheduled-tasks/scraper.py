import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def extract_greenhouse_info(search_item):
    try:
        # Link is scraped from metadata
        link = search_item["pagemap"]["metatags"][0]["og:url"]  
    except KeyError:
        # Link is scraped from search result
        link = search_item.get("link")  

    try:
        # Location is scraped from metadata
        location = search_item["pagemap"]["metatags"][0]["og:description"]  
    except KeyError:
        location = "N/A"

    title_pattern = r'(.*) at ([^ ]+.*)'
    alt_title = search_item.get("title").removeprefix("Job Application for ")
    title_match = re.search(title_pattern, alt_title)
    try:
        # Job title is scraped from metadata
        title = search_item["pagemap"]["metatags"][0]["og:title"]  
    except KeyError:
        title = "N/A"
        try:
            # Job title is scraped from search result
            alt_title = title_match.group(1).strip()  
        except AttributeError:
            alt_title = "N/A"
    
    try:
        # Company name is scraped from search result
        company = title_match.group(2).strip()   
        # TODO: Sometimes the above yields company = "Name ..." or "..."
        #  since the title may appear as "Intern at ..." due to limited search result space.
        #  Add another check to use to link scrape method if there are three periods in the company name
    except AttributeError:
        try:
            # Company name is scraped from URL
            link_pattern = r'greenhouse\.io/([^/]+)/jobs'  
            link_match = re.search(link_pattern, link)
            company = link_match.group(1)
        except AttributeError:
            company = "N/A"
    
    return title, alt_title, company, location, link

def scrape_greenhouse():
    query = "allintitle:intern site:greenhouse.io after:2024-07-26 before:2024-07-27" 
    # TODO: Implement query date parameters dynamically

    for page in range(1, 11):
        start = (page - 1) * 10 + 1  # Google's search results display 10 results per page
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"

        try:
            data = requests.get(url, timeout=100).json()
            search_items = data.get("items")

            if search_items is None:
                break
            
            for i, search_item in enumerate(search_items, start):
                title, alt_title, company, location, link = extract_greenhouse_info(search_item)
                
                if title != "N/A":
                    job_data = {
                        "title": title,
                        "company": company,
                        "location": location,
                        "date": "2000-01-01 00:00:01",
                        "link": link,
                    }
                    r = requests.post("https://instapply.onrender.com/api/master", json=job_data)
                elif alt_title != "N/A":
                    job_data = {
                        "title": alt_title,
                        "company": company,
                        "location": location,
                        "date": "2000-01-01 00:00:01",
                        "link": link,
                    }
                    r = requests.post("https://instapply.onrender.com/api/master", json=job_data)
                else:
                    continue
                
        # Exits the loop when no more search results are found
        except TypeError:
            break

scrape_greenhouse()

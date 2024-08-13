import os
import re
import requests
from dotenv import load_dotenv
from datetime import date, timedelta
from bs4 import BeautifulSoup
from config import KEYWORDS

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
        # Location is scraped directly from website
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html5lib')
        location = soup.find('div', attrs = {'class':'location'}).text 
    except AttributeError:
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
        if "..." in company:
            raise AttributeError
    except AttributeError:
        try:
            # Company name is scraped from URL
            link_pattern = r'greenhouse\.io/([^/]+)/jobs'  
            link_match = re.search(link_pattern, link)
            company = link_match.group(1)
        except AttributeError:
            company = "N/A"
    
    return title, alt_title, company, location, link

def classify_job(title):
    industry_list = []
    for industry, keywords in KEYWORDS.items():
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, title, re.IGNORECASE):
                industry_list.append(industry)
                break

    return industry_list

def scrape_greenhouse():
    today = date.today()
    yesterday = today - timedelta(days = 1)

    query = f"allintitle:intern site:greenhouse.io after:{yesterday} before:{today}" 
    job_postings = []
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
                    industry = classify_job(title)
                    job_posting = {
                        "title": title,
                        "company": company,
                        "industry": industry,
                        "location": location,
                        "date": yesterday,
                        "link": link,
                    }
                    job_postings.append(job_posting)
                elif alt_title != "N/A":
                    industry = classify_job(alt_title)
                    job_posting = {
                        "title": alt_title,
                        "company": company,
                        "industry": industry,
                        "location": location,
                        "date": yesterday,
                        "link": link,
                    }
                    job_postings.append(job_posting)
                else:
                    continue     
        # Exits the loop when no more search results are found
        except TypeError:
            break
    r = requests.post("https://instapply-api.vercel.app/api/master", json=job_postings)

scrape_greenhouse()
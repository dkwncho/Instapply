import re
import requests
from bs4 import BeautifulSoup

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
import re
import requests
from bs4 import BeautifulSoup

def extract_lever_info(search_item):
    try:
        # Link is scraped from metadata
        link = search_item["pagemap"]["metatags"][0]["og:url"]  
    except KeyError:
        # Link is scraped from search result
        link = search_item.get("link")  

    try:
        # Location is scraped directly from website
        r = requests.get(link)
        soup = BeautifulSoup(r.content, "html5lib")
        location = soup.find("div", attrs = {"class":"location"}).text 
    except AttributeError:
        location = "N/A"
            
    title_pattern = r"^(.*? - )(.+)"
    try:
        # Job title is scraped from metadata
        title = search_item["pagemap"]["metatags"][0]["og:title"] 
        title_match = re.search(title_pattern, title)
        title = title_match.group(2).strip()    
    except (AttributeError, KeyError):
        title = ""
        try:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, "html5lib")
            div_tag = soup.find("h2")
            title = div_tag.text
            print(title)
            if title == "":
                raise NameError
        except NameError:
            title = "N/A"
    
    try:
        # Company name is scraped directly from website
        company = ""
        r = requests.get(link)
        soup = BeautifulSoup(r.content, "html5lib")
        div_tag = soup.find("div", class_="main-footer-text")
        if div_tag:
            p_tag = div_tag.find("p")
            if p_tag:
                a_tag = p_tag.find("a")
                if a_tag:
                    text = a_tag.text
                    company = text[:-10]
        if company == "":
            raise NameError
    except NameError:
        try:
            # Company name is scraped from URL
            link_pattern = r"lever\.co/([^/]+)/"  
            link_match = re.search(link_pattern, link)
            company = link_match.group(1)
        except AttributeError:
            company = "N/A"
    
    return title, company, location, link
import re

def extract_smartrecruiters_info(search_item):
    try:
        # Link is scraped from metadata
        link = search_item["pagemap"]["metatags"][0]["og:url"]  
    except KeyError:
        # Link is scraped from search result
        link = search_item.get("link")  

    try:
        country = search_item["pagemap"]["postaladdress"][0]["addresscountry"]
        region = search_item["pagemap"]["postaladdress"][0]["addressregion"]
        location = f"{region}, {country}"
    except KeyError:
        try:
            location = country
        except NameError:
            location = "N/A"    

    try:
        # Job title is scraped from metadata
        title = search_item["pagemap"]["jobposting"][0]["title"]
    except KeyError:
        try:
            # Job title is scraped from metadata
            title = search_item["pagemap"]["metatags"][0]["og:title"]
        except KeyError:
            title = "N/A"
    # Checks for non-ASCII characters in job title
    if any(ord(char) > 127 for char in title):
        title = "N/A"
    try:
        # Company name is scraped from metadata
        company = search_item["pagemap"]["jobposting"][0]["hiringorganization"]
    except KeyError:
        try:
            # Company name is scraped from metadata
            company = search_item["pagemap"]["metatags"][0]["og:site_name"]
        except KeyError:
            try:
                # Company name is scraped from URL
                link_pattern = r'smartrecruiters.com/([^/]+)/'  
                link_match = re.search(link_pattern, link)
                company = link_match.group(1)
            except AttributeError:
                company = "N/A"
    
    return title, company, location, link
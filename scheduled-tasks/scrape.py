import os
import requests
from dotenv import load_dotenv
from datetime import date, timedelta
from classify_job import classify_job
from extract_lever_info import extract_lever_info
from extract_greenhouse_info import extract_greenhouse_info
from extract_smartrecruiters_info import extract_smartrecruiters_info

load_dotenv()

API_KEY = os.getenv("API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def scrape(website_url):
    today = date.today()
    yesterday = today - timedelta(days = 1)
    today_string = today.strftime("%Y-%m-%d")
    yesterday_string = yesterday.strftime("%Y-%m-%d")

    query = f"allintitle:intern site:{website_url} after:{yesterday_string} before:{today_string}" 
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
                if website_url == "greenhouse.io":
                    title, alt_title, company, location, link = extract_greenhouse_info(search_item)
                elif website_url == "lever.co":
                    title, company, location, link = extract_lever_info(search_item)
                elif website_url == "smartrecruiters.com":
                    title, company, location, link = extract_smartrecruiters_info(search_item)
                else:
                    break

                if title != "N/A" and location != "N/A" and company != "N/A":
                    industry = classify_job(title)
                    job_posting = {
                        "title": title,
                        "company": company,
                        "industry": industry,
                        "location": location,
                        "date": yesterday_string,
                        "link": link,
                    }
                    job_postings.append(job_posting)
                elif website_url == "greenhouse.io" and alt_title != "N/A" and location != "N/A" and company != "N/A":
                    industry = classify_job(alt_title)
                    job_posting = {
                        "title": alt_title,
                        "company": company,
                        "industry": industry,
                        "location": location,
                        "date": yesterday_string,
                        "link": link,
                    }
                    job_postings.append(job_posting)
                else:
                    continue     
        # Exits the loop when no more search results are found
        except TypeError:
            break
    r = requests.post("https://instapply-api.vercel.app/api/master", json=job_postings)

scrape("greenhouse.io")
scrape("lever.co")
scrape("smartrecruiters.com")

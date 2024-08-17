import re
from config import KEYWORDS

def classify_job(title):
    industry_list = []
    for industry, keywords in KEYWORDS.items():
        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if re.search(pattern, title, re.IGNORECASE):
                industry_list.append(industry)
                break

    return industry_list
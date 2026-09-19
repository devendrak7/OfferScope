from loader import postings
import re
import json


def extract_title(posting):
    lines = posting.splitlines()

    for line in lines:
        if line.strip():
            return line.strip()

    return None
def extract_duration(posting):
    pattern_duration = r"(\d+(?:\.\d+)?)\s*(months?|weeks?|month?|week?)"
    match = re.search(pattern_duration,posting,re.IGNORECASE)
    if match:
        value = float(match.group(1))
        unit = match.group(2).lower()
    if "month" in unit:
        value = value*4.3
    return value
def extract_work_mode(posting):
    if re.search(r"Remote|Work from home", posting, re.IGNORECASE):
        return "remote"
    elif re.search(r"Hybrid",posting,re.IGNORECASE):
        return "hybrid"
    elif re.search(r"On-site|Onsite|Work from office",posting,re.IGNORECASE):
        return "onsite"
    else:
        return "not_mentioned"
def extract_job_type(posting):
    if re.search(r"Internship",posting,re.IGNORECASE):
        return "internship"
    elif re.search(r"\bjob\b",posting,re.IGNORECASE):
        return "job"
    else:
        return None
def extract_location(posting):
    with open ("config/settings.json","r",encoding="utf-8") as file:
        settings = json.load(file)
        cities = settings["cities"]
    for city in cities:
        if re.search(re.escape(city),posting,re.IGNORECASE):
            return city
    return None
def extract_stipend():pass

def extract_skills():pass
def extract_pay_status():pass

print(extract_title(postings[0]))
print(extract_duration(postings[0]))
print(extract_work_mode(postings[2]))
print(extract_job_type(postings[2]))
print(extract_location(postings[1]))



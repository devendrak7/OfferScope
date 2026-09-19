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
def extract_skills(posting):
    with open ("config/skills.json","r",encoding="utf-8") as file:
        skills = json.load(file)
        found_skills = []

    for skill,aliases in skills.items():
        for alias in aliases:
            if re.search(r"\b" + re.escape(alias) + r"\W*\b",posting,re.IGNORECASE):
                found_skills.append(skill)
                break
    return found_skills
def extract_pay_status(posting):
    if re.search(r"\bunpaid\b",posting,re.IGNORECASE):
        return "unpaid"
    elif re.search(r"\bpaid\b",posting,re.IGNORECASE):
        return "paid"
    elif re.search(r"\bnot disclosed\b",posting,re.IGNORECASE):
        return "not_disclosed"
    else:
        return "ambiguous"
def extract_stipend(posting):
    match = re.search(r"(?:₹|INR)?\s*([\d,]+)\s*(?:-|to)\s*(?:₹|INR)?\s*([\d,]+)\s*(?:/month|per month|monthly)",posting,re.IGNORECASE)
    if match:
        minimum = float(match.group(1).replace(",", ""))
        maximum = float(match.group(2).replace(",", ""))
        midpoint = (minimum + maximum) / 2
        return minimum,maximum,midpoint
    match = re.search(r"₹?\s*([\d,]+)\s*(?:/month|per month|monthly)",posting,re.IGNORECASE)
    if match:
        amount = float(match.group(1).replace(",", ""))
        return amount, amount, amount
    match = re.search(r"(?:₹|INR)?\s*([\d.]+)\s*LPA\s*(?:-|to)\s*(?:₹|INR)?\s*([\d.]+)\s*LPA",posting,re.IGNORECASE)
    if match:
        minimum = float(match.group(1).replace(",", ""))*100000/12
        maximum = float(match.group(2).replace(",", ""))*100000/12
        midpoint = ((minimum + maximum) / 2)
        return minimum,maximum,midpoint

    match = re.search(r"([\d.]+)\s*LPA",posting,re.IGNORECASE)
    if match:
        monthly = float(match.group(1))*100000/12
        return monthly, monthly, monthly
    return None


print(extract_title(postings[1]))
print(extract_duration(postings[1]))
print(extract_work_mode(postings[1]))
print(extract_job_type(postings[1]))
print(extract_location(postings[1]))
print(extract_skills(postings[1]))
print(extract_pay_status(postings[1]))
print(extract_stipend(postings[7]))
tests = [
    "Stipend: ₹12,000/month",
    "Compensation: INR 15,000 - INR 20,000 per month",
    "Compensation: 2.4 LPA",
    "Annual compensation: ₹6 LPA - ₹9 LPA",
    "This is an unpaid internship."
]

for test in tests:
    print(extract_stipend(test))




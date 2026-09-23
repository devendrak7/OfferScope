import re
import json

try:
    with open("config/settings.json", "r", encoding="utf-8") as f:
        CITIES = json.load(f).get("cities", [])
except (FileNotFoundError, json.JSONDecodeError):
    CITIES = []

try:
    with open("config/skills.json", "r", encoding="utf-8") as f:
        SKILLS = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    SKILLS = {}
PAY_WORDS_REGEX =re.compile(r"")
PAY_WORDS_REGEX = re.compile(r"stipend|salary|\bctc\b|compensation|per month|/month|monthly|\blpa\b", re.IGNORECASE)
SKIP_WORDS_REGEX = re.compile(r"\bfees?\b|funding|funded|raised|deposit", re.IGNORECASE)
YEARLY_WORDS_REGEX = re.compile(r"per annum|per year|/year|yearly|annual", re.IGNORECASE)
CURRENCY = r"(?:₹|\bINR|\bRs\.?)"
NUMBER = r"(\d[\d,]*(?:\.\d+)?)"

def extract_title(posting):
    lines = posting.splitlines()

    for line in lines:
        if line.strip():
            return line.strip()

    return None
def extract_duration(posting):
    pattern_duration = r"(\d+(?:\.\d+)?)\s*(months?|weeks?)\b"
    match = re.search(pattern_duration,posting,re.IGNORECASE)
    if match:
        value = float(match.group(1))
        unit = match.group(2).lower()
        if "month" in unit:
            value = value*4.3
        return value
    return None
def extract_work_mode(posting):
    if re.search(r"Hybrid", posting, re.IGNORECASE):
        return "hybrid"
    elif re.search(r"Remote|Work from home", posting, re.IGNORECASE):
        return "remote"
    elif re.search(r"On-site|Onsite|Work from office",posting,re.IGNORECASE):
        return "onsite"
    else:
        return "not_mentioned"
def extract_job_type(posting):
    if re.search(r"\bintern(ship)?\b",posting,re.IGNORECASE):
        return "internship"
    elif re.search(r"\bjob\b|full[- ]time",posting,re.IGNORECASE):
        return "job"
    else:
        return None
def extract_location(posting):
    for city in CITIES:
        if re.search(re.escape(city), posting, re.IGNORECASE):
            return city
    return None

def extract_skills(posting):
    found_skills = []
    for skill, similars in SKILLS.items():
        for similar in similars:
            if re.search(r"(?<!\w)" + re.escape(similar) + r"(?!\w)", posting, re.IGNORECASE):
                found_skills.append(skill)
                break
    return found_skills
def extract_pay_status(posting):
    if re.search(r"\bunpaid\b",posting,re.IGNORECASE):
        return "unpaid"
    elif extract_stipend(posting) is not None:
        return "paid"
    elif re.search(r"\bpaid\b",posting,re.IGNORECASE):
        return "paid"
    elif re.search(r"\bnot disclosed\b",posting,re.IGNORECASE):
        return "not_disclosed"
    else:
        return "ambiguous"
def to_number(text):
    return float(text.replace(",", ""))
def extract_stipend(posting):
    for line in posting.splitlines():
        if not PAY_WORDS_REGEX.search( line):
            continue
        if SKIP_WORDS_REGEX.search(line):
            continue

        match = re.search(NUMBER + r"\s*(?:LPA)?\s*(?:-|–|to)\s*" + CURRENCY + r"?\s*" + NUMBER + r"\s*LPA", line, re.IGNORECASE)
        if match:
            minimum = to_number(match.group(1))*100000/12
            maximum = to_number(match.group(2))*100000/12
            midpoint = (minimum + maximum) / 2
            return minimum,maximum,midpoint

        match = re.search(NUMBER + r"\s*LPA", line, re.IGNORECASE)
        if match:
            monthly = to_number(match.group(1))*100000/12
            return monthly,monthly,monthly

        if YEARLY_WORDS_REGEX.search( line):
            continue

        match = re.search(CURRENCY + r"\s*" + NUMBER + r"\s*(?:-|–|to|and)\s*" + CURRENCY + r"?\s*" + NUMBER, line, re.IGNORECASE)
        if match:
            minimum = to_number(match.group(1))
            maximum = to_number(match.group(2))
            midpoint = (minimum + maximum) / 2
            return minimum,maximum,midpoint

        match = re.search(CURRENCY + r"\s*" + NUMBER, line, re.IGNORECASE)
        if match:
            amount = to_number(match.group(1))
            return amount,amount,amount

        match = re.search(NUMBER + r"\s*(?:/\s*month|per month|monthly)", line, re.IGNORECASE)
        if match:
            amount = to_number(match.group(1))
            return amount,amount,amount
    return None


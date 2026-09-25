
import pandas as pd

from extractors import (extract_title,extract_stipend,extract_pay_status,
                        extract_duration,extract_work_mode,extract_skills,
                        extract_location,extract_job_type)
def build_record(posting):
    title = extract_title(posting)
    stipend = extract_stipend(posting)
    pay_status = extract_pay_status(posting)
    duration = extract_duration(posting)
    work_mode = extract_work_mode(posting)
    skills = extract_skills(posting)
    location = extract_location(posting)
    job_type = extract_job_type(posting)
    if stipend:
        stipendMin = stipend[0]
        stipendMax = stipend[1]
        stipendMid = stipend[2]
    else:
        stipendMin = None
        stipendMax = None
        stipendMid = None

    return {
    "title": title,
    "stipend_max": stipendMax,
    "stipend_min": stipendMin,
    "stipend_mid": stipendMid,
    "pay_status": pay_status,
    "duration_weeks": round(duration, 1) if duration is not None else None,
    "work_mode": work_mode,
    "skills": skills,
    "location": location,
    "job_type": job_type
    }
def create_dataframe(postings):
    records = []

    for posting in postings:
        record = build_record(posting)
        records.append(record)

    df = pd.DataFrame(records)

    return df


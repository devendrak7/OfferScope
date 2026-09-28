import pandas as pd


def get_stipend_statistics(df):
    valid_stipends = df["stipend_mid"].dropna()
    valid_stipends_describe = valid_stipends.describe()
    valid_stipends_90 = valid_stipends.quantile(0.90)
    return valid_stipends,valid_stipends_describe  ,valid_stipends_90

def get_outliers(valid_stipends):
    q1 = valid_stipends.quantile(0.25)
    q3 = valid_stipends.quantile(0.75)

    iqr = q3 - q1

    lower_limit = max(0, q1 - 1.5 * iqr)
    upper_limit = q3 + 1.5 * iqr

    outliers = valid_stipends[(valid_stipends < lower_limit) |(valid_stipends > upper_limit)]

    return outliers

def get_skill_demand(df):
    if len(df) == 0:
        return pd.Series(dtype=int), pd.Series(dtype=float)
    skill_counts = df["skills"].explode().value_counts()
    skill_percentage = (skill_counts / len(df)) * 100

    return skill_counts, skill_percentage

def get_skill_pay(df, skill_counts):
    skill_pay = {}

    for skill in skill_counts.index:
        skill_postings = df[
            df["skills"].apply(lambda skills: skill in skills)
        ]

        skill_stipends = skill_postings["stipend_mid"].dropna()

        if len(skill_stipends) >= 3:
            median_stipend = skill_stipends.median()
        else:
            median_stipend = "insufficient data"

        skill_pay[skill] = median_stipend

    return skill_pay

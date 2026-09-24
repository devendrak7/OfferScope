def show_stipend_report(valid_stipends):
    print("\n----- STIPEND REPORT -----")

    print("Postings with a disclosed stipend:", len(valid_stipends))
    print(f"Lowest stipend found: ₹{valid_stipends.min():.0f}")
    print(f"Highest stipend found: ₹{valid_stipends.max():.0f}")

def show_skill_report(skill_counts, skill_percentage):
    print("\n----- SKILL REQUIRED REPORT -----")
    for skill in skill_counts.index:
        count = skill_counts[skill]
        percentage = skill_percentage[skill]

        print(f"{skill}: {count} postings ({percentage:.1f}% of all postings)")

def show_skill_pay_report(skill_pay):
    print("\n----- SKILL MEDIAN PAY REPORT -----")

    for skill, median_stipend in skill_pay.items():
        if median_stipend == "insufficient data":
            print(f"{skill}: Insufficient data(Postings < 3)")
        else:
            print(f"{skill}:₹{median_stipend:.0f}")

def show_quality_report(df):
    print("\n----- EXTRACTION QUALITY REPORT of POSTINGS -----")
    print("Total job/internship postings:", len(df))
    print("Stipend amount was not found:",df["stipend_mid"].isna().sum())
    print("Pay information is unclear:",(df["pay_status"] == "ambiguous").sum())
    print("Duration was not found:",df["duration_weeks"].isna().sum())
    print("Work mode was not mentioned:",(df["work_mode"] == "not_mentioned").sum())
    print("No recognized skills were found:",(df["skills"].apply(len) == 0).sum())
    print("Location was not found:",df["location"].isna().sum())
    print("Job type was not found:",df["job_type"].isna().sum())

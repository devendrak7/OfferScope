from loader import load_postings
from cleaner import create_dataframe
from analyzer import (get_stipend_statistics,get_outliers,get_skill_demand,get_skill_pay,get_numpy_statistics)
from reports import (show_stipend_report,show_skill_report,show_skill_pay_report,show_quality_report)
from exporter import export_csv, export_json, export_txt
from ui import show_menu, get_choice

def main():
    postings = []
    df = None
    while True:
        show_menu()
        choice = get_choice()
        if(choice == "1"):
            postings = load_postings("data/sample/postings.txt")
            if postings:
                df = create_dataframe(postings)
                print(f"\nLoaded {len(postings)} postings successfully.")
        elif(choice == "2"):
            if df is None:
                print("Please load postings first.By Choice 1.")
                continue
            show_quality_report(df)
        elif(choice == "3"):
            if df is None:
                print("Please load postings first.")
                continue
            valid_stipends = get_stipend_statistics(df)
            if len(valid_stipends) == 0:
                print("No valid stipend data found.")
                continue
            show_stipend_report(valid_stipends)
            numpy_stats = get_numpy_statistics(valid_stipends)
            print("\nNumPy Statistics:")
            print(f"Average Stipend: ₹{numpy_stats['mean']:.2f}")
            print(f"Typical Stipend (Median): ₹{numpy_stats['median']:.2f}")
            print(f"Stipend Spread (Standard Deviation): ₹{numpy_stats['std']:.2f}")
            print(f"25% of postings have stipend ≤ ₹{numpy_stats['percentile_25']:.2f}")
            print(f"50% of postings have stipend ≤ ₹{numpy_stats['median']:.2f}")
            print(f"75% of postings have stipend ≤ ₹{numpy_stats['percentile_75']:.2f}")
            print(f"90% of postings have stipend ≤ ₹{numpy_stats['percentile_90']:.2f}")
            outliers = get_outliers(valid_stipends)
            print("Unusually high/low stipends (Outliers):", list(outliers))
        elif(choice == "4"):
            if df is None:
                print("Please load postings first.")
                continue
            skill_counts, skill_percentage = get_skill_demand(df)
            show_skill_report(skill_counts, skill_percentage)
        elif(choice == "5"):
            if df is None:
                print("Please load postings first.")
                continue
            skill_counts, skill_percentage = get_skill_demand(df)
            skill_pay = get_skill_pay(df, skill_counts)
            show_skill_pay_report(skill_pay)

        elif(choice == "6"):

            if df is None:
                print("Please load postings first.")
                continue

            keyword = input("Enter skill/title/location to search: ").strip().lower()

            result = df[
                df["title"].str.lower().str.contains(keyword, na=False, regex=False)
                | df["location"].str.lower().str.contains(keyword, na=False, regex=False)
                | df["skills"].apply(lambda rowSkills: any(keyword in skill.lower() for skill in rowSkills))]
            print("\nSearch Results:")

            if result.empty:
                print("No matching postings found.")
            else:
                print(result[["title", "location", "skills", "stipend_mid"]].to_string(index=False))
        elif(choice == "7"):

            if df is None:
                print("Please load postings first.")
                continue

            export_csv(df, "data/output/postings.csv")
            export_json(df, "data/output/postings.json")
            export_txt(df, "data/output/postings.txt")

        elif(choice == "8"):
            print("Exiting OfferScope...")
            break

        else:

            print("Invalid choice. Please enter 1-8.")
if __name__ == "__main__":
    main()

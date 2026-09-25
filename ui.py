def show_menu():
    print("\n========== OFFERSCOPE ==========")
    print("""   1. Load postings(Power Button)
    2. Extraction quality report
    3. Stipend statistics
    4. Skill demand
    5. Skill vs pay
    6. Search / filter postings
    7. Export CSV / JSON / TXT
    8. Exit""")
    print("================================")


def get_choice():
    return input("Enter your choice: ").strip()

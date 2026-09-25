def show_menu():
    print("\n========== OFFERSCOPE ==========")
    print("1. Load postings")
    print("2. Extraction quality report")
    print("3. Stipend statistics")
    print("4. Skill demand")
    print("5. Skill vs pay")
    print("6. Search / filter postings")
    print("7. Export CSV / JSON / TXT")
    print("8. Exit")
    print("================================")

def get_choice():
    return input("Enter your choice: ").strip()

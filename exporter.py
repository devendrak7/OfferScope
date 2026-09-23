def export_csv(df, file_path):
    df.to_csv(file_path, index=False)
    print("CSV exported successfully.")

def export_json(df, file_path):
    df.to_json(file_path, orient="records", indent=4)
    print("JSON exported successfully.")

def export_txt(df, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(df.to_string(index=False))
    print("TXT exported successfully.")

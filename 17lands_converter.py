import csv

RAW_DATA_PATH_17LANDS = 'C:/Users/shach/OneDrive/Desktop/GithubRepos/MTGVisualizer/17lands_raw_021124.csv'
REFINED_DATA_PATH_17LANDS = 'C:/Users/shach/OneDrive/Desktop/GithubRepos/MTGVisualizer/17lands_refined_021124.csv'


corrected_data = []

with open(RAW_DATA_PATH_17LANDS, 'r') as infile:
    csv_reader = csv.DictReader(infile)
    for row in csv_reader:
        main_colors = ''.join([char for char in row["colors"] if char.isupper()])
        splash_colors = ''.join([char.upper() for char in row["colors"] if char.islower()])
        row_record = row["record"]
        corrected_row = {
            "set_name": "",
            "set_code_name": row["set_code_name"],
            "format": row["format"],
            "date": row["date"],
            "points": row["record"].split('-')[0].strip(),
            "max_points": 7,
            "losses": row["record"].split('-')[1].strip(),
            "colors": main_colors,
            "splash": splash_colors,
            "platform": "arena",
            "link": row["link"]
        }
        corrected_data.append(corrected_row)
    with open(REFINED_DATA_PATH_17LANDS, 'w', newline='') as outfile:
        filenames = ['set_name','set_code_name','format','date','points','max_points','losses','colors','splash','platform','link']
        writer = csv.DictWriter(outfile, fieldnames=filenames)
        writer.writeheader()
        writer.writerows(corrected_data)

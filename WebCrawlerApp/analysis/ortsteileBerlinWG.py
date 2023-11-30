from bs4 import BeautifulSoup
import csv

html_file_path = "data/html/WG-Gesucht/berlin-mainpage.html"
csv_output_path = "data/input/berlin-ortsteileWG.csv"

with open(html_file_path, "r", encoding='utf-8') as html_file:
    html = html_file.read()

soup = BeautifulSoup(html, 'html.parser')

target_values = [
    "114", "85076", "115", "116", "117", "118", "119", "120", "121", "122",
    "123", "124", "125", "126", "85077", "127", "128", "85078", "129", "130",
    "131", "132", "85079", "133", "134", "85080", "85081", "135", "136",
    "85082", "85083", "137", "138", "139", "140", "141", "142", "143", "144",
    "145", "146", "147", "148", "149", "150", "151", "152", "153", "154",
    "155", "156", "157", "158", "159", "160", "161", "162", "85085", "163",
    "85086", "164", "85087", "165", "166", "167", "168", "169", "170",
    "85088", "85089", "171", "172", "173", "174", "175", "85090", "176",
    "177", "178", "179", "180", "85091", "85092", "181", "85093", "182",
    "183", "85094", "184", "185", "186", "187", "188", "189", "190",
    "191", "85095", "85096", "192", "193", "194"
    # ... add more values here
]

# Find <option> tags with the specified values
selected_options = soup.select('select.selectpicker option[value]')

ortsteile = []

# Iterate through selected <option> tags and extract/print their values and text
for option in selected_options:
    value = option['value']
    if value in target_values:
        ortsteil = option.get_text(strip=True)
        ortsteile.append(ortsteil)

with open(csv_output_path, "w", newline='' ,encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Ortsteile"])
    csv_writer.writerows([ortsteil] for ortsteil in ortsteile)


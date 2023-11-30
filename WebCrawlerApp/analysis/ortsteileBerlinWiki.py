from bs4 import BeautifulSoup 
import csv

html_file_path = "data/html/Wikipedia/berlin-ortsteile.html"
csv_output_path = "data/input/berlin-ortsteile.csv"

with open(html_file_path, "r", encoding='utf-8') as html_file:
    html = html_file.read()

soup = BeautifulSoup(html, 'html.parser')

rows = soup.find_all("tr")
data = []

for row in rows: 
    cells = row.find_all('td')
    if len(cells) == 6:  # Ensure there are exactly 6 cells in the row
        ortsteil = cells[1].find('a').text
        bezirk = cells[2].text

        bezirk = bezirk.rstrip("\n")

        data.append([ortsteil, bezirk])

with open(csv_output_path, "w", newline='' ,encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Ortsteil", "Bezirk"])
    csv_writer.writerows(data)
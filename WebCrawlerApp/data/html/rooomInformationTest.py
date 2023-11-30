import pandas as pd
import requests
from bs4 import BeautifulSoup

class RoomInfoExtractor:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.data = {}

    def extract_address(self):
        address_section = self.soup.find('h3', text='Adresse')
        if address_section:
            address = address_section.find_next('span', class_='section_panel_detail').get_text(strip=True)
        else:
            address = "NA"
        self.data['Address'] = address

    def extract_availability(self):
        availability_section = self.soup.find('h3', text='Verfügbarkeit')
        if availability_section:
            frei_ab = availability_section.find('span', class_='section_panel_detail', text='frei ab:').find_next('span').get_text(strip=True)
            frei_bis_section = availability_section.find('span', class_='section_panel_detail', text='frei bis:')
            frei_bis = frei_bis_section.find_next('span').get_text(strip=True) if frei_bis_section else "NA"
        else:
            frei_ab, frei_bis = "NA", "NA"
        self.data['Available From'] = frei_ab
        self.data['Available Until'] = frei_bis

    def extract_online_status(self):
        online_status_section = self.soup.find('span', text='Online:')
        if online_status_section:
            online_status = online_status_section.find_next('b').get_text(strip=True)
        else:
            online_status = "NA"
        self.data['Online Status'] = online_status

    def extract_additional_details(self, detail_type):
        detail_section = self.soup.find('h3', text=detail_type)
        if detail_section:
            details = detail_section.find_all_next('span', class_='section_panel_detail')
            for detail in details:
                self.data[detail_type + ": " + detail.get_text(strip=True).split(':')[0]] = detail.get_text(strip=True)
        else:
            self.data[detail_type] = "NA"

    def create_dataframe(self):
        return pd.DataFrame([self.data])

    def save_to_csv(self, filename):
        df = self.create_dataframe()
        df.to_csv(filename, index=False)


# Usage example:
html_content_path = "WebCrawlerApp/data/html/ad/roomAD1.html"

with open(html_content_path, "r", encoding="utf-8") as file:
    html_content = file.read()

extractor = RoomInfoExtractor(html_content)

extractor.extract_address()
extractor.extract_availability()
extractor.extract_online_status()
extractor.extract_additional_details('WG-Details')
extractor.extract_additional_details('Angaben zum Objekt')
extractor.extract_additional_details('Benötigte Unterlagen')

df = extractor.create_dataframe()
print(df)

# Save to CSV
extractor.save_to_csv('room_info.csv')


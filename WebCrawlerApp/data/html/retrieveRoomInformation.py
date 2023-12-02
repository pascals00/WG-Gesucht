from bs4 import BeautifulSoup
from datetime import datetime 
import re

class HTMLInfoExtractor:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract_rental_information(self):
        title = self.soup.find('h1', class_='headline').get_text(strip=True)
        footer_details = self.soup.find('div', class_='section_footer_dark')
        details = footer_details.find_all('b', class_='key_fact_value')

        room_size = details[0].get_text(strip=True) if len(details) > 0 else None 
        total_rent = details[1].get_text(strip=True) if len(details) > 1 else None 

        return title, room_size, total_rent

    def extract_address(self):
        address_section = self.soup.find('h3', class_= 'section_panel_title mb10 m0', string=re.compile(r'\s*Adresse\s*', re.I))
        if address_section:
            address = address_section.find_next('span', class_='section_panel_detail').get_text(strip=True)
            # Regular expression to match street, postcode, city, and suburb
            match = re.search(r'(.+?)\s*(\d{6})\s*(.+)', address)
            if match:
                street = match.group(1).strip()
                postcode = match.group(2).strip()
                city_suburb = match.group(3).strip()

                # Splitting city and suburb if necessary
                city_suburb_parts = city_suburb.split()
                city = city_suburb_parts[0]
                suburb = ' '.join(city_suburb_parts[1:]) if len(city_suburb_parts) > 1 else None
            else:
                # Handle cases where the pattern does not match
                street = None
                postcode = None
                city = None
                suburb = None
        else:
            address = None 
        return address, street, postcode, city, suburb
    
    def extract_online_status(self):
        # Find the 'Online:' section and the next 'b' tag
        online_status_section = self.soup.find('span', class_='noprint section_panel_detail', string=re.compile(r'\s*Online\s*'))
        if online_status_section:
            online_status = online_status_section.find_next('b').get_text(strip=True)

            # Check if the online status includes 'minute' or 'Minuten' (depending on the language)
            if re.search(r'\bminuten?\b', online_status, re.IGNORECASE):
                # If in minutes, return today's date
                online_status = datetime.now().strftime("%Y-%m-%d")
                return online_status
            else:
                # Otherwise, return the online status as is
                return online_status
        else:
            return None

    def extract_availability(self):
        availability_section = self.soup.find('h3', class_='section_panel_title mb10 m0', string=re.compile(r'\s*Verfügbarkeit\s*', re.I))
        if availability_section:
            # Navigate to the container of 'frei ab' and 'frei bis' sections
            container = availability_section.find_next('div', class_='row')

            # Find 'frei ab' date
            frei_ab_section = container.find('span', class_='section_panel_detail', string=re.compile(r'\s*frei ab\s*'))
            frei_ab = frei_ab_section.find_next('span').get_text(strip=True) if frei_ab_section else None

            # Find 'frei bis' date
            frei_bis_section = container.find('span', class_='section_panel_detail', string=re.compile(r'\s*frei bis\s*'))
            frei_bis = frei_bis_section.find_next('span').get_text(strip=True) if frei_bis_section else None
        else:
            frei_ab, frei_bis = None, None

        return frei_ab, frei_bis


    def extract_costs(self):
        sections = self.soup.find_all('span', class_='section_panel_detail') # find('h3', class_='section_panel_title mb10 m0', string=re.compile(r'\s*Kosten\s*', re.I))

        for row in sections:
            cost_text = row.get_text()
            if re.search(r'\s*Miete\s*', cost_text):
                rent = row.find_next('span', class_='section_panel_value').get_text(strip=True)
            elif re.search(r'\s*Nebenkosten\s*', cost_text):
                utilities = row.find_next('span', class_='section_panel_value').get_text(strip=True)
            elif re.search(r'\s*Sonstige Kosten\s*', cost_text):
                other_costs = row.find_next('span', class_='section_panel_value').get_text(strip=True)
            elif re.search(r'\s*Kaution\s*', cost_text):
                deposit = row.find_next('span', class_='section_panel_value').get_text(strip=True)
            elif re.search(r'\s*Ablösevereinbarung\s*', cost_text):
                transfer_agreement = row.find_next('span', class_='section_panel_value').get_text(strip=True)

        return rent, utilities, other_costs, deposit, transfer_agreement
        
    def extract_wg_details(self):
        wg_details = {}

        # Find the WG-Details section
        wg_details_section = self.soup.find('h3', class_='section_panel_title mb10 m0', string=re.compile(r'\s*WG-Details\s*', re.I))
        if not wg_details_section:
            return wg_details

        # Extract the details
        wg_details_list = wg_details_section.find_next('ul')
        if wg_details_list:
            wg_details['details'] = [' '.join(li.get_text().replace('\n', ' ').split()) for li in wg_details_list.find_all('li')]

        # Extract 'Gesucht wird' (if present)
        gesucht_wird_section = self.soup.find('h4', string=re.compile(r'\s*Gesucht wird\s*', re.I))
        if gesucht_wird_section:
            gesucht_wird_list = gesucht_wird_section.find_next('ul')
            if gesucht_wird_list:
                wg_details['gesucht_wird'] = [li.get_text(strip=True) for li in gesucht_wird_list.find_all('li')]

        return wg_details

    def extract_object_details(self):
        object_details = []
        object_details_section = self.soup.find('h3', text='Angaben zum Objekt')

        if object_details_section:
            utility_icons = object_details_section.find_next_sibling('div').find_all('div', class_='text-center')

            for icon in utility_icons:
                detail = icon.get_text(strip=True)
                object_details.append(detail)

        return object_details

    def extract_required_documents(self):
        required_documents = []
        documents_section = self.soup.find('h3', text=lambda text: text and 'Benötigte Unterlagen' in text)

        if documents_section:
            utility_icons = documents_section.find_next('div', class_='utility_icons').find_all('div', class_='text-center')

            for icon in utility_icons:
                document = icon.get_text(strip=True)
                required_documents.append(document)

        return required_documents


# Usage example:
html_content_path = "WebCrawlerApp/data/html/ad/roomAD1.html"
with open(html_content_path, "r", encoding="utf-8") as file:
    html_content = file.read()

extractor = HTMLInfoExtractor(html_content)
print(extractor.extract_rental_information())
print(extractor.extract_address())
print(extractor.extract_availability())
print(extractor.extract_online_status())
print(extractor.extract_costs())
print(extractor.extract_wg_details())
print(extractor.extract_object_details())
print(extractor.extract_required_documents())





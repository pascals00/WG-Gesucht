from ..constants import OUTPUT_FILEPATH
from bs4 import BeautifulSoup
from datetime import datetime 
import csv
import os   
import re


# Column names for the dataframe
COLUMN_NAMES = ['title', 'room_size', 'total_rent', 
                'address', 'street', 'postcode', 'suburb', 'city', 
                'available_from', 'available_until', 'online_since',
                'rent', 'utilities', 'other_costs', 'deposit', 'transfer_agreement_cost',
                'apartment_size', 'max_roommate', 'roommate_age', 'languages',
                'wg_detail1', 'wg_detail2', 'wg_detail3', 'wg_detail4', 'wg_detail5', 'wg_detail6',
                'object_detail1', 'object_detail2', 'object_detail3', 'object_detail4', 'object_detail5', 'object_detail6', 'object_detail7', 'object_detail8', 'object_detail9', 'object_detail10', 'object_detail11', 'object_detail12', 'object_detail13',
                'required_document1', 'required_document2', 'required_document3']

class HTMLInfoExtractor:
    def __init__(self, html_content):
        # Initialize the HTMLInfoExtractor with HTML content.
        # :param html_content: HTML content to be parsed.

        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.output_filepath = OUTPUT_FILEPATH
        self.apartment_data = {key: None for key in COLUMN_NAMES}

    def update_apartment_data(self, data):
        # Update the apartment data dictionary with new data.
        # :param data: A dictionary containing new data to be updated.

        for key, value in data.items():
            self.apartment_data[key] = value

    def extract_rental_information(self):
        # Extracts basic rental information such as title, room size, and total rent.
        # :return: Tuple of title, room size, and total rent.
        
        title = self.soup.find('h1', class_='headline').get_text(strip=True)
        footer_details = self.soup.find('div', class_='section_footer_dark')
        details = footer_details.find_all('b', class_='key_fact_value')

        room_size = details[0].get_text(strip=True) if len(details) > 0 else None 
        total_rent = details[1].get_text(strip=True) if len(details) > 1 else None 

        data = {'title': title, 'room_size': room_size, 'total_rent': total_rent}
        self.update_apartment_data(data)
        return title, room_size, total_rent

    def extract_address(self):
        # Extracts the address information, including street, postcode, city, and suburb.
        # :return: Tuple containing address, street, postcode, city, and suburb.

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

        data = {'address': address, 'street': street, 'postcode': postcode, 'city': city, 'suburb': suburb}
        self.update_apartment_data(data)
        return address, street, postcode, city, suburb
    
    def extract_online_status(self):
        # Extracts online status information.
        # :return: Online status as a string or None if not found.

        online_status_section = self.soup.find('span', class_='noprint section_panel_detail', string=re.compile(r'\s*Online\s*'))
        if online_status_section:
            online_status = online_status_section.find_next('b').get_text(strip=True)

            # Check if the online status includes 'minute' or 'Minuten' (depending on the language)
            if re.search(r'\bminuten?\b', online_status, re.IGNORECASE):
                # If in minutes, return today's date
                online_status = datetime.now().strftime("%Y-%m-%d")

            data = {'online_since': online_status}
            self.update_apartment_data(data)
        else:
            return None
        
    def extract_availability(self):
        # Extracts information about the availability of the apartment.
        # :return: Tuple of available from and available until dates.

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

        data = {'available_from': frei_ab, 'available_until': frei_bis}
        self.update_apartment_data(data)
        return frei_ab, frei_bis

    def extract_costs(self):
        # Extracts cost-related information such as rent, utilities, etc.
        # :return: Tuple of rent, utilities, other costs, deposit, transfer agreement cost.

        sections = self.soup.find_all('span', class_='section_panel_detail')
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
                transfer_agreement_cost = row.find_next('span', class_='section_panel_value').get_text(strip=True)

        data = {'rent': rent, 'utilities': utilities, 'other_costs': other_costs, 'deposit': deposit, 'transfer_agreement_cost': transfer_agreement_cost}
        self.update_apartment_data(data)
        return rent, utilities, other_costs, deposit, transfer_agreement_cost

    def get_raw_wg_details(self):
        # Extracts raw WG (shared apartment) details.
        # :return: Dictionary of WG details.

        wg_details = {}
        wg_details_section = self.soup.find('h3', class_='section_panel_title mb10 m0', string=re.compile(r'\s*WG-Details\s*', re.I))
        
        if not wg_details_section:
            return wg_details
        
        wg_details_list = wg_details_section.find_next('ul')
        if wg_details_list:
            wg_details['details'] = [' '.join(li.get_text().replace('\n', ' ').split()) for li in wg_details_list.find_all('li')]
        
        gesucht_wird_section = self.soup.find('h4', string=re.compile(r'\s*Gesucht wird\s*', re.I))
        
        if gesucht_wird_section:
            gesucht_wird_list = gesucht_wird_section.find_next('ul')
            if gesucht_wird_list:
                wg_details['gesucht_wird'] = [' '.join(li.get_text().replace('\n', ' ').split()) for li in gesucht_wird_list.find_all('li')]
        return wg_details


    def extract_wg_details(self):
        # Cleans and extracts WG details from raw WG details.
        # :return: Dictionary of cleaned WG details.

        wg_details = self.get_raw_wg_details()
        wg_details = self.clean_wg_details(wg_details)

        # Initialize the target dictionary with default values
        data = {
            'apartment_size': None,
            'max_roommate': None,
            'roommate_age': None,
            'languages': None
        }

        # Update the data dictionary with values from wg_details
        data['apartment_size'] = wg_details.get('Wohnungsgröße')
        data['max_roommate'] = wg_details.get('WG_max_people')
        data['roommate_age'] = wg_details.get('Bewohneralter')
        data['languages'] = wg_details.get('Sprache/n')

        # Handling the 'details' list
        for i, detail in enumerate(wg_details.get('details', [])):
            data[f'wg_detail{i+1}'] = detail
        
        self.update_apartment_data(data)
        return data


    def clean_wg_details(self, data):
        # Cleans WG details by parsing key-value pairs and categorizing them.
        # :param data: Dictionary of raw WG details.
        # :return: Dictionary of cleaned WG details.

        new_data = {}
        for key, values in data.items():
            for value in values:
                if ':' in value:
                    # Splitting at the first colon to extract key-value pairs
                    split_value = value.split(':', 1)
                    new_data[split_value[0].strip()] = split_value[1].strip()
                else:
                    # Adding non-key-value data to 'details'
                    if 'details' not in new_data:
                        new_data['details'] = []
                    new_data['details'].append(value)

                # Extracting the maximum number of people in the WG
                wg_max_people_match = re.search(r'(\d+)er WG', value)
                if wg_max_people_match:
                    # Extracting the number and converting it to an integer
                    new_data['WG_max_people'] = int(wg_max_people_match.group(1))

        return new_data


    def extract_object_details(self):
        # Extracts object details such as amenities and features of the apartment.
        # :return: Dictionary of object details.

        data = {}
        # Find the h3 tag with specific text
        object_details_section = self.soup.find('h3', string=re.compile(r'\s*Angaben zum Objekt\s*', re.I))

        if object_details_section:
            # Navigate to the parent and then to the next div
            section_panel = object_details_section.find_parent('div', class_='section_panel')
            if section_panel:
                utility_icons = section_panel.find_all('div', class_='text-center')

                for i, icon in enumerate(utility_icons, 1):
                    # Extract and clean text
                    detail = ' '.join(icon.get_text(strip=True).replace('\n', ' ').split())
                    data[f'object_detail{i}'] = detail

        self.update_apartment_data(data)
        return data


    def extract_required_documents(self):
        # Extracts information about the documents required for the apartment rental.
        # :return: Dictionary of required documents.

        data = {}
        documents_section = self.soup.find('h3', string=lambda text: text and 'Benötigte Unterlagen' in text)

        if documents_section:
            utility_icons = documents_section.find_next('div', class_='utility_icons').find_all('div', class_='text-center')

            for i, icon in enumerate(utility_icons, 1):
                document = icon.get_text(strip=True)
                data[f'required_document{i}'] = document

        self.update_apartment_data(data)
        return data


    def write_to_csv(self):
        # Writes the extracted apartment data to a CSV file.
        # :param filename: Name of the CSV file to be written.

        filename = self.output_filepath        
        file_exists = os.path.isfile(filename)

        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            # Dynamically adjust column names based on the data
            fieldnames = list(self.apartment_data.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header only if file did not exist
            if not file_exists:
                writer.writeheader()

            # Extend existing columns if new data has more columns
            missing_columns = set(fieldnames) - set(COLUMN_NAMES)
            if missing_columns:
                COLUMN_NAMES.extend(missing_columns)

            writer.writerow(self.apartment_data)

    def extract_all(self):
        # Main method to extract all information and handle exceptions.
        try:
            self.extract_rental_information()
            self.extract_address()
            self.extract_availability()
            self.extract_online_status()
            self.extract_costs()
            self.extract_wg_details()
            self.extract_object_details()
            self.extract_required_documents()
            self.write_to_csv()
        except Exception as e:
            print(f"An error occurred: {e}")

# Usage example
html_content_path = "WebCrawlerApp/data/html/ad/roomAD3.html"
with open(html_content_path, "r", encoding="utf-8") as file:
    html_content = file.read()

extractor = HTMLInfoExtractor(html_content)
extractor.extract_all()  
extractor.write_to_csv()

from ..constants import ROOMINFO_PATH, LOG_PATH
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
import traceback
import csv
import os   
import re


# Column names for the dataframe
COLUMN_NAMES = ['apartmentID', 'title', 'room_size', 'total_rent', 'premiumstatus', 'user_name',
                'address', 'street', 'postcode', 'suburb', 'city', 
                'available_from', 'available_until', 'online_since',
                'rent', 'utilities', 'other_costs', 'deposit', 'transfer_agreement_cost',
                'apartment_size', 'max_roommate', 'roommate_age', 'languages', 'wg_type', 'smoking_policy', 'preferred_gender_age', 'wg_detail1', 'wg_detail2', 
                'house_type', 'floor', 'parking_situation', 'public_transport_reach', 'furnitured', 'garden', 'balcony', 'electricity_eco_friendly', 'heating', 'internet', 'bathroom', 'ground_material', 'object_detail1', 'object_detail2', 
                'required_document1', 'required_document2', 'required_document3']

class HTMLInfoExtractor:
    def __init__(self, html_content, apartmentID):
        # Initialize the HTMLInfoExtractor with HTML content.
        # :param html_content: HTML content to be parsed.
            self.soup = BeautifulSoup(html_content, 'html.parser')
            self.apartmentID = apartmentID
            self.output_filepath = ROOMINFO_PATH
            self.apartment_data = {key: None for key in COLUMN_NAMES}
            logging.basicConfig(filename=LOG_PATH, filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def update_apartment_data(self, data):
        # Update the apartment data dictionary with new data.
        # :param data: A dictionary containing new data to be updated.
        try:
            for key, value in data.items():
                self.apartment_data[key] = value
        except Exception as e:
            logging.error(f"{self.apartmentID}: Error in update_apartment_data. Message: {e}")
            logging.error(traceback.format_exc())

    def check_ad_is_active(self): 
        # Checks if the ad is active or not.
        # :return: True if the ad is active, False otherwise.
        try: 
            # Find the section with the title 'Anzeige ist deaktiviert'
            ad_deactivated = re.compile(r'Anzeige.*deaktiviert', re.DOTALL)
            if ad_deactivated.search(self.soup.text):
                return False
            else:
                return True
        except Exception as e:
            logging.error(f"{self.apartmentID}: Error in check_ad_is_active. Message: {e}")
            logging.error(traceback.format_exc())

    def check_id_is_stored(self):
        # Checks if the apartment ID is already stored in the CSV file.
        # :return: True if the apartment ID is already stored, False otherwise.
        try: 
            # Find the section with the title 'Anzeige ist deaktiviert'
            with open(self.output_filepath, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row['apartmentID'] == self.apartmentID:
                        return True
                return False
        except Exception as e:
            logging.error(f"{self.apartmentID}: Error in check_id_is_stored. Message: {e}")
            logging.error(traceback.format_exc())

    def extract_user_information(self):
        # Extracts user information such as name and premium status.
        # :return: Tuple of premium status and user name.
        try: 
            premium_image = self.soup.find('img', {'src': '/img/wgg_premium_partner.png'})
            premium_status = True if premium_image else False

            name_tag = self.soup.find('p', {'class': 'text-dark-gray text-bold mb0 '})
            name = name_tag.get_text().strip() if name_tag else None 

            data = {'premiumstatus' : premium_status, 'user_name' : name}
            self.update_apartment_data(data)
            return premium_status, name
        except Exception as e:
            data = {'premiumstatus' : False, 'user_name' : 'Public Person'}
            self.update_apartment_data(data)
            logging.error(f"{self.apartmentID}: Error in extract_user_information. Message: {e}")
            logging.error(traceback.format_exc())

    def extract_rental_information(self):
        # Extracts basic rental information such as title, room size, and total rent.
        # :return: Tuple of title, room size, and total rent.
        try: 
            # Extract title
            title_element = self.soup.find('h1', class_='headline')
            if title_element:
                title = title_element.get_text(strip=True)

            # Extract details
            footer_details = self.soup.find('div', class_='section_footer_dark')
            if footer_details:
                details = footer_details.find_all('b', class_='key_fact_value')

                if len(details) > 0:
                    room_size_element = details[0]
                    if room_size_element:
                        room_size = room_size_element.get_text(strip=True)
                
                if len(details) > 1:
                    total_rent_element = details[1]
                    if total_rent_element:
                        total_rent = total_rent_element.get_text(strip=True)
            
            apartmentID = self.apartmentID
            data = {'apartmentID' : apartmentID, 'title': title, 'room_size': room_size, 'total_rent': total_rent}
            self.update_apartment_data(data)
            return title, room_size, total_rent
        except Exception as e:
            logging.error(f"{self.apartmentID}: Error in extract_rental_information. Message: {e}")
            logging.error(traceback.format_exc())

    def extract_address(self):
        # Extracts the address information, including street, postcode, city, and suburb.
        # :return: Tuple containing address, street, postcode, city, and suburb.
        try: 
            address_section = self.soup.find('h3', class_= 'section_panel_title mb10 m0', string=re.compile(r'\s*Adresse\s*', re.I))
            if address_section:
                address = address_section.find_next('span', class_='section_panel_detail').get_text(strip=True)
                # Regular expression to match street, postcode, city, and suburb
                match = re.search(r'(.+?)\s*(\d{5})\s+(.+)', address)
                if match:
                    street = match.group(1).strip()
                    postcode = match.group(2).strip()
                    city_suburb = match.group(3).strip()

                    # Splitting city and suburb based on whitespace
                    city_suburb_parts = city_suburb.split(maxsplit=1)
                    city = city_suburb_parts[0].strip()
                    suburb = city_suburb_parts[1].strip() if len(city_suburb_parts) > 1 else None
                else:
                    # Handle cases where the pattern does not match
                    street = None
                    postcode = None
                    city = None
                    suburb = None

                data = {'address': address, 'street': street, 'postcode': postcode, 'city': city, 'suburb': suburb}
                self.update_apartment_data(data)  # This method should be defined elsewhere in your class to handle the data update.
                return street, postcode, city, suburb
        except Exception as e:
            logging.error(f"{self.apartmentID}: Error in extract_address. Message: {e}")
            logging.error(traceback.format_exc())

    def extract_online_status(self):
        # Extracts online status information.
        # :return: Online status as a string or None if not found.
        try: 
            online_status_section = self.soup.find('span', class_='noprint section_panel_detail', string=re.compile(r'\s*Online\s*'))
            if online_status_section:
                online_status = online_status_section.find_next('b').get_text(strip=True)

                # Check if the online status includes 'minute' or 'Minuten' (German for minutes)
                if re.search(r'\bminuten?\b', online_status, re.IGNORECASE):
                    # If in minutes, return today's date
                    formatted_date = datetime.now().strftime("%Y-%m-%d")
                # Check if the online status includes 'Stunde' or 'Stunden' (German for hour/hours)
                elif re.search(r'\bstunden?\b', online_status, re.IGNORECASE):
                    # If in hours, return today's date
                    formatted_date = datetime.now().strftime("%Y-%m-%d")
                # Check if the online status includes 'Tag' or 'Tage' (German for day/days)
                elif re.search(r'\btag(e)?\b', online_status, re.IGNORECASE):
                    # Extract the number of days from the status
                    days = int(re.search(r'\d+', online_status).group())
                    # Subtract that number of days from today's date
                    formatted_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
                # If the status already has a date, just use that
                elif re.match(r'\d{2}\.\d{2}\.\d{4}', online_status):
                    # Convert the date from 'dd.mm.yyyy' to 'yyyy-mm-dd'
                    formatted_date = datetime.strptime(online_status, '%d.%m.%Y').strftime('%Y-%m-%d')

                # Only update if a date was able to be parsed
                if formatted_date:
                    data = {'online_since': formatted_date}
                    self.update_apartment_data(data)
            else:
                return None
        except Exception as e:
            logging.error(f"{self.apartmentID}: Error in extract_online_status. Message: {e}")
            logging.error(traceback.format_exc())
            
    def extract_availability(self):
        # Extracts information about the availability of the apartment.
        # :return: Tuple of available from and available until dates.
        try: 
            availability_section = self.soup.find('h3', class_='section_panel_title mb10 m0', string=re.compile(r'\s*Verfügbarkeit\s*', re.I))
            if availability_section:
                # Navigate to the container of 'frei ab' and 'frei bis' sections
                container = availability_section.find_next('div', class_='row')
                # Find 'frei ab' date
                frei_ab_section = container.find('span', class_='section_panel_detail', string=re.compile(r'\s*frei ab\s*'))
                frei_ab = frei_ab_section.find_next('span').get_text(strip=True) if frei_ab_section else None
                if frei_ab:
                    frei_ab = datetime.strptime(frei_ab, '%d.%m.%Y').strftime('%d.%m.%Y') 
                else:
                    frei_ab = None
                # Find 'frei bis' date
                container = container.find_next('div', class_='row')
                frei_bis_section = container.find('span', class_='section_panel_detail', string=re.compile(r'\s*frei bis\s*'))
                frei_bis = frei_bis_section.find_next('span').get_text(strip=True) if frei_bis_section else None
                if frei_bis:
                    frei_bis = datetime.strptime(frei_bis, '%d.%m.%Y').strftime('%d.%m.%Y')
                else: None
            else:
                frei_ab, frei_bis = None, None

            data = {'available_from': frei_ab, 'available_until': frei_bis}
            self.update_apartment_data(data)
            return frei_ab, frei_bis
        except Exception as e:
            logging.error(f"{self.apartmentID}: Error in extract_availability. Message: {e}")
            logging.error(traceback.format_exc())

    def extract_costs(self):
        # Extracts cost-related information such as rent, utilities, etc.
        # :return: Tuple of rent, utilities, other costs, deposit, transfer agreement cost.
        try:
            rent = utilities = other_costs = deposit = transfer_agreement_cost = None
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
        except Exception as e:
            logging.error(f"{self.apartmentID}: Error in extract_costs. Message: {e}")
            logging.error(traceback.format_exc())

    def get_raw_wg_details(self):
        # Extracts raw WG (shared apartment) details.
        # :return: Dictionary of WG details.
        try: 
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
        except Exception as e:
            logging.error(f"{self.apartmentID}: Error in get_raw_wg_details. Message: {e} ")
            logging.error(traceback.format_exc())

    def extract_wg_details(self):
        # Cleans and extracts WG details from raw WG details.
        # :return: Dictionary of cleaned WG details.
        try: 
            wg_details = self.get_raw_wg_details()
            wg_details = self.clean_wg_details(wg_details)
            
            # Define the list of possible WG-Art values
            wg_art_values = [
                '-WG', 'Wohnheim', 'WG mit Kindern', 'Verbindung', 'gemischte WG',
                'Mehrgenerationen', 'Vegan', 'Wohnen für Hilfe', 'LGBTQ', 'Alleinerziehende'
            ]

            # Initialize the target dictionary with default values
            data = {
                'apartment_size': None,
                'max_roommate': None,
                'roommate_age': None,
                'languages': None, 
                'wg_type': None,
                'smoking_policy': None, 
                'preferred_gender_age': None, 
            }

            if wg_details:

                # Update the data dictionary with values from wg_details
                data['apartment_size'] = wg_details.get('Wohnungsgröße')
                data['max_roommate'] = wg_details.get('WG_max_people')
                data['roommate_age'] = wg_details.get('Bewohneralter')
                data['languages'] = wg_details.get('Sprache/n')

                for wg_art in wg_art_values:
                    wg_art_found = False
                    for index, wg_detail in enumerate(wg_details['details']):
                        if wg_art in wg_detail: 
                            data['wg_type'] = wg_detail
                            wg_art_found = True
                            # Remove the matched wg_detail from the list
                            del wg_details['details'][index]
                            break
                    if wg_art_found is True: 
                        break
            
                for index, wg_detail in enumerate(wg_details['details']):
                    if 'Rauchen' in wg_detail:
                        data['smoking_policy'] = wg_detail
                        del wg_details['details'][index]
                        break

                for index, wg_detail in enumerate(wg_details['details']):
                    if 'Frau zwischen' in wg_detail or 'Mann zwischen' in wg_detail or 'Geschlecht egal' in wg_detail:
                        data['preferred_gender_age'] = wg_detail
                        del wg_details['details'][index]
                        break

                # Handling the 'details' list
                for i, detail in enumerate(wg_details.get('details', [])):
                    data[f'wg_detail{i+1}'] = detail
                
                self.update_apartment_data(data)
                return data
        except Exception as e:
            logging.error(f"{self.apartmentID}: Error in extract_wg_details. Message: {e}")
            logging.error(traceback.format_exc())

    def clean_wg_details(self, data):
        # Cleans WG details by parsing key-value pairs and categorizing them.
        # :param data: Dictionary of raw WG details.
        # :return: Dictionary of cleaned WG details.
        try: 
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
        except Exception as e:
            logging.error(f"{self.apartmentID}: Error in clean_wg_details. Message: {e}")
            logging.error(traceback.format_exc())

    def extract_object_details(self):
        # Extracts object details such as amenities and features of the apartment.
        # :return: Dictionary of object details.
        try: 
            data = {}
            # Find the h3 tag with specific text
            object_details_section = self.soup.find('h3', string=re.compile(r'\s*Angaben zum Objekt\s*', re.I))

            if object_details_section:
                # Navigate to the parent and then to the next div
                section_panel = object_details_section.find_parent('div', class_='section_panel')
                if section_panel:
                    utility_icons = section_panel.find_all('div', class_='text-center')

                    data = {
                        'house_type' : None, 
                        'floor' : None, 
                        'parking_situation' : None, 
                        'public_transport_reach' : None, 
                        'furnitured' : None, 
                        'garden' : False, 
                        'balcony' : False, 
                        'electricity_eco_friendly' : False, 
                        'heating' : None, 
                        'internet' : None, 
                        'bathroom' : None, 
                        'ground_material' : None  
                    }

                    house_type = ['Altbau', 'sanierter Altbau', 'Neubau', 'Reihenhaus', 'Doppelhaus', 'Einfamilienhaus', 'Mehrfamilienhaus', 'Hochhaus', 'Plattenbau']
                    parking_situation = ['gute Parkmöglichkeit', 'schlechte Parkmöglichkeit', 'Bewohnerparken', 'eigener Parkplatz', 'Tiefgaragenstellplatz' ]
                    furnitured = ['möbliert', 'teilmöbliert', 'unmöbliert']
                    heating = ['Zentralheizung', 'Gasheizung', 'Ofenheizung', 'Fernwärme', 'Kohleofen', 'Nachtspeicher' ]
                    internet = ['DSL', 'Wlan', 'Flatrate']
                    ground_material = ['Teppich', 'Parkett', 'Laminat', 'Dielen', 'PVC', 'Fliesen', 'Fußbodenheizung']
                    i = 1 

                    for icon in utility_icons:
                        # Extract and clean text
                        detail = ' '.join(icon.get_text(strip=True).replace('\n', ' ').split())
                        if detail in house_type: 
                            data['house_type'] = detail
                        elif 'OG' in detail or 'EG' in detail: 
                            data['floor'] = detail
                        elif detail in parking_situation: 
                            data['parking_situation'] = detail 
                        elif 'Minuten zu' in detail: 
                            data['public_transport_reach'] = detail
                        elif detail in furnitured: 
                            data['furnitured'] = detail 
                        elif 'Garten' in detail: 
                            data['garden'] = True 
                        elif 'Balkon' in detail: 
                            data['balcony'] = True
                        elif 'Ökostrom' in detail: 
                            data['electricity_eco_friendly'] = True 
                        elif detail in heating: 
                            data['heating'] = detail
                        elif detail in internet: 
                            data['internet'] = detail
                        elif 'Dusche' in detail or 'Bad' in detail: 
                            data['bathroom'] = detail
                        elif detail in ground_material: 
                            data['ground_material'] = detail
                        else: 
                            data[f'object_detail{i}'] = detail
                            i =+ 1

            self.update_apartment_data(data)
            return data
        except Exception as e:
            logging.error(f"{self.apartmentID}: Error in extract_object_details. Message: {e}")
            logging.error(traceback.format_exc())

    def extract_required_documents(self):
        # Extracts information about the documents required for the apartment rental.
        # :return: Dictionary of required documents.
        try: 
            data = {}
            documents_section = self.soup.find('h3', string=lambda text: text and 'Benötigte Unterlagen' in text)

            if documents_section:
                utility_icons = documents_section.find_next('div', class_='utility_icons').find_all('div', class_='text-center')

                for i, icon in enumerate(utility_icons, 1):
                    document = icon.get_text(strip=True)
                    data[f'required_document{i}'] = document

            self.update_apartment_data(data)
            return data
        except Exception as e:
            logging.error(f"{self.apartmentID}: Error in extract_required_documents. Message: {e}")
            logging.error(traceback.format_exc())

    def write_to_csv(self):
        # Writes the extracted apartment data to a CSV file.
        # :param filename: Name of the CSV file to be written.
        try:
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
        except Exception as e:
            logging.error(f"{self.apartmentID}: Error in write_to_csv. Message: {e}")
            logging.error(traceback.format_exc())

    def extract_all(self):
        # Main method to extract all information and handle exceptions.
        try:
            if self.check_ad_is_active() is True:
                if self.check_id_is_stored() is False:
                    self.extract_rental_information()
                    self.extract_user_information()
                    self.extract_address()
                    self.extract_availability()
                    self.extract_online_status()
                    self.extract_costs()
                    self.extract_wg_details()
                    self.extract_object_details()
                    self.extract_required_documents()
                    self.write_to_csv()
                    logging.info(f"{self.apartmentID}: Apartment data extracted successfully.")
                else: 
                    logging.info(f"{self.apartmentID}: Apartment ID is already stored.")
            else:
                logging.info(f"{self.apartmentID}: ... Ad is inactive.")
        except Exception as e:
            logging.error(f"Error in extract_all: {e}")
            logging.error(traceback.format_exc())
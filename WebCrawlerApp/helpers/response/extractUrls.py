from ..constants import *
import csv
import re
import traceback
import os
import logging
from bs4 import BeautifulSoup

class AdsExtractor:
    def __init__(self):
        self.base_url = BASE_URL
        logging.basicConfig(filename=LOG_PATH, filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def extract_ads_url_endings(self, responseHTML):
        # Find all the ads and extract their IDs and URL endings
        soup = BeautifulSoup(responseHTML, 'html.parser')
        ads = soup.find_all('div', class_='wgg_card offer_list_item')
        url_dict = {}

        for ad in ads:
            ad_id = ad.get('data-id')
            url_ending = ad.find('a', href=True)['href']
            url_dict[ad_id] = url_ending

        self.store_ads_url_endings_in_csv(url_dict)

    def extract_max_results(self, responseHTML):
        # Find the max results of the search on First Page
        try: 
            soup = BeautifulSoup(responseHTML, 'html.parser')
            h1_tag = soup.find('div', class_='col-md-8').find('h1')
            h1_text = h1_tag.text if h1_tag else ''
            numbers = re.findall(r'\d+', h1_text)
            max_results = int(numbers[0]) if numbers else 0
            return max_results
        except Exception as e:
            logging.error(f"Error extracting max results: {e}")
            logging.error(traceback.format_exc())

    
    def store_max_results_in_csv(self, max_results, district, suburbs):
        file_exists = os.path.isfile(MAX_RESULTS_SUBURBS_PATH)

        with open(MAX_RESULTS_SUBURBS_PATH, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['District','Suburbs','Max Results'])

            writer.writerow([district, suburbs, max_results])

    def store_ads_url_endings_in_csv(self, url_dict):
        file_exists = os.path.isfile(self.csv_path)
        stored_urls = self.read_url_endings()

        with open(self.csv_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['Ad ID', 'URL Ending'])  # Adding header if file doesn't exist

            for ad_id, url_ending in url_dict.items():
                if ad_id not in stored_urls:
                    writer.writerow([ad_id, url_ending])

        logging.info("New ADs with their corresponding url have been saved to ADsURLList.csv.")

    def read_url_endings(self):
        urls = {}
        try:
            with open(ADS_URL_LIST_PATH, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)  # Skip header
                for row in reader:
                    # if statement 
                    full_url = self.base_url + row[1]
                    urls[row[0]] = full_url
            return urls
        except FileNotFoundError:
            logging.error(f"File {ADS_URL_LIST_PATH} not found.")
            return []
        
    def ads_roominfo_not_extracted(self):
        stored_urls = self.read_url_endings()
        url_endings_roominfo_not_extracted = {}

        with open(ROOMINFO_PATH, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            ids_roominfo_extracted = [int(float(row[0])) for row in reader]

        for id in stored_urls.keys():
            if int(id) not in ids_roominfo_extracted:
                url_endings_roominfo_not_extracted[id] = stored_urls[id]
        
        return url_endings_roominfo_not_extracted
    

    

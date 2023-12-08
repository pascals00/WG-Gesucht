from ..constants import *
import csv
import os
import logging
from bs4 import BeautifulSoup

class AdsExtractor:
    def __init__(self):
        self.base_url = BASE_URL
        self.csv_path = ADS_URL_LIST_PATH
        # Initialize logging in the constructor
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def extract_ads_url_endings(self, responseHTML):
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(responseHTML, 'html.parser')

        # Find all the ads and extract their IDs and URL endings
        ads = soup.find_all('div', class_='wgg_card offer_list_item')
        url_dict = {}

        for ad in ads:
            ad_id = ad.get('data-id')
            url_ending = ad.find('a', href=True)['href']
            url_dict[ad_id] = url_ending

        self.store_ads_url_endings_in_csv(url_dict)

    def store_ads_url_endings_in_csv(self, url_dict):
        file_exists = os.path.isfile(self.csv_path)

        with open(self.csv_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['Ad ID', 'URL Ending'])  # Adding header if file doesn't exist

            for ad_id, url_ending in url_dict.items():
                writer.writerow([ad_id, url_ending])

        logging.info("New ads URL endings saved to ADsURLList.csv.")

    def read_url_endings(self):
        urls = []
        try:
            with open(self.csv_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)  # Skip header
                for row in reader:
                    full_url = self.base_url + row[1]
                    urls.append(full_url)
            return urls
        except FileNotFoundError:
            logging.error(f"File {self.csv_path} not found.")
            return []


import pandas as pd
import logging
import requests
from ..constants import VALID_PROXIE_LIST_PATH

class ProxyReader:
    def __init__(self):
        self.filepath = VALID_PROXIE_LIST_PATH
        self.df = pd.read_csv(self.filepath, header=0)
        self.logger = logging.getLogger(__name__)

    def filter_valid_proxies(self):
        try:
            self.df = self.df[self.df['WgGesucht'] == 1]
            self.logger.info("Valid proxies filtered successfully.")
        except Exception as e:
            self.logger.error("Error occurred while filtering valid proxies: %s", str(e))

    def random_proxy(self):
        try:
            self.filter_valid_proxies()
            return self.df.sample(n=1)
        except Exception as e:
            self.logger.error("Error occurred while selecting random proxy: %s", str(e))

    def get_proxies(self):
        try:
            row = self.random_proxy().iloc[0]
            proxies = {"http": row['http'], "https": row['https']}
            self.test_proxies(proxies)
            self.logger.info("Proxies dictionary retrieved successfully.")
            return proxies
        except Exception as e:
            self.logger.error("Error occurred while getting proxies dictionary: %s", str(e))

    def test_proxies(self, proxies):
        try:
            working_proxie = False
            while working_proxie is False: 
                try: 
                    response = requests.get('https://www.wg-gesucht.de/', proxies=proxies)
                except requests.exceptions.RequestException:
                    proxies = self.get_proxies()
                    continue 
                response.raise_for_status()
                self.logger.info("Proxies tested successfully.")
        except Exception as e:
            self.logger.error("Error occurred while testing proxies: %s", str(e))
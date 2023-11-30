import pandas as pd
import logging
from constants import VALID_PROXIE_LIST_PATH

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
            return self.df.sample(n=1)
        except Exception as e:
            self.logger.error("Error occurred while selecting random proxy: %s", str(e))

    def get_proxies_dict(self):
        try:
            row = self.random_proxy().iloc[0]
            proxies = {"http": row['http'], "https": row['https']}
            self.logger.info("Proxies dictionary retrieved successfully.")
            return proxies
        except Exception as e:
            self.logger.error("Error occurred while getting proxies dictionary: %s", str(e))

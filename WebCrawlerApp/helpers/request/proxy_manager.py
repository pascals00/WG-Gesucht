from fp.fp import FreeProxy
from helpers.request.constants import *
import pandas as pd
import concurrent.futures
import csv
import requests
import random
import logging
import traceback


class ProxyManager:

    def __init__(self):
        self.proxy_path = PROXY_CSV_PATH
        self.proxies_df = self.init_proxie_df()
        logging.basicConfig(level=logging.INFO)


    def init_proxie_df(self): 
        try:
            proxies_df = pd.DataFrame(columns=['http', 'https'])
            for key in URLS.keys():
                proxies_df[key] = pd.NA 
            return proxies_df
        except Exception as e:
            logging.error(f"Error in init_proxie_df: {e}")
            logging.error(traceback.format_exc())
    

    def find_proxies_FreeProxy(self):
        try:
            for _ in range(NUMBER_OF_PROXIES_TO_TEST):
                proxy = self.get_random_proxy()
                if proxy:
                    proxies = {'http': proxy, 'https': proxy}
                    wg_gesucht_found, _ = self.test_proxy(proxy, proxies)
                    if wg_gesucht_found:
                        # Found a working proxy, store it and return
                        self.store_working_ip_address_in_csv(self.proxies_df)
                        return proxies

            logging.info("Failed to find a working proxy after several attempts")
            return None
        except Exception as e:
            logging.error(f"Error in find_proxies_FreeProxy: {e}")
            logging.error(traceback.format_exc())
    

    def get_random_proxy(self):
        try:
            random_country = self.select_random_country()
            try:
                proxy = FreeProxy(country_id=random_country).get()
                if proxy:
                    return proxy
                else:
                    logging.warning(f"No proxy found for country: {random_country}")
                    return None
            except Exception as e:
                logging.error(f"Error obtaining proxy: {e}")
                return None
        except Exception as e:
            logging.error(f"Error in get_random_proxy: {e}")
            logging.error(traceback.format_exc())

    def select_random_country(self):
        europe_countries = ['DE'] * 10 + ['CH'] * 2 + ['AT'] * 3 + ['FR'] * 2 + ['IT'] * 2 + ['ES'] * 2 + ['GB'] * 2 + ['NL'] * 2 + ['SE'] * 2 + ['PL'] * 2
        worldwide_countries = ['US', 'CA', 'AU', 'JP', 'BR']
        countries = europe_countries + worldwide_countries
        return random.choice(countries)


    def test_proxy(self, proxy, proxies):
        try:
            wg_gesucht_found = False
            for key, url in URLS.items():
                if self.is_proxy_working(proxy, proxies, url):
                    self.proxies_df.loc[0, key] = 1
                    if key == 'WgGesucht':
                        self.proxies_df.loc[0, 'http'] = proxy
                        self.proxies_df.loc[0, 'https'] = proxy
                        logging.info("Found working proxies for WgGesucht.")
                        wg_gesucht_found = True
                else:
                    self.proxies_df.loc[0, key] = 0

            return wg_gesucht_found, proxies
        except Exception as e:
            logging.error(f"Error in test_proxy: {e}")
            logging.error(traceback.format_exc())


    def is_proxy_working(self, proxy, proxies, url):
        try:
            response = requests.get(url, proxies=proxies)
            if response.status_code == 200:
                logging.info(f"{proxy}: Proxy is working for the website {url}.")
                return True
            else:
                logging.info(f"{proxy}: Proxy is NOT working for the website {url}.")
                return False
        except requests.exceptions.RequestException as e:
            logging.error(f"{proxy}: Error connecting to website {url}.")
            return False


    def store_working_ip_address_in_csv(self, proxies_df):
        try:
            # Read existing proxies from CSV
            existing_proxies = self.read_proxies_from_csv()

            # Extract proxy information from the DataFrame
            proxy_http = proxies_df.iloc[0]['http']
            proxy_https = proxies_df.iloc[0]['https']

            # Check if the proxy is already in the CSV
            if not any(proxy_http == p['http'] and proxy_https == p['https'] for p in existing_proxies):
                # If not, append the entire row to the CSV
                with open(self.proxy_path, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    # Writing the entire row from DataFrame to CSV
                    writer.writerow(proxies_df.iloc[0].tolist())
                logging.info("New proxy information saved to proxies.csv.")
            else:
                logging.info("Proxy already exists in the CSV.")
        except Exception as e:
            logging.error(f"Error in store_working_ip_address_in_csv: {e}")
            logging.error(traceback.format_exc())

    def read_proxies_from_csv(self):
        try:
            proxies = []
            try:
                with open(self.proxy_path, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        proxies.append({'http': row[0], 'https': row[1]})
            except FileNotFoundError:
                pass
            return proxies
        except Exception as e:
            logging.error(f"Error in read_proxies_from_csv: {e}")
            logging.error(traceback.format_exc())
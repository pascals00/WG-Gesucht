from fp.fp import FreeProxy
import csv
import requests
import random

class ProxyManager:
    def __init__(self, proxy_path='data/input/proxies.csv'):
        self.proxy_path = proxy_path

    def find_proxies(self):
        # Random country selection with a preference for Germany
        country = ['DE'] * 7 + ['CH'] * 1 + ['AT'] * 2
        proxies_found = False

        while not proxies_found:
            random_country = random.choice(country)
            proxy = FreeProxy(country_id=random_country).get()

            if proxy:
                proxies = {'http': proxy, 'https': proxy}
                try:
                    response = requests.get('https://wg-gesucht.de', proxies=proxies)
                    if response.status_code == 200:
                        print("Proxy is working:", proxy)
                        self.store_working_ip_address_in_csv(proxies)
                        proxies_found = True
                        return proxies
                    else:
                        print("Proxy returned status code:", response.status_code)
                except requests.exceptions.RequestException as e:
                    print(f"Error with proxy {proxy}: {e}")

        print("Failed to find a working proxy after several attempts")
        return None

    def store_working_ip_address_in_csv(self, proxies):
        existing_proxies = self.read_proxies_from_csv()

        if proxies['http'] not in [p['http'] for p in existing_proxies] or \
           proxies['https'] not in [p['https'] for p in existing_proxies]:
            with open(self.proxy_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([proxies['http'], proxies['https']])
            print("New proxies saved to proxies.csv.")
        else:
            print("No new proxies to save.")

    def read_proxies_from_csv(self):
        proxies = []
        try:
            with open(self.proxy_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    proxies.append({'http': row[0], 'https': row[1]})
        except FileNotFoundError:
            pass

        return proxies

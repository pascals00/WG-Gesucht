from helpers.request.proxy_manager import *
from helpers.request.suburb_filter import *
from helpers.request.header import *
from helpers.request.url_manager import *
from helpers.response.extractAdsUrls import *
from helpers import logging
import requests
import time

# -------------------------------------------------------
# 1. Request to get all available rooms in Berlin 
# ------------------------------------------------------

# 1.1. Initialize all the helper classes
suburbFilter = SuburbFilter()
requestHeaders = RequestHeaders()
urlManager = URLManager()
findproxy = ProxyManager()
adsExtractor = AdsExtractor()

# Initialize the logging
logging.setup_logging()

# 1.2. Get all the districts
districts = suburbFilter.get_all_districts()

# 1.3 Initialize the variables for request through pages of the district
BaseURL = urlManager.set_base_url(filter_apartment=False, filter_wg=True)
header_initialized = False
currentpage_num = 1

# 1.4. Request through pages of the district and extract the ads url endings
proxies = findproxy.find_proxies_FreeProxy()
headers = requestHeaders.init_headers()

for district in districts:
    for suburbs in suburbFilter.generate_random_suburb_subsets(district):
        FilterUrl = urlManager.set_suburb_filter(BaseURL, suburbs[0])
        currentpage_num = 1
        counter = 1

        while True:
            try:
                page_url = urlManager.switch_page(FilterUrl, currentpage_num)
                response = requests.get(page_url, proxies=proxies, headers=headers)
                response.raise_for_status()

                if currentpage_num == 1:
                    max_results = adsExtractor.extract_max_results(response.text)
                    adsExtractor.store_max_results_in_csv(max_results, district, suburbs[0])

                length_urls_check = adsExtractor.extract_ads_url_endings(response.text, district, suburbs[0])
                if length_urls_check == 0:
                    counter += 1
                else: 
                    currentpage_num += 1

                if adsExtractor.check_no_ads_within_radius_lastpage(response.text):
                    currentpage_num = 1
                    headers = requestHeaders.change_headers()
                    break
                elif counter >= 10:
                    counter = 0 
                    time.sleep(random.randint(5,15))
                    proxies = findproxy.find_proxies_FreeProxy()
                    headers = requestHeaders.change_headers()  

            except requests.exceptions.HTTPError:
                currentpage_num = 1
                headers = requestHeaders.change_headers()
                break
            except requests.exceptions.RequestException:
                proxies = findproxy.find_proxies_FreeProxy()
                headers = requestHeaders.change_headers()

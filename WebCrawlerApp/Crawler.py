from helpers.request.proxy_manager import *
from helpers.request.suburb_filter import *
from helpers.request.header import *
from helpers.request.url_manager import *
from helpers.request.findproxy import *
from helpers.response.extractUrls import *
from helpers.response.retrieveRoomInformation import *
import requests

# -------------------------------------------------------
# 1. Initial Request for District
# ------------------------------------------------------

# 1.1. Initialize all the helper classes
suburbFilter = SuburbFilter()
requestHeaders = RequestHeaders()
urlManager = URLManager()
proxyReader = ProxyReader()
findproxy = ProxyManager()
adsExtractor = AdsExtractor()

# 1.2. Get all the districts
districts = suburbFilter.get_all_districts()
#testdistrict = districts[11]

# 1.3 Initialize the variables for request through pages of the district
BaseURL = urlManager.set_base_url(filter_apartment=False, filter_wg=True)
header_initialized = False
currentpage_num = 1

# 1.4. Request through pages of the district and extract the ads url endings
for district in districts:
    for suburbs in suburbFilter.generate_random_suburb_subsets(district):
        FilterUrl = urlManager.set_suburb_filter(BaseURL, suburbs[0])
        if header_initialized == False:
            proxies = findproxy.find_proxies_FreeProxy()
            headers = requestHeaders.init_headers()
            header_initialized = True
            runningproxie = False

        while True:
            try:
                page_url = urlManager.switch_page(FilterUrl, currentpage_num)
                response = requests.get(page_url, proxies=proxies, headers=headers)
                response.raise_for_status()
                adsExtractor.extract_ads_url_endings(response.text)
                currentpage_num += 1
            except requests.exceptions.HTTPError:
                # HTTP error (e.g., page not found), break the loop
                break
            except requests.exceptions.RequestException:
                # Other request errors (e.g., proxy failure), try new proxy
                proxies = findproxy.find_proxies_FreeProxy()
                if not proxies:
                    break  # No more proxies available, break the loop

# -------------------------------------------------------
# 2. Request for Apartment
# -------------------------------------------------------

# 2.1. Read the ads url endings from the file 
ad_url_list = adsExtractor.read_url_endings()
headers_initialized = False

# 2.2. Find proxie and create header for request
proxies = findproxy.find_proxies_FreeProxy()
headers = requestHeaders.init_headers()

# 2.3. Requests for the apartment and extract the information
for id, url in ad_url_list.items():
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        # Save the html file test purpose
        with open(HTML_FILES_PATH + '/' + str(id) + '.html', 'w', encoding='utf-8') as f: 
            f.write(response.text)
        response.raise_for_status()
        HTMLInfoExtractor(html_content=response.text, apartmentID=id).extract_all()
    except requests.exceptions.RequestException:
        # Other request errors (e.g., proxy failure), try new proxy
        proxies = findproxy.find_proxies_FreeProxy()
        if not proxies:
            break
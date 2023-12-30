from helpers.request.proxy_manager import *
from helpers.request.header import *
from helpers.request.findproxy import *
from helpers.response.extractAdsUrls import *
from helpers.response.extractRoomInformation import *
from helpers import logging
import requests

# -------------------------------------------------------
# 2. Request to extract the information of the apartments
# -------------------------------------------------------

# Initialize all the helper classes
requestHeaders = RequestHeaders()
findproxy = ProxyManager()
adsExtractor = AdsExtractor()

# Setup Logging 
logging.setup_logging()

# 2.1. Read the ads url endings from the file 
if os.path.isfile(ROOMINFO_PATH):
    ad_url_list = adsExtractor.ads_roominfo_not_extracted()
else: 
    ad_url_list = adsExtractor.read_url_endings()
    
# 2.2. Find proxie
proxies = findproxy.find_proxies_FreeProxy()

# 2.3. Requests for the apartment and extract the information
for id, url in ad_url_list.items():
    try:
        headers = requestHeaders.init_headers()
        response = requests.get(url, headers=headers, proxies=proxies)
        while 'Captcha' in response.text or 'captcha' in response.text:
            headers = requestHeaders.change_headers()
            proxies = findproxy.find_proxies_FreeProxy()
            response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()
        HTMLInfoExtractor(html_content=response.text, apartmentID=id).extract_all()
    except requests.exceptions.RequestException:
        # Other request errors (e.g., proxy failure), try new proxy
        proxies = findproxy.find_proxies_FreeProxy()
        headers = requestHeaders.change_headers()
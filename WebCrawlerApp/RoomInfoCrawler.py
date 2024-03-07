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
    # Read not extracted ads (Difference between AdsUrlList file and apartmentsData file)
    adsExtractor.delete_duplicates()
    ad_url_list = adsExtractor.ads_roominfo_not_extracted()
    all_ads = adsExtractor.read_url_endings()

    ids_to_delete = [id for id in all_ads.keys() if id not in ad_url_list.keys()]

    if ids_to_delete:
        adsExtractor.delete_inactive_ad(ids_to_delete)
else: 
    ad_url_list = adsExtractor.read_url_endings()
    
# 2.2. Find proxie
proxies = findproxy.find_proxies_FreeProxy()

# 2.3. Requests for the apartment and extract the information
for id, url in ad_url_list.items():
    try:
        headers = requestHeaders.init_headers()
        response = requests.get(url, headers=headers, proxies=proxies)
        while 'Lösung des Captchas' in response.text or 'class="g-recaptcha"' in response.text:
            headers = requestHeaders.change_headers()
            proxies = findproxy.find_proxies_FreeProxy()
            response = requests.get(url, headers=headers, proxies=proxies)
        ad_extract_success = HTMLInfoExtractor(html_content=response.text, apartmentID=id).extract_all()
        if ad_extract_success is False or 'existiert nicht in der Datenbank' in response.text :
            adsExtractor.delete_inactive_ad(id)
            
    except requests.exceptions.RequestException:
        # Other request errors (e.g., proxy failure), try new proxy
        proxies = findproxy.find_proxies_FreeProxy()
        headers = requestHeaders.change_headers()
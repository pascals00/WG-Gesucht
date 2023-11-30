from WebCrawlerApp.helpers.request.suburb_filter import *
from helpers.request.header import *
from WebCrawlerApp.helpers.request.url_manager import *
from helpers.response.extractHtml import *
import requests

# -------------------------------------------------------
# 1. Initial Request for District
# -------------------------------------------------------

suburbFilter = SuburbFilter()
requestHeaders = RequestHeaders()
urlManager = URLManager()

districts = suburbFilter.get_all_districts()
testdistrict = districts[11]

BaseURL = urlManager.set_base_url(filter_apartment=False, filter_wg=True)
header_initialized = False
currentpage_num = 0 

for suburbs in suburbFilter.generate_random_suburb_subsets(testdistrict):
    FilterUrl = urlManager.set_suburb_filter(BaseURL, suburbs[0])
    if header_initialized == False:
        proxies = 0 
        # Here get Proxies from list. proxies =
        headers = requestHeaders.init_headers()
        header_initialized = True


    response = requests.get(FilterUrl, proxies=proxies)
    max_page = extract_max_page(response.text)
    extract_Ads_URL_endings(response.text)

    if max_page > 1:
        for currentpage_num in range(1, max_page):
            nextpage_url = switch_page(FilterUrl, currentpage_num)
            response = requests.get(nextpage_url, proxies=proxies)
            extract_Ads_URL_endings(response.text)



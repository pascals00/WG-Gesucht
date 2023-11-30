from helpers.request.filter_suburbs import *
from helpers.request.header import *
from helpers.request.url import *
from helpers.request.proxies import ProxyManager
from helpers.response.extractHtml import *
import requests

# -------------------------------------------------------
# 1. Initial Request for District
# -------------------------------------------------------

districts = getalldistricts()
testdistrict = districts[11]

BaseURL = set_BaseURL(filter_apartment=False, filter_wg=True)
header_initialized = False
currentpage_num = 0 
ProxyManager = ProxyManager()

for suburbs in generate_random_suburb_subsets(testdistrict):
    FilterUrl = set_suburbfilter(BaseURL, suburbs[0])#.encode('utf-8')
    if header_initialized == False:
        proxies = ProxyManager.find_proxies()
        headers = init_headers()
        header_initialized = True
    else:
        headers = nextpage_headers(headers, FilterUrl, currentpage_num)

    response = requests.get(FilterUrl, proxies=proxies)
    max_page = extract_max_page(response.text)
    extract_Ads_URL_endings(response.text)

    if max_page > 1:
        for currentpage_num in range(1, max_page):
            headers = nextpage_headers(headers, FilterUrl, currentpage_num)
            nextpage_url = switch_page(FilterUrl, currentpage_num)
            response = requests.get(nextpage_url, proxies=proxies)
            extract_Ads_URL_endings(response.text)
            random_delay()



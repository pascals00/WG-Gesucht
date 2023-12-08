from helpers.request.proxy_manager import *
from helpers.request.suburb_filter import *
from helpers.request.header import *
from helpers.request.url_manager import *
from helpers.request.findproxy import *
from helpers.response.extractUrls import *
import requests

# -------------------------------------------------------
# 1. Initial Request for District
# -------------------------------------------------------

suburbFilter = SuburbFilter()
requestHeaders = RequestHeaders()
urlManager = URLManager()
proxyReader = ProxyReader()
findproxy = ProxyManager()


districts = suburbFilter.get_all_districts()
testdistrict = districts[11]

BaseURL = urlManager.set_base_url(filter_apartment=False, filter_wg=True)
header_initialized = False
currentpage_num = 1

for suburbs in suburbFilter.generate_random_suburb_subsets(testdistrict):
    FilterUrl = urlManager.set_suburb_filter(BaseURL, suburbs[0])
    if header_initialized == False:
        proxies = findproxy.find_proxies_FreeProxy()
        headers = requestHeaders.init_headers()
        header_initialized = True
        runningproxie = False


    while True:
        page_url = urlManager.switch_page(FilterUrl, currentpage_num)
        response = requests.get(page_url, proxies=proxies)
        try:
            response.raise_for_status()
            extract_Ads_URL_endings(response.text)
            currentpage_num += 1
        except requests.exceptions.HTTPError:
            break



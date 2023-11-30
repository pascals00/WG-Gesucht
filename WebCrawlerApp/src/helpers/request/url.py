from bs4 import BeautifulSoup
from .filter_suburbs import *

BASE_URL = "https://www.wg-gesucht.de"

def set_BaseURL(filter_wg, filter_apartment): 
    wg_room = 'wg-zimmer'
    apartment = '1-zimmer-wohnung'

    if filter_wg == True and filter_apartment == False: 
        relative_url_apartment_room = '/'+ wg_room + '-in-Berlin.8.0.1.0.html'
    elif filter_wg == False and filter_apartment == True:
        relative_url_apartment_room = '/'+ apartment + '-in-Berlin.8.0.1.0.html'
    else:
        relative_url_apartment_room = '/'+ wg_room + apartment + '-in-Berlin.8.0.1.0.html'
    
    return BASE_URL + relative_url_apartment_room


def set_suburbfilter(url, suburbs):
    filterurl = url + '?offer_filter=1&city_id=8&sort_order=0&noDeact=1&categories[]=0&categories[]=1'
    for suburb, number in suburbs:
        filterurl += f'&ot[]={number}'

    return filterurl


def switch_page(url, pagenumber):
    # Splitting the URL to separate the base URL and the query parameters
    parts = url.split('?')
    base_url = parts[0]

    # Checking if the page number is valid
    if pagenumber >= 1:
        # Modifying the base URL to include the page number
        if 'html' in base_url:
            # If 'html' is present, modify the URL accordingly
            base_url = base_url.rsplit('.', 2)[0] + f'.{pagenumber - 1}.html'
        else:
            base_url += f'.{pagenumber}'

        # Reconstructing the URL with pagination parameter
        if pagenumber == 1:
            page_url = base_url + '?' + parts[1]
            return page_url
        else:
            nextpage_url = base_url + '?' + parts[1] + '&pagination=1&pu=#page-' + str(pagenumber)
            return nextpage_url
    else:
        raise ValueError("Page number must be greater than or equal to 1.")
    



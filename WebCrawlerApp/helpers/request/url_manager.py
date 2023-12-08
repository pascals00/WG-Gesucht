from .suburb_filter import *
from ..constants import *

class URLManager:
    BASE_URL = BASE_URL

    @staticmethod
    def set_base_url(filter_wg, filter_apartment):
        wg_room = 'wg-zimmer'
        apartment = '1-zimmer-wohnung'

        if filter_wg and not filter_apartment:
            relative_url_apartment_room = '/' + wg_room + '-in-Berlin.8.0.1.0.html'
        elif not filter_wg and filter_apartment:
            relative_url_apartment_room = '/' + apartment + '-in-Berlin.8.0.1.0.html'
        else:
            relative_url_apartment_room = '/' + wg_room + apartment + '-in-Berlin.8.0.1.0.html'
        
        return URLManager.BASE_URL + relative_url_apartment_room

    @staticmethod
    def set_suburb_filter(url, suburbs):
        filter_url = url + '?offer_filter=1&city_id=8&sort_order=0&noDeact=1&categories[]=0&categories[]=1'
        for suburb, number in suburbs:
            filter_url += f'&ot[]={number}'
        return filter_url

    @staticmethod
    def switch_page(url, page_number):
        parts = url.split('?')
        base_url = parts[0]

        if page_number >= 1:
            if 'html' in base_url:
                base_url = base_url.rsplit('.', 2)[0] + f'.{page_number - 1}.html'
            else:
                base_url += f'.{page_number}'

            if page_number == 1:
                page_url = base_url + '?' + parts[1]
                return page_url
            else:
                next_page_url = base_url + '?' + parts[1] + '&pagination=1&pu=#page-' + str(page_number)
                return next_page_url
        else:
            raise ValueError("Page number must be greater than or equal to 1.")

from .suburb_filter import *
from ..constants import *
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs

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
        # Parse the URL
        parsed_url = urlparse(url)

        # Existing query parameters
        query_params = parse_qs(parsed_url.query)

        # Add additional parameters
        query_params['offer_filter'] = ['1']
        query_params['city_id'] = ['8']
        query_params['sort_order'] = ['0']
        query_params['noDeact'] = ['1']
        query_params['categories[]'] = ['0', '1']
        query_params['ot[]'] = [str(number) for suburb, number in suburbs]

        # Encode the query string
        encoded_query = urlencode(query_params, doseq=True)

        # Reconstruct the full URL with the encoded query string
        return urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, encoded_query, parsed_url.fragment))

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

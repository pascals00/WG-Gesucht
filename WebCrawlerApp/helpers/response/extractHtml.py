from bs4 import BeautifulSoup
import csv

def extract_max_page(responseHTML):
    # Parse the HTML
    soup = BeautifulSoup(responseHTML, 'html.parser')
    # Find all the page-link elements
    page_links = soup.find_all('a', class_='page-link')
    # Extract the numbers from the page links and find the maximum
    max_page = max(int(link.get_text()) for link in page_links if link.get_text().isdigit())

    if max_page is not None:
        return max_page
    else:
        max_page = 0 
        return 
    
def extract_Ads_URL_endings(responseHTML): 
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(responseHTML, 'html.parser')

    # Find all the ads and extract their IDs and URL endings
    ads = soup.find_all('div', class_='wgg_card offer_list_item')
    url_dict = {}

    for ad in ads:
        ad_id = ad.get('data-id')
        url_ending = ad.find('a', href=True)['href']
        url_dict[ad_id] = url_ending
    
    store_Ads_URL_endings_in_csv(url_dict)  


def store_Ads_URL_endings_in_csv(url_dict):
    with open('data/output/ADsURLList.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for ad_id, url_ending in url_dict.items():
            writer.writerow([ad_id, url_ending])
    print("New ads URL endings saved to ads_url_endings.csv.")
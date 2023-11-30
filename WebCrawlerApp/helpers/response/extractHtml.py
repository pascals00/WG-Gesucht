from bs4 import BeautifulSoup
import csv
    
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
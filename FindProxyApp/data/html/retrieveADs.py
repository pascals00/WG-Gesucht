from bs4 import BeautifulSoup

PATH = "data/html/ad/resultlistADs.html"

with open(PATH, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the ads and extract their IDs and URL endings
ads = soup.find_all('div', class_='wgg_card offer_list_item')
url_dict = {}

for ad in ads:
    ad_id = ad.get('data-id')
    url_ending = ad.find('a', href=True)['href']
    url_dict[ad_id] = url_ending

for ad_id, url in url_dict.items():
    print(f"Ad ID: {ad_id}, URL Ending: {url}")

print(len(url_dict))
from bs4 import BeautifulSoup

PATH = "data/html/ad/resultlistADs.html"

with open(PATH, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the page-link elements
page_links = soup.find_all('a', class_='page-link')

# Extract the numbers from the page links and find the maximum
max_page = max(int(link.get_text()) for link in page_links if link.get_text().isdigit())

print(max_page)

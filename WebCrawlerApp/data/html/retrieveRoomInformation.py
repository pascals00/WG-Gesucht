from bs4 import BeautifulSoup


class HTMLInfoExtractor:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract_rental_information(self):
        title = self.soup.find('h1', class_='headline').get_text(strip=True)
        footer_details = self.soup.find('div', class_='section_footer_dark')
        details = footer_details.find_all('b', class_='key_fact_value')

        room_size = details[0].get_text(strip=True) if len(details) > 0 else "Not specified"
        total_rent = details[1].get_text(strip=True) if len(details) > 1 else "Not specified"

        return {
            "Title": title,
            "Room Size": room_size,
            "Total Rent": total_rent
        }

    def extract_address(self):
        address_section = self.soup.find('h3', text='Adresse').find_next('div', class_='row')
        address = address_section.find('span', class_='section_panel_detail').get_text(strip=True)
        return address

    def extract_availability(self):
        availability_section = self.soup.find('h3', text='Verfügbarkeit').find_next('div', class_='row')
        frei_ab = availability_section.find('span', class_='section_panel_detail', text='frei ab:').find_next('span').get_text(strip=True)
        frei_bis_section = availability_section.find('span', class_='section_panel_detail', text='frei bis:')
        frei_bis = frei_bis_section.find_next('span').get_text(strip=True) if frei_bis_section else "Not specified"
        return frei_ab, frei_bis

    def extract_online_status(self):
        online_status_section = self.soup.find('span', text='Online:').find_next('b')
        online_status = online_status_section.get_text(strip=True) if online_status_section else "Not specified"
        return online_status

    def extract_costs(self):
        costs_data = []
        cost_items = self.soup.find_all('div', class_='row')[1:]  # Skip the first row which is the title

        for item in cost_items:
            detail = item.find('span', class_='section_panel_detail').get_text(strip=True)
            value = item.find('span', class_='section_panel_value').get_text(strip=True)
            costs_data.append({"Cost Detail": detail, "Amount": value})

        return costs_data
        
    def extract_wg_details(self):
        wg_details = []
        wg_details_section = self.soup.find('h3', text='WG-Details')

        if wg_details_section:
            details_list = wg_details_section.find_next('ul').find_all('li')
            for detail in details_list:
                text = detail.get_text(strip=True)
                wg_details.append(text)

        return wg_details

    def extract_object_details(self):
        object_details = []
        object_details_section = self.soup.find('h3', text='Angaben zum Objekt')

        if object_details_section:
            utility_icons = object_details_section.find_next_sibling('div').find_all('div', class_='text-center')

            for icon in utility_icons:
                detail = icon.get_text(strip=True)
                object_details.append(detail)

        return object_details

    def extract_required_documents(self):
        required_documents = []
        documents_section = self.soup.find('h3', text=lambda text: text and 'Benötigte Unterlagen' in text)

        if documents_section:
            utility_icons = documents_section.find_next('div', class_='utility_icons').find_all('div', class_='text-center')

            for icon in utility_icons:
                document = icon.get_text(strip=True)
                required_documents.append(document)

        return required_documents


# Usage example:
html_content_path = "WebCrawlerApp/data/html/ad/roomAD1.html"
with open(html_content_path, "r", encoding="utf-8") as file:
    html_content = file.read()

extractor = HTMLInfoExtractor(html_content)
print(extractor.extract_rental_information())
print(extractor.extract_address())
print(extractor.extract_availability())
print(extractor.extract_online_status())
print(extractor.extract_costs())
print(extractor.extract_wg_details())
print(extractor.extract_object_details())
print(extractor.extract_required_documents())





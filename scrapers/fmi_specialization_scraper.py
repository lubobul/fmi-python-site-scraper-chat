import requests
from bs4 import BeautifulSoup
from models.models import SpecializationModel, ProgramLinkModel
from typing import List

def scrape_specializations(url: str) -> List[SpecializationModel]:
    # Send a GET request to the webpage
    response = requests.get(url)

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table with class "edu_gratbl"
    table = soup.find('table', class_='edu_gratbl')
    programs = []
    if table:
        # Extract rows from the table
        for row in table.find_all('tr')[1:]:  # Skip the header row
            cells = row.find_all('td')
            if cells[0].find('strong'):
                specialization_name = cells[0].get_text().strip()
                specialization_name = specialization_name.replace('\xa0', '')
                specialization = SpecializationModel(specialization_name, [])
                programs.append(specialization)

                if cells[1].find('a') or cells[2].find('a'):
                    specialization_link = ProgramLinkModel(specialization_name)
                    specialization_link.winter_link = cells[1].find('a').get('href') if cells[1].find('a') else None
                    specialization_link.summer_link = cells[2].find('a').get('href') if cells[2].find('a') else None
                    specialization.programs.append(specialization_link)
            else:
                link_name = cells[0].get_text().strip()
                specialization_link = ProgramLinkModel(link_name)
                specialization_link.winter_link = cells[1].find('a').get('href') if cells[1].find('a') else None
                specialization_link.summer_link = cells[2].find('a').get('href') if cells[2].find('a') else None
                specialization.programs.append(specialization_link)
    return programs




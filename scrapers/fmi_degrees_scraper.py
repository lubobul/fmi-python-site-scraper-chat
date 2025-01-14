import requests
from bs4 import BeautifulSoup
from models.models import ProgramModel, ProgramLinkModel
from typing import List

def scrape_degrees(url: str) -> List[ProgramModel]:
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
                degree_name = cells[0].get_text().strip()
                program = ProgramModel(degree_name, [])
                programs.append(program)

                if cells[1].find('a') or cells[2].find('a'):
                    program_link = ProgramLinkModel(degree_name)
                    program_link.winter_link = cells[1].find('a').get('href') if cells[1].find('a') else None
                    program_link.summer_link = cells[2].find('a').get('href') if cells[2].find('a') else None
                    program.links.append(program_link)
            else:
                link_name = cells[0].get_text().strip()
                program_link = ProgramLinkModel(link_name)
                program_link.winter_link = cells[1].find('a').get('href') if cells[1].find('a') else None
                program_link.summer_link = cells[2].find('a').get('href') if cells[2].find('a') else None
                program.links.append(program_link)
    return programs




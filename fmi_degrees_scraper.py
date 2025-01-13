import requests
from bs4 import BeautifulSoup
from models import DegreeModel, DegreeLinkModel
from typing import List

def scrape_degrees(url: str) -> List[DegreeModel]:
    # Send a GET request to the webpage
    response = requests.get(url)

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table with class "edu_gratbl"
    table = soup.find('table', class_='edu_gratbl')

    if table:
        # Extract rows from the table
        disciplinesRaw = []
        for row in table.find_all('tr')[1:]:  # Skip the header row
            cells = row.find_all('td')
            degree_name = cells[0].get_text().strip()
            if cells[0].find('strong'):
                degree_name = cells[0].get_text().strip()


                print(degree_name)




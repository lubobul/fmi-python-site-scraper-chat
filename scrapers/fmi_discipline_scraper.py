import requests
from bs4 import BeautifulSoup
from models.models import DisciplineModelRaw, DisciplineVariantModel, DisciplineModel
from typing import List

def scrape_disciplines(url: str) -> List[DisciplineModel]:
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
            time = cells[0].get_text().strip()
            discipline_and_lecturer = cells[1].get_text(separator='|').split('|')
            if len(discipline_and_lecturer) == 2:
                disciplineName = discipline_and_lecturer[0].strip()
                lecturer = discipline_and_lecturer[1].strip()
            else:
                disciplineName = cells[1].get_text().strip()
                lecturer = ""
            type = cells[2].get_text().strip()
            cabinetNumber = cells[3].get_text().strip()

            discipline = DisciplineModelRaw(time, disciplineName, lecturer, type, cabinetNumber)
            disciplinesRaw.append(discipline)
        
        disciplinesRaw = [d for d in disciplinesRaw if d.discipline]

        # Create a dictionary to hold unique disciplines as keys and list of records as values
        discipline_map = {}
        for disciplineRaw in disciplinesRaw:
            if disciplineRaw.discipline not in discipline_map:
                discipline_map[disciplineRaw.discipline] = []
            discipline_map[disciplineRaw.discipline].append(disciplineRaw)

        # Create the populated DisciplineModel instances
        discipline_models = []
        discipline_id_counter = 1  # Initialize a counter for unique discipline IDs
        for discipline_name, records in discipline_map.items():
            discipline_variants = []
            for record in records:
                variant = DisciplineVariantModel(
                    discipline_id=discipline_id_counter,
                    lecturer=record.lecturer,
                    time=record.time,
                    discipline_type=record.type,
                    cabinet_number=record.cabinetNumber
                )
                discipline_variants.append(variant)
                discipline_id_counter += 1
            discipline_model = DisciplineModel(discipline_name=discipline_name, discipline_list=discipline_variants)
            discipline_models.append(discipline_model)

        return discipline_models
    else:
        print("Table with class 'edu_gratbl' not found.")
        return []


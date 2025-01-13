# models.py
from typing import List

class DisciplineVariantModel:
    def __init__(self, discipline_id: int, lecturer: str, time: str, discipline_type: str, cabinet_number: str):
        self.disciplineId = discipline_id
        self.lecturer = lecturer
        self.time = time
        self.type = discipline_type
        self.cabinetNumber = cabinet_number

class DisciplineModel:
    def __init__(self, discipline_name: str, discipline_list: List[DisciplineVariantModel]):
        self.disciplineName = discipline_name
        self.disciplineList = discipline_list

class DisciplineModelRaw:
    def __init__(self, time: str, discipline: str, lecturer: str, type: str, cabinet_number: str):
        self.time = time
        self.discipline = discipline
        self.lecturer = lecturer
        self.type = type
        self.cabinetNumber = cabinet_number

class DegreeLinkModel:
    def __init__(self, link_title: str, link: str):
        self.link_title = link_title
        self.link = link

class DegreeModel:
    def __init__(self, degree_name: str, links: List[DegreeLinkModel]):
        self.degree_name = degree_name
        self.links = links
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

class ProgramLinkModel:
    def __init__(self, link_title: str, summer_link: str = None, winter_link: str= None):
        self.link_title = link_title
        self.summer_link = summer_link
        self.winter_link = winter_link

class ProgramModel:
    def __init__(self, program_name: str, links: List[ProgramLinkModel]):
        self.program_name = program_name
        self.links = links
# models.py
from typing import List

class DisciplineVariantModel:
    def __init__(self, disciplineId: int, lecturer: str, time: str, type: str, cabinetNumber: str):
        self.disciplineId = disciplineId
        self.lecturer = lecturer
        self.time = time
        self.type = type
        self.cabinetNumber = cabinetNumber

class DisciplineModel:
    def __init__(self, disciplineName: str, disciplineList: List[DisciplineVariantModel]):
        self.disciplineName = disciplineName
        self.disciplineList = disciplineList

class DisciplineModelRaw:
    def __init__(self, time: str, discipline: str, lecturer: str, type: str, cabinetNumber: str):
        self.time = time
        self.discipline = discipline
        self.lecturer = lecturer
        self.type = type
        self.cabinetNumber = cabinetNumber

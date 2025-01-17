from scrapers.fmi_discipline_scraper import scrape_disciplines
from scrapers.fmi_specialization_scraper import scrape_specializations

def main():

    url = "https://fmi-plovdiv.org/index.jsp?ln=1&id=1384"
    programs = scrape_specializations(url)
    for program in programs:
        print(f"Degree Name: {program.specialization_name}")
        for link in program.programs:
            print(f" Link Title: {link.program_name}")
            print(f" Winter Link: {link.winter_link}")
            print(f" Summer Link: {link.summer_link}")

    url = "https://fmi-plovdiv.org/index.jsp?id=4792&ln=1"
    discipline_models = scrape_disciplines(url)
    for model in discipline_models:
        print(f"Discipline Name: {model.disciplineName}")
        for variant in model.disciplineList:
            print(f"  ID: {variant.disciplineId}, Time: {variant.time}, Lecturer: {variant.lecturer}, Type: {variant.type}, Cabinet: {variant.cabinetNumber}")

if __name__ == "__main__":
    main()

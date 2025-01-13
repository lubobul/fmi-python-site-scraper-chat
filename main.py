from fmi_scraper import scrape_disciplines

def main():
    url = "https://fmi-plovdiv.org/index.jsp?id=4792&ln=1"
    discipline_models = scrape_disciplines(url)
    for model in discipline_models:
        print(f"Discipline Name: {model.disciplineName}")
        for variant in model.disciplineList:
            print(f"  ID: {variant.disciplineId}, Time: {variant.time}, Lecturer: {variant.lecturer}, Type: {variant.type}, Cabinet: {variant.cabinetNumber}")

if __name__ == "__main__":
    main()

# fmi-python-site-scraper-chat
This repository is used for educational purposes

We are going to create a chat for answering questions such as:
- What sujects do I have this semester?
- When do I have to go to the university this week?

By using a scraper and feeding the data into a chat model.

Everything should be written in Python!

# How to run the project
python3 -m venv fmi-scraper-virtual-env
source fmi-scraper-virtual-env/bin/activate
pip3 install requests beautifulsoup4
python3 main.py

# Chat interaction model
##  Phase 1
A: Please type help, if you'd like to know anything.
Q: Help
A: List of all root commands
Q: Give the all specializations for the master degree program in FMI
A: {{All the specializations from the FMI website}}
Q: Give me info about {{specialization name}}
A: {{Available years of education}}
Q: {{Specific year + specific course}}
A: Available seasons {{list of seasons - winter / summer}}. Pick either.
Q: {{Season}}
A: {{List of all disciplines}}. Which one do you want to know more about?
Q: {{A specific discipline}}
A: {{The dates | the room | the lecturer | the type (lecture / exercises)}}

## Phase 2 (optional)
Q: What courses do I have this week?
A: {{The dates | the room | the lecturer | the type (lecture / exercises)}}

## Chat user interface
Angular application

# Model of the srcraped raw data
## Master's degree page model
- Specialization: string
- courseVariations: CourseVariant

### Course Variant model
- name: string
- season: string[] - "winter" | "summer"

## Model of the specific specialization page 
- disciplineName: string
- dateTime: Date
- type: string
- cabinetNumber: string

# MVP of this project
## Chat interaction model
A: Please type help, if you'd like to know anything.
Q: Help
A: List of all root commands
Q: Which disciplines do I have?
A: {{List of all disciplines}}. Which one do you want to know more about?
Q: {{A specific discipline}}
A: List of {{The dates | the room | the lecturer | the type (lecture / exercises)}}

## Chat user interface
For the MVP we are going to interact with the chat via the terminal

## Business models
### ChatModel
- disciplineName: string
- disciplineList: DisciplineModel[]

### DisciplineModel
- disciplineId: number
- time: string
- type: disciplineType
- cabinetNumber: string
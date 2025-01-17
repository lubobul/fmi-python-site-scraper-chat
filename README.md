# fmi-python-site-scraper-chat

This repository is used for educational purposes

We are going to create a chat for answering questions such as:

- What sujects do I have this semester?
- When do I have to go to the university this week?

By using a scraper and feeding the data into a chat model.

Everything should be written in Python!

# Chat interaction model

## Phase 1

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

# Chatbot


# Building blocks of the Chatbot
## REST API
The rest API is build using **flask**.
The [chatbot_controller.py](controllers%2Fchatbot_controller.py) serves as the core of the Chatbot. It handles user queries by matching them to a predefined set of questions. The Chatbot uses the scraped data to generate human-readable responses to the HTTP requests from the client.

## Scrapers
The scrapers [fmi_discipline_scraper.py](scrapers%2Ffmi_discipline_scraper.py), [fmi_specialization_scraper.py](scrapers%2Ffmi_specialization_scraper.py) use **BeautifulSoup**
to scrape data from the FMI website. It transforms and normalizes the scraped data, in preparation
for consumption in the REST API

## UI
The Chatbot UI is written using Angular 19. The chat design is realized using Flex box model.

## Integrating the UI Chat into the FMI Website via HTTP Proxy
The idea behind this proxy, is to fetch the FMI website and inject the UI application along
with some javascript that modifies the DOM. This gives us the ability to demonstrate the chat
as being integrated in the FMI website. This is realized via the injection of a new menu item called "**Чат Бот**"
When clicked, an injected script by the proxy, is triggered and replaces the page main content
with an **iframe** hosting the UI Angular application.

# How to run the Chatbot

## Run python virtual environment
```
python3 -m venv fmi-scraper-virtual-env
source fmi-scraper-virtual-env/bin/activate
pip3 install flask flask_cors requests beautifulsoup4
```
Then you can simply run the [run.sh](run.sh) which will essentially run all the commands bellow.

## Run the python chat REST server
```
python3 app.py
```

## Run the chat Front-end

```
cd chat-ui
npm ci
npm start
```

## Run the FMI website proxy
python3 fmi_website_proxy.py

## How to test the FMI chatbot
Using a Chrome browser go to http://localhost:12345

# Postman

POST http://127.0.0.1:5000/api/chatbot

Request body:

```
{
    "question": "Кога ми е следващият час?"
}
```

Response body:

```
{
    "message": "Следващият час е на: 18.01.2025 по дисциплината Избираема дисциплина 1 в кабинет 547 к.з."
}
```

## Information command

GET http://127.0.0.1:5000/api/help

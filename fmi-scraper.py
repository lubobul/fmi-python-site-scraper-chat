import requests
from bs4 import BeautifulSoup

# URL of the webpage you want to scrape
url = "https://fmi-plovdiv.org/"

# Send a GET request to the webpage
response = requests.get(url)

# Create a BeautifulSoup object and specify the parser
soup = BeautifulSoup(response.content, 'html.parser')

# Find the elements you want to extract (example: all paragraph texts)
paragraphs = soup.find_all('p')

# Print the text content of each paragraph
for paragraph in paragraphs:
    print(paragraph.get_text())

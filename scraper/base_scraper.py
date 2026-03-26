import requests
from bs4 import BeautifulSoup

def coleta_materia(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')
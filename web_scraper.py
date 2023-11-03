import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def get_appointments() -> bool:
    response = requests.get(os.getenv('URL'))
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html5lib')
        rows = soup.find('tr', attrs = { 'class' : 'table-row' })
        return len(rows) > 0
    
def get_protocol(protocolo: str):
    response = requests.get(os.getenv('URL_PROTOCOL') + protocolo)
    
    if (response.status_code == 200):
        return response.json()
    return
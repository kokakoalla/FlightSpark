import os #Tuodaan os-moduuli 
from dotenv import load_dotenv #Tuodaan load_dotenv-funktio dotenv-moduulista // .env tiedosto

load_dotenv()  # .env-tiedoston lataaminen

class Config: #Määritellään Config-luokka
    API_KEY = os.getenv('API_KEY') #Haetaan API_KEY ympäristömuuttujasta
    TEQUILA_ENDPOINT_LOCATION = 'https://tequila-api.kiwi.com' #Määritellään TEQUILA_ENDPOINT_LOCATION-muuttuja
    DATABASE_URL = os.getenv('DATABASE_URL') #Haetaan DATABASE_URL ympäristömuuttujasta

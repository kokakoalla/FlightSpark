import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv('API_KEY')
    TEQUILA_ENDPOINT_LOCATION = 'https://tequila-api.kiwi.com'
    DATABASE_URL = os.getenv('DATABASE_URL')

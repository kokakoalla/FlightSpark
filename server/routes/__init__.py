import logging #Tuodaan logging-moduuli
from quart import Quart, send_from_directory #Tuodaan Quart-moduuli
from .flight import flight_bp #Tuodaan flight_bp Blueprint-moduuli
from .location import location_bp #Tuodaan location_bp Blueprint-moduuli
from .radius import radius_bp #Tuodaan radius_bp Blueprint-moduuli
from .config import Config #Tuodaan Config-moduuli
from apscheduler.schedulers.asyncio import AsyncIOScheduler #Tuodaan AsyncIOScheduler-moduuli
from apscheduler.triggers.interval import IntervalTrigger #Tuodaan IntervalTrigger-moduuli
import asyncpg #Tuodaan asyncpg-moduuli
import asyncio #Tuodaan asyncio-moduuli
import datetime #Tuodaan datetime-moduuli
from quart_cors import cors


logging.basicConfig(level=logging.INFO) # Määritetään perusasetukset loggingille, INFO-tasolla
logger = logging.getLogger(__name__) #Luodaan logger-olio

def create_app(): #Määritellään funktio, joka luo sovelluksen
    # app = Quart(__name__, static_folder='/var/www/html/dist') #Luodaan Quart-sovellus
    app = Quart(__name__) #Luodaan Quart-sovellus

    app = cors(app, allow_origin="*")

    app = Quart(__name__) #Luodaan Quart-sovellus
    # app.static_folder = '/var/www/html/dist'
    
    app.register_blueprint(location_bp) #Rekisteröidään reititys location_bp:sta
    app.register_blueprint(flight_bp) #Rekisteröidään reititys flight_bp:sta
    app.register_blueprint(radius_bp) #Rekisteröidään reititys radius_bp:sta




    return app #Palautetaan sovellus



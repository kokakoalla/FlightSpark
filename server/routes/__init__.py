import logging #Tuodaan logging-moduuli
from quart import Quart #Tuodaan Quart-moduuli
from .flight import flight_bp #Tuodaan flight_bp Blueprint-moduuli
from .location import location_bp #Tuodaan location_bp Blueprint-moduuli
from .radius import radius_bp #Tuodaan radius_bp Blueprint-moduuli
from .config import Config #Tuodaan Config-moduuli
from apscheduler.schedulers.asyncio import AsyncIOScheduler #Tuodaan AsyncIOScheduler-moduuli
from apscheduler.triggers.interval import IntervalTrigger #Tuodaan IntervalTrigger-moduuli
import asyncpg #Tuodaan asyncpg-moduuli
import asyncio #Tuodaan asyncio-moduuli
import datetime #Tuodaan datetime-moduuli

# logging.basicConfig(level=logging.INFO) # Määritetään perusasetukset loggingille, INFO-tasolla
# logger = logging.getLogger(__name__) #Luodaan logger-olio

async def cleanup_old_records(app): #Määritellään asynkroninen funktio, joka poistaa vanhat tietueet
    async with app.db_pool.acquire() as con: #Luodaan asynkroninen yhteys tietokantaan
        current_time = datetime.datetime.now().timestamp() #Haetaan nykyinen Unix-aika
        time_10_days_ago = (datetime.datetime.now() + datetime.timedelta(days=10)).timestamp() #Haetaan Unix-aika 10 päivää eteenpäin
        
        logger.info(f"Current Unix time: {current_time}") #Tulostetaan nykyinen Unix-aika
        logger.info(f"Unix time 10 days ago: {time_10_days_ago}") #Tulostetaan Unix-aika 10 päivää eteenpäin

        old_records = await con.fetch('''  
            SELECT * FROM search_history
            WHERE date_time < $1
        ''', time_10_days_ago) #Haetaan vanhat tietueet tietokannasta, 10 päivää eteenpäin
        
        # if old_records:    #Jos vanhoja tietueita löytyy
        #     logger.info(f"Old records to be deleted: {old_records}") #Tulostetaan vanhat tietueet
        # else: #Jos vanhoja tietueita ei löydy
        #     logger.info("No old records found.") #Tulostetaan, ettei vanhoja tietueita löytynyt

        await con.execute('''
            DELETE FROM search_history
            WHERE date_time < $1
        ''', time_10_days_ago) #Postetaan vanhat tietueet tietokannasta
        # logger.info("Old records deleted successfully.")

def start_scheduler(app): #Määritellään funktio, joka käynnistää ajastimen
    scheduler = AsyncIOScheduler() #Luodaan asynkrooninen aikatauluttaja
    scheduler.add_job(cleanup_old_records, IntervalTrigger(days=1), args=[app]) # days=1 // Suoritetaan cleanup_old_records-funktio joka päivä
    scheduler.start() #Käynnistetään aikatauluttaja

def create_app(): #Määritellään funktio, joka luo sovelluksen
    app = Quart(__name__) #Luodaan Quart-sovellus
    
    app.register_blueprint(location_bp) #Rekisteröidään reititys location_bp:sta
    app.register_blueprint(flight_bp) #Rekisteröidään reititys flight_bp:sta
    app.register_blueprint(radius_bp) #Rekisteröidään reititys radius_bp:sta

    @app.before_serving # Määritellään funktio, joka luo tietokannan yhteyden ennen sovelluksen käynnistämistä
    async def create_db_pool(): #Määritellään asynkroninen funktio, joka luo tietokannan yhteyden
        app.db_pool = await asyncpg.create_pool(Config.DATABASE_URL) #Luodaan tietokannan yhteys

    @app.after_serving # Määritellään funktio, joka sulkee tietokannan yhteyden sovelluksen sulkemisen jälkeen
    async def close_db_pool(): #Määritellään asynkroninen funktio, joka sulkee tietokannan yhteyden
        await app.db_pool.close() #Suljetaan tietokannan yhteys

    return app #Palautetaan sovellus



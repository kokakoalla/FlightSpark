from quart import Blueprint, request, jsonify #Tuodaan tarvittavat moduulit 
import aiohttp #Tuodaan aiohttp-moduuli
from .config import Config                          #Tuodaan Config-luokka config-moduulista
import asyncpg                                  #Tuodaan asyncpg-moduuli
import datetime                                 #   Tuodaan datetime-moduuli
import time                                     #Tuodaan time-moduuli
from .database import get_database_connection   #Tuodaan get_database_connection-funktio database-moduulista
import logging #                                Tuodaan logging-moduuli

# Määritellään muuttujat, jotka sisältävät päivämäärät 10 ja 20 päivää eteenpäin
aika_nyt = datetime.datetime.now().date()
date_plus_10 = aika_nyt + datetime.timedelta(days=10)
new_date_plus_10 = date_plus_10.strftime("%Y-%m-%d")
date_plus_20 = aika_nyt + datetime.timedelta(days=20)
new_date_plus_20 = date_plus_20.strftime("%Y-%m-%d")

logging.basicConfig(level=logging.INFO) #Määritetään perusasetukset loggingille, INFO-tasolla
logger = logging.getLogger(__name__) #Luodaan logger-olio   

#Luodaan Blueprint radius reititys
radius_bp = Blueprint('radius', __name__) 

#Määritellään asynkroninen funktio, joka hakee tietueet tietokannasta
async def fetch_search_history(con, location_code): 
    query = '''
    SELECT DISTINCT ON (to_city) from_city, to_city, url, price, to_id
    FROM search_history 
    WHERE from_id = $1 and stopovers = 0 and adults = 1
    order by to_city, id desc, price desc
    LIMIT 3; 
    '''
    search_history = await con.fetch(query, location_code) #Etsitään tietueet tietokannasta // location_code - nykyinen sijainti(lentoaseman koodi)
    return [{'cityFrom': res['from_city'], 'cityTo': res['to_city'], 'price': res['price'], 'deep_link': res['url']}
            for res in search_history]

async def fetch_from_kiwi(session, url, params, headers): #Määritellään asynkroninen funktio fetch_from_kiwi, joka ottaa vastaan session, url, params ja headers parametrit
    async with session.get(url, params=params, headers=headers) as response: #Tehdään GET-pyyntö Kiwi API:lle
        if response.status != 200: #Jos vastauskoodi ei ole 200
            raise Exception('Failed to fetch data from Kiwi API') #Heitetään poikkeus
        return await response.json() #Muutetaan vastaus JSON-muotoon

async def save_fligth_data(con, data): #Määritellään asynkroninen funktio save_fligth_data, joka ottaa vastaan con ja data parametrit
    for flight_data in data: #Käydään läpi data
        await con.execute('''
            INSERT INTO search_history (from_city, to_city, price, date_time, url, from_id, to_id, local_arrival, local_departure, stopovers, adults)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        ''', flight_data.get('cityFrom', 'N/A'), flight_data.get('cityTo', 'N/A'), flight_data.get('price', 'N/A'),
        int(time.time()), flight_data.get('deep_link', 'N/A'), flight_data.get('cityCodeFrom', 'N/A'),
        flight_data.get('cityCodeTo', 'N/A'), flight_data.get('local_arrival', 'N/A'), flight_data.get('local_departure', 'N/A'),
        len(flight_data.get('route', [])) - 1, 1)

@radius_bp.route('/api/location/radius', methods=['GET']) # Määritellään reitti /api/location/radius, joka ottaa vastaan vain GET-pyyntöjä
async def receive_location(): #Määritellään asynkroninen funktio receive_location
    latitude = request.args.get('latitude') # Haetaan latitude-parametri pyynnöstä
    longitude = request.args.get('longitude') # Haetaan longitude-parametri pyynnöstä

    if not latitude or not longitude: #Jos latitude tai longitude puuttuu
        return jsonify({'error': 'Missing latitude or longitude'}), 400 # Palautetaan virheilmoitus ja statuskoodi 400

    logger.info(f"Received location: {latitude}, {longitude}") #Tulostetaan lokitiedot
    try:  #Yritetään suorittaa seuraava koodi
        async with aiohttp.ClientSession() as session: # Luodaan asynkroninen HTTP-istunto
            kiwi_data = await fetch_from_kiwi( #Haetaan data Kiwi API:sta
                session, #Session
                f'{Config.TEQUILA_ENDPOINT_LOCATION}/locations/radius', #URL
                params={'lat': latitude, 'lon': longitude, 'radius': 500}, #Parametrit
                headers={'apikey': Config.API_KEY}) #Otsikot
            if 'locations' in kiwi_data:    # Jos 'locations' löytyy kiwi_datasta
                location = kiwi_data['locations'][0] # Otetaan ensimmäinen sijainti
                logger.info(f"Location: {location}") #Tulostetaan lokitiedot
                if 'code' in location:               # Jos 'code' löytyy sijainnista
                    code_location = location['code']    # Tehdään code_location-muuttuja, joka sisältää sijainnin koodin joka auttaa tulevaisuudessa estämään virheitä, jos lentokentästä ei ole lentoja
                    logger.info(f'Location code: {code_location}')
                    # if len(code_location) != 3:
                    #     code_location = 'HEL' #Jos code_location on suurempi kuin 0
                    # code_location = 'HEL'
                    con = await get_database_connection() #Haetaan tietokannan yhteys
                    try:
                        db_data = await fetch_search_history(con, code_location)    
                        logger.info(f"db_data: {db_data}")
                        if len(db_data) > 2:
                            return jsonify(db_data)  
                        else:      # Tarvitsemme 3 korttia
                            date_from = new_date_plus_10 #  Lentojen päivämäärä 10 päivää eteenpäin
                            date_to = new_date_plus_20  #  Lentojen päivämäärä 20 päivää eteenpäin (haku 10 -20 pv eteenpäin)
                            logger.info(f"Fetching data from Kiwi API for location: {code_location}") #Tulostetaan lokitiedot
                            kiwi_data = await fetch_from_kiwi(
                                session,
                                f'{Config.TEQUILA_ENDPOINT_LOCATION}/v2/search',
                                params={'fly_from': code_location, 'date_from': date_from, 'date_to': date_to, 'limit': 10},
                                headers={'apikey': Config.API_KEY}  #Haetaan satunnaisia lentoja Kiwi API:sta (10-20 pv eteenpäin)
                            )
                            data = kiwi_data.get('data', []) # Talleneteaan data-muuttujaan data Kiwi API:sta
                            logger.info(f"Data from kiwi: {data}")

             
                        await save_fligth_data(con, data)  #Tallenetaan data tietokantaan
                        db_data = await fetch_search_history(con, code_location) #Haetaan tietueet tietokannasta
                        logger.info(f"db_data_last: {db_data}") 
                        return jsonify(db_data) #Palautetaan tietueet JSON-muodossa
                    finally:
                        await con.close()
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        return jsonify({'error': f'An error occurred final: {e}'}), 500

    return jsonify({'error': 'No location code found'}), 404

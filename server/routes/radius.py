from quart import Blueprint, request, jsonify #Tuodaan tarvittavat moduulit 
import aiohttp #Tuodaan aiohttp-moduuli
from .config import Config  #Tuodaan Config-luokka config-moduulista
import asyncpg  #Tuodaan asyncpg-moduuli
import datetime     #Tuodaan datetime-moduuli
import time     #Tuodaan time-moduuli
from .database import get_database_connection #Tuodaan get_database_connection-funktio database-moduulista


# Määritellään muuttujat, jotka sisältävät päivämäärät 10 ja 20 päivää eteenpäin
aika_nyt = datetime.datetime.now().date()
date_plus_10 = aika_nyt + datetime.timedelta(days=10)
new_date_plus_10 = date_plus_10.strftime("%Y-%m-%d")
date_plus_20 = aika_nyt + datetime.timedelta(days=20)
new_date_plus_20 = date_plus_20.strftime("%Y-%m-%d")


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

@radius_bp.route('/api/location/radius', methods=['GET']) # Määritellään reitti /api/location/radius, joka ottaa vastaan vain GET-pyyntöjä
async def receive_location(): #Määritellään asynkroninen funktio receive_location
    latitude = request.args.get('latitude') # Haetaan latitude-parametri pyynnöstä
    longitude = request.args.get('longitude') # Haetaan longitude-parametri pyynnöstä

    if not latitude or not longitude: #Jos latitude tai longitude puuttuu
        return jsonify({'error': 'Missing latitude or longitude'}), 400 # Palautetaan virheilmoitus ja statuskoodi 400

    try:  #Yritetään suorittaa seuraava koodi
        async with aiohttp.ClientSession() as session: # Luodaan asynkroninen HTTP-istunto
            async with session.get(             # Tehdään GET-pyyntö Kiwi API:lle
                f'{Config.TEQUILA_ENDPOINT_LOCATION}/locations/radius',
                params={
                    'lat': latitude,
                    'lon': longitude,
                    'radius': 250,
                    'locale': 'en-US',
                    'location_types': 'airport',
                    'limit': 1
                },
                headers={'apikey': Config.API_KEY} # Lisätään API-avain
            ) as kiwi_response: # Tallennetaan vastaus muuttujaan kiwi_response
                if kiwi_response.status != 200:     #Jos vastauskoodi ei ole 200
                    return jsonify({'error': 'Failed to fetch data from Kiwi API'}), 500    # Palautetaan virheilmoitus ja statuskoodi 500
                
                kiwi_data = await kiwi_response.json() # Odotetaan ja muutetaan vastaus JSON-muotoon
                if 'locations' in kiwi_data: #Jos locations löytyy kiwi_datasta
                    location = kiwi_data['locations'][0]   #Haetaan ensimmäinen sijainti 'locations' avaimesta
                    if 'code' in location: #Jos 'code' avain löytyy locationista
                        con = await get_database_connection() #Haetaan tietokannan yhteys
                        try:
                            db_data = await fetch_search_history(con, location['code'])

                            if len(db_data) < 3:
                                date_from = new_date_plus_10
                                date_to = new_date_plus_20
                                async with session.get(
                                    'https://api.tequila.kiwi.com/v2/search',
                                    params={
                                        'fly_from': location['code'],
                                        'date_from': date_from,
                                        'date_to': date_to,
                                        'adults': 1,
                                        'limit': 3
                                    },
                                    headers={'apikey': Config.API_KEY, 'Content-Type': 'application/json'}
                                ) as kiwi_response:
                                    if kiwi_response.status != 200:
                                        return jsonify({'error': 'Failed to fetch data from Kiwi API'}), 500
                                    
                                    kiwi_data = await kiwi_response.json()
                                    if 'data' in kiwi_data:
                                        data = kiwi_data['data']
                                        for flight_data in data:
                                            await con.execute('''
                                                INSERT INTO search_history (from_city, to_city, price, date_time, url, from_id, to_id, local_arrival, local_departure, stopovers, adults)
                                                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                                            ''', flight_data.get('cityFrom', 'N/A'), flight_data.get('cityTo', 'N/A'), flight_data.get('price', 'N/A'), int(time.time()), flight_data.get('deep_link', 'N/A'),
                                            flight_data.get('cityCodeFrom', 'N/A'), flight_data.get('cityCodeTo', 'N/A'), flight_data.get('local_arrival', 'N/A'), flight_data.get('local_departure', 'N/A'), len(flight_data.get('route', [])) - 1, 1)

                                        db_data = await fetch_search_history(con, location['code'])
                        finally:
                            await con.close()
                        return jsonify(db_data)
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500

    return jsonify({'error': 'No location code found'}), 404

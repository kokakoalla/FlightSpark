from quart import Blueprint, request, jsonify
import aiohttp
from .config import Config
import asyncpg
import datetime
import time
from .database import get_database_connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Мгновенная установка дат
aika_nyt = datetime.datetime.now().date()
new_date_plus_10 = (aika_nyt + datetime.timedelta(days=10)).strftime("%Y-%m-%d")
new_date_plus_20 = (aika_nyt + datetime.timedelta(days=20)).strftime("%Y-%m-%d")

radius_bp = Blueprint('radius', __name__)

async def fetch_search_history(con, location_code):
    query = '''
    SELECT DISTINCT ON (to_city) from_city, to_city, url, price, to_id
    FROM search_history 
    WHERE from_id = $1 and stopovers = 0 and adults = 1
    ORDER BY to_city, id DESC, price DESC
    LIMIT 3; 
    '''
    search_history = await con.fetch(query, location_code)
    return [{'cityFrom': res['from_city'], 'cityTo': res['to_city'], 'price': res['price'], 'deep_link': res['url']}
            for res in search_history]

async def fetch_from_kiwi(session, url, params, headers):
    async with session.get(url, params=params, headers=headers) as response:
        if response.status != 200:
            raise Exception('Failed to fetch data from Kiwi API')
        return await response.json()

async def save_flight_data(con, data):
    for flight_data in data:
        await con.execute('''
            INSERT INTO search_history (from_city, to_city, price, date_time, url, from_id, to_id, local_arrival, local_departure, stopovers, adults)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        ''', flight_data.get('cityFrom', 'N/A'), flight_data.get('cityTo', 'N/A'), flight_data.get('price', 'N/A'),
        int(time.time()), flight_data.get('deep_link', 'N/A'), flight_data.get('cityCodeFrom', 'N/A'),
        flight_data.get('cityCodeTo', 'N/A'), flight_data.get('local_arrival', 'N/A'), flight_data.get('local_departure', 'N/A'),
        len(flight_data.get('route', [])) - 1, 1)

@radius_bp.route('/api/location/radius', methods=['GET'])
async def receive_location():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if not latitude or not longitude:
        return jsonify({'error': 'Missing latitude or longitude'}), 400

    try:
        async with aiohttp.ClientSession() as session:
            kiwi_data = await fetch_from_kiwi(
                session,
                f'{Config.TEQUILA_ENDPOINT_LOCATION}/locations/radius',
                params={'lat': latitude, 'lon': longitude, 'radius': 250, 'locale': 'en-US', 'location_types': 'airport', 'limit': 1},
                headers={'apikey': Config.API_KEY}
            )
            if 'locations' in kiwi_data:
                location = kiwi_data['locations'][0]
                if 'code' in location:
                    con = await get_database_connection()
                    try:
                        db_data = await fetch_search_history(con, location['code'])
                        if len(db_data) < 3:
                            date_from = new_date_plus_10
                            date_to = new_date_plus_20
                            logger.info(f"Fetching data from Kiwi API for location: {location['code']}")
                            kiwi_data = await fetch_from_kiwi(
                                session,
                                'https://api.tequila.kiwi.com/v2/search',
                                params={'fly_from': location['code'], 'date_from': date_from, 'date_to': date_to, 'adults': 1, 'limit': 3},
                                headers={'apikey': Config.API_KEY, 'Content-Type': 'application/json'}
                            )
                            data = kiwi_data['data']
                            if not data:
                                kiwi_data = await fetch_from_kiwi(
                                    session,
                                    'https://api.tequila.kiwi.com/v2/search',
                                    params={'fly_from': "HEL", 'date_from': date_from, 'date_to': date_to, 'adults': 1, 'limit': 3},
                                    headers={'apikey': Config.API_KEY, 'Content-Type': 'application/json'}
                                )
                                data = kiwi_data['data']
                            await save_flight_data(con, data)
                            db_data = await fetch_search_history(con, location['code'] if data else 'HEL')
                        logger.info(f"db_Data: {db_data}")
                        return jsonify(db_data)
                    finally:
                        await con.close()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return jsonify({'error': f'An error occurred: {e}'}), 500

    return jsonify({'error': 'No location code found'}), 404

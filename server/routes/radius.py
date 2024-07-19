from quart import Blueprint, request, jsonify
import aiohttp
from .config import Config
import datetime
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define constants for dates 10 and 20 days ahead
aika_nyt = datetime.datetime.now().date()
date_plus_10 = aika_nyt + datetime.timedelta(days=10)
new_date_plus_10 = date_plus_10.strftime("%Y-%m-%d")
date_plus_20 = aika_nyt + datetime.timedelta(days=20)
new_date_plus_20 = date_plus_20.strftime("%Y-%m-%d")

# Create a Blueprint for the radius API
radius_bp = Blueprint('radius', __name__)

async def fetch_search_history(con, location_code):
    """
    Fetch search history from the database for the given location code.
    """
    query = '''
    SELECT DISTINCT ON (to_city) from_city, to_city, url, price, to_id
    FROM search_history 
    WHERE from_id = $1 AND stopovers = 0 AND adults = 1
    ORDER BY to_city, id DESC, price DESC
    LIMIT 3;
    '''
    search_history = await con.fetch(query, location_code)
    return [{'cityFrom': res['from_city'], 'cityTo': res['to_city'], 'price': res['price'], 'deep_link': res['url']}
            for res in search_history]

async def fetch_from_kiwi(session, url, params, headers):
    """
    Fetch data from the Kiwi API.
    """
    async with session.get(url, params=params, headers=headers) as response:
        if response.status != 200:
            raise Exception('Failed to fetch data from Kiwi API')
        return await response.json()

async def save_flight_data(con, data):
    """
    Save flight data to the database.
    """
    for flight_data in data:
        await con.execute('''
            INSERT INTO search_history (from_city, to_city, price, date_time, url, from_id, to_id, local_arrival, local_departure, stopovers, adults)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        ''', flight_data.get('cityFrom', 'N/A'), flight_data.get('cityTo', 'N/A'), flight_data.get('price', 'N/A'),
        int(datetime.datetime.now().timestamp()), flight_data.get('deep_link', 'N/A'), flight_data.get('cityCodeFrom', 'N/A'),
        flight_data.get('cityCodeTo', 'N/A'), flight_data.get('local_arrival', 'N/A'), flight_data.get('local_departure', 'N/A'),
        len(flight_data.get('route', [])) - 1, 1)

@radius_bp.route('/api/location/radius', methods=['GET'])
async def receive_location():
    """
    Handle GET requests to fetch location data and flight information.
    """
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if not latitude or not longitude:
        return jsonify({'error': 'Missing latitude or longitude'}), 400

    try:
        async with aiohttp.ClientSession() as session:
            kiwi_data = await fetch_from_kiwi(
                session,
                f'{Config.TEQUILA_ENDPOINT_LOCATION}/locations/radius',
                params={'lat': latitude, 'lon': longitude, 'radius': 250},
                headers={'apikey': Config.API_KEY}
            )
            if 'locations' in kiwi_data:
                location = kiwi_data['locations'][0]
                if 'city' in location:
                    code_location = location['city']['code']
                    logger.info(f"Location code: {code_location}")
                    con = await get_database_connection()
                    try:
                        db_data = await fetch_search_history(con, code_location)
                        logger.info(f"db_data: {db_data}")
                        if len(db_data) > 2:
                            return jsonify(db_data)
                        else:
                            # Fetch new flight data
                            logger.info(f"Fetching data from Kiwi API for location: {location['code']}")
                            kiwi_data = await fetch_from_kiwi(
                                session,
                                f'{Config.TEQUILA_ENDPOINT_LOCATION}/v2/search',
                                params={
                                    'fly_from': location['city']['code'],
                                    'date_from': new_date_plus_10,
                                    'date_to': new_date_plus_20,
                                    'partner_market': 'us',
                                    'partner': 'picky',
                                    'curr': 'USD',
                                    'limit': 10
                                },
                                headers={'apikey': Config.API_KEY}
                            )
                            data = kiwi_data['data']
                            await save_flight_data(con, data)
                            db_data = await fetch_search_history(con, code_location)
                            logger.info(f"db_data: {db_data}")
                            return jsonify(db_data)
                    finally:
                        await con.close()
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        return jsonify({'error': f'An error occurred: {e}'}), 500

    return jsonify({'error': 'No location code found'}), 404

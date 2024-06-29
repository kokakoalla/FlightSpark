from quart import Blueprint, request, jsonify
import aiohttp
from .config import Config
import asyncpg
import datetime
import time

aika_nyt = datetime.datetime.now().date()
date_plus_10 = aika_nyt + datetime.timedelta(days=10)
new_date_plus_10 = date_plus_10.strftime("%Y-%m-%d")
date_plus_20 = aika_nyt + datetime.timedelta(days=20)
new_date_plus_20 = date_plus_20.strftime("%Y-%m-%d")

radius_bp = Blueprint('radius', __name__)

async def fetch_search_history(con, location_code):
    query = '''
    SELECT DISTINCT ON (to_city) from_city, to_city, price, url 
    FROM search_history 
    WHERE from_id = $1 
    ORDER BY to_city, price ASC
    LIMIT 3;
    '''
    search_history = await con.fetch(query, location_code)
    return [{'cityFrom': res['from_city'], 'cityTo': res['to_city'], 'price': res['price'], 'deep_link': res['url']}
            for res in search_history]

@radius_bp.route('/api/location/radius', methods=['GET'])
async def receive_location():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if not latitude or not longitude:
        return jsonify({'error': 'Missing latitude or longitude'}), 400

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{Config.TEQUILA_ENDPOINT_LOCATION}/locations/radius',
                params={
                    'lat': latitude,
                    'lon': longitude,
                    'radius': 50,
                    'locale': 'en-US',
                    'location_types': 'city',
                    'limit': 1
                },
                headers={'apikey': Config.API_KEY}
            ) as kiwi_response:
                if kiwi_response.status != 200:
                    return jsonify({'error': 'Failed to fetch data from Kiwi API'}), 500
                
                kiwi_data = await kiwi_response.json()
                if 'locations' in kiwi_data:
                    location = kiwi_data['locations'][0]
                    if 'code' in location:
                        con = await asyncpg.connect(Config.DATABASE_URL)
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
                                                INSERT INTO search_history (from_city, to_city, price, date_time, url, from_id, to_id, local_arrival, local_departure, stopovers)
                                                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                                            ''', flight_data.get('cityFrom', 'N/A'), flight_data.get('cityTo', 'N/A'), flight_data.get('price', 'N/A'), int(time.time()), flight_data.get('deep_link', 'N/A'),
                                            flight_data.get('cityCodeFrom', 'N/A'), flight_data.get('cityCodeTo', 'N/A'), flight_data.get('local_arrival', 'N/A'), flight_data.get('local_departure', 'N/A'), len(flight_data.get('route', [])) - 1)

                                        db_data = await fetch_search_history(con, location['code'])
                        finally:
                            await con.close()
                        return jsonify(db_data)
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500

    return jsonify({'error': 'No location code found'}), 404

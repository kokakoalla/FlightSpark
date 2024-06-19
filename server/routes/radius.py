from quart import Blueprint, request, jsonify
import aiohttp
from .config import Config
import asyncpg
import datetime

aika_nyt = datetime.datetime.now().date()
date_plus_10 = aika_nyt + datetime.timedelta(days=10)
new_date_plus_10 = date_plus_10.strftime("%Y-%m-%d")
date_plus_20 = aika_nyt + datetime.timedelta(days=20)
new_date_plus_20 = date_plus_20.strftime("%Y-%m-%d")

radius_bp = Blueprint('radius', __name__)

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
                        query = '''
                        SELECT from_city, to_city, price, url FROM search_history WHERE from_id = $1 ORDER BY date_time DESC LIMIT 3;
                        '''
                        search_history = await con.fetch(query, location['code'])
                        await con.close()

                        db_data = [{'cityFrom': res['from_city'], 'cityTo': res['to_city'], 'price': res['price'], 'deep_link': res['url']}
                                   for res in search_history]

                        if db_data:
                            return jsonify(db_data)

                        if len(search_history) < 4:
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
                                return jsonify({'kiwi_data': kiwi_data})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500

    return jsonify({'error': 'No location code found'}), 404

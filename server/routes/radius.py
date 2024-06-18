from flask import Blueprint, request, jsonify
import requests
from .config import Config
from .db import get_db_connection
import datetime

aika_nyt = datetime.datetime.now().date()
date_plus_10 = aika_nyt + datetime.timedelta(days=10)
new_date_plus_10 = date_plus_10.strftime("%Y-%m-%d")
date_plus_20 = aika_nyt + datetime.timedelta(days=20)
new_date_plus_20 = date_plus_20.strftime("%Y-%m-%d")

radius_bp = Blueprint('radius', __name__)

@radius_bp.route('/api/location/radius', methods=['GET'])
def receive_location():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if not latitude or not longitude:
        return jsonify({'error': 'Missing latitude or longitude'}), 400

    try:
        kiwi_response = requests.get(
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
        )
        kiwi_data = kiwi_response.json()
        if 'locations' in kiwi_data:
            location = kiwi_data['locations'][0]
            if 'code' in location:
                code = location['code']
                conn = get_db_connection()
                cur = conn.cursor()
                query = '''
                SELECT "from_city", "to_city", "price", "url" FROM 
                "search_history" WHERE "from_id" = ? ORDER BY "date_time" DESC LIMIT 3;
                '''
                cur.execute(query, (code,))
                search_history = cur.fetchall()
                conn.close()

                db_data = [{'cityFrom': res[0], 'cityTo': res[1], 'price': res[2], 'deep_link': res[3]}
                           for res in search_history]

                if db_data:
                    return jsonify(db_data)

                if len(search_history) < 4:
                    date_from = new_date_plus_10
                    date_to = new_date_plus_20
                    kiwi_response = requests.get(
                        'https://api.tequila.kiwi.com/v2/search',
                        params={
                            'fly_from': code,
                            'date_from': date_from,
                            'date_to': date_to,
                            'limit': 3
                        },
                        headers={'apikey': Config.API_KEY, 'Content-Type': 'application/json'}
                    )
                    if kiwi_response.status_code != 200:
                        return jsonify({'error': 'Failed to fetch data from Kiwi API'}), 500
                    kiwi_data = kiwi_response.json()
                    return jsonify({'kiwi_data': kiwi_data})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500

    return jsonify({'error': 'No location code found'}), 404

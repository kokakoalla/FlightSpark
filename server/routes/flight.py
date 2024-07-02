from quart import Blueprint, request, jsonify, current_app
import aiohttp
from .config import Config
import time

flight_bp = Blueprint('flight', __name__)

@flight_bp.route('/api/flights', methods=['GET'])
async def get_flights():
    async with current_app.db_pool.acquire() as con:
        from_city = request.args.get('from')
        to_city = request.args.get('to')
        date = request.args.get('date')
        dateBack = request.args.get('dateBack')
        adults = request.args.get('adults')


        if not from_city or not to_city or not date:
            return jsonify({'error': 'Please provide from_city, to_city, and date parameters'}), 400

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.tequila.kiwi.com/v2/search',
                                       params={
                                           'fly_from': from_city,
                                           'fly_to': to_city,
                                           'date_from': date,
                                           'date_to': date,
                                            'return_from': dateBack,
                                            'return_to': dateBack,
                                             'adults': adults,
                                           'max_stopovers': '2',
                                       },
                                       headers={'apikey': Config.API_KEY, 'Content-Type': 'application/json'}) as response:
                    if response.status != 200:
                        return jsonify({'error': 'Failed to fetch flights'}), response.status

                    data = await response.json()
                    results = data.get("data", [])

                    res = []
                    for flight_data in results:
                        formatted_data = {
                            'from': flight_data.get('cityFrom', 'N/A'),
                            'to': flight_data.get('cityTo', 'N/A'),
                            'arrival': flight_data.get('local_arrival', 'N/A'),
                            'departure': flight_data.get('local_departure', 'N/A'),
                            'price': flight_data.get('price', 'N/A'),
                            'url': flight_data.get('deep_link', 'N/A'),
                            'from_id': flight_data.get('cityCodeFrom', 'N/A'),
                            'to_id': flight_data.get('cityCodeTo', 'N/A'),
                            'stopovers': len(flight_data.get('route', [])) - 1
                        }
                        res.append(formatted_data)

                        # Insert into database
                        await con.execute('''
                            INSERT INTO search_history (from_city, to_city, price, date_time, url, from_id, to_id, local_arrival, local_departure, stopovers)
                            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                        ''', formatted_data['from'], formatted_data['to'], formatted_data['price'], int(time.time()), formatted_data['url'],
                        formatted_data['from_id'], formatted_data['to_id'], formatted_data['arrival'], formatted_data['departure'], formatted_data['stopovers'])

                    return jsonify(data), 200

        except aiohttp.ClientError as e:
            return jsonify({'error': f'Aiohttp Client Error: {str(e)}'}), 500

        except Exception as e:
            return jsonify({'error': f'Server Error: {str(e)}'}), 500

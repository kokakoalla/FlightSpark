from quart import Blueprint, request, jsonify
import aiohttp
from .config import Config
import time
from .database import get_database_connection

# Create a Blueprint for flight-related routes
flight_bp = Blueprint('flight', __name__)

@flight_bp.route('/api/flights', methods=['GET'])
async def get_flights():
    """
    Fetch flight data based on parameters and save to the database.
    """
    from_city = request.args.get('from')
    to_city = request.args.get('to')
    date = request.args.get('date')
    date_back = request.args.get('dateBack')
    adults = request.args.get('adults')

    if not from_city or not to_city or not date or not adults:
        return jsonify({'error': 'Please provide from_city, to_city, date, and adults parameters'}), 400

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'https://api.tequila.kiwi.com/v2/search',
                params={
                    'fly_from': from_city,
                    'fly_to': to_city,
                    'date_from': date,
                    'date_to': date,
                    'return_from': date_back,
                    'return_to': date_back,
                    'adults': adults,
                    'max_stopovers': '2',
                    'limit': '30',
                },
                headers={'apikey': Config.API_KEY, 'Content-Type': 'application/json'}
            ) as response:
                if response.status != 200:
                    return jsonify({'error': 'Failed to fetch flights'}), response.status

                data = await response.json()
                results = data.get("data", [])

                res = []
                for flight_data in results:
                    formatted_data = {
                        'adults': adults,
                        'price': flight_data.get('price', 'N/A'),
                        'url': flight_data.get('deep_link', 'N/A'),
                        'from': {
                            'city': flight_data.get('cityFrom', 'N/A'),
                            'city_code': flight_data.get('cityCodeFrom', 'N/A'),
                            'country': flight_data.get('countryFrom', {}).get('name', 'N/A'),
                        },
                        'to': {
                            'city': flight_data.get('cityTo', 'N/A'),
                            'city_code': flight_data.get('cityCodeTo', 'N/A'),
                            'country': flight_data.get('countryTo', {}).get('name', 'N/A'),
                        },
                        'outbound_routes': [],
                        'return_routes': []
                    }

                    for route in flight_data.get('route', []):
                        route_data = {
                            'airline': route.get('airline', 'N/A'),
                            'from': route.get('cityFrom', 'N/A'),
                            'to': route.get('cityTo', 'N/A'),
                            'departure': route.get('local_departure', 'N/A'),
                            'arrival': route.get('local_arrival', 'N/A')
                        }
                        if route.get('return') == 0:
                            formatted_data['outbound_routes'].append(route_data)
                        else:
                            formatted_data['return_routes'].append(route_data)

                    res.append(formatted_data)

                    # Save flight data to the database
                    con = await get_database_connection()
                    try:
                        for route in flight_data.get('route', []):
                            await con.execute('''
                                INSERT INTO search_history (from_city, to_city, price, date_time, url, from_id, to_id, local_arrival, local_departure, stopovers, adults)
                                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                            ''',
                            formatted_data['from']['city'],
                            formatted_data['to']['city'],
                            formatted_data['price'],
                            int(time.time()),
                            formatted_data['url'],
                            route['cityCodeFrom'],
                            route['cityCodeTo'],
                            route['local_arrival'],
                            route['local_departure'],
                            len(flight_data.get('route', [])) - 1,
                            int(adults))
                    finally:
                        await con.close()

                return jsonify(res), 200

    except aiohttp.ClientError as e:
        return jsonify({'error': f'Aiohttp Client Error: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': f'Server Error: {str(e)}'}), 500

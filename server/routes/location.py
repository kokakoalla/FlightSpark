from quart import Blueprint, request, jsonify
import aiohttp
from .config import Config

location_bp = Blueprint('location', __name__)

@location_bp.route('/api/locations', methods=['GET'])
async def get_locations():
    term = request.args.get('term')
    if not term:
        return jsonify({'error': 'Missing term parameter'}), 400

    async with aiohttp.ClientSession() as session:
        async with session.get(f'{Config.TEQUILA_ENDPOINT_LOCATION}/locations/query', 
                               params={'term': term, 'location_types': 'city', 'limit': 5, 'active_only': 'True'},
                               headers={'apikey': Config.API_KEY}) as response:
            if response.status != 200:
                return jsonify({'error': 'Failed to fetch locations'}), response.status

            data = await response.json()
            return jsonify(data)

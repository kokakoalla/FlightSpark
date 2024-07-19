from quart import Blueprint, request, jsonify
import aiohttp
from .config import Config
import logging

# Create a Blueprint for location-related routes
location_bp = Blueprint('location', __name__)

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@location_bp.route('/api/locations', methods=['GET'])
async def get_locations():
    """
    Fetch location data based on the search term from the Tequila API.
    """
    term = request.args.get('term')
    
    if not term:
        return jsonify({'error': 'Missing term parameter'}), 400

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{Config.TEQUILA_ENDPOINT_LOCATION}/locations/query',
                params={'term': term, 'location_types': 'city', 'limit': 5, 'active_only': 'True'},
                headers={'apikey': Config.API_KEY}
            ) as response:
                if response.status != 200:
                    logger.error(f'Failed to fetch locations, status code: {response.status}')
                    return jsonify({'error': 'Failed to fetch locations'}), response.status

                data = await response.json()
                logger.info(f'Successfully fetched locations for term: {term}')
                return jsonify(data)
                
    except aiohttp.ClientError as e:
        logger.error(f'Aiohttp Client Error: {str(e)}')
        return jsonify({'error': f'Aiohttp Client Error: {str(e)}'}), 500

    except Exception as e:
        logger.error(f'Server Error: {str(e)}')
        return jsonify({'error': f'Server Error: {str(e)}'}), 500

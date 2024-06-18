from flask import Blueprint, request, jsonify
import requests
from .config import Config

location_bp = Blueprint('location', __name__)

@location_bp.route('/api/locations', methods=['GET'])
def get_locations():
    term = request.args.get('term')
    if not term:
        return jsonify({'error': 'Missing term parameter'}), 400

    response = requests.get(f'{Config.TEQUILA_ENDPOINT_LOCATION}/locations/query', 
                            params={'term': term, 'location_types': 'city', 'limit': 5, 'active_only': True},
                            headers={'apikey': Config.API_KEY})
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch locations'}), response.status_code

    return jsonify(response.json())

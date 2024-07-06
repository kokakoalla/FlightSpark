from quart import Blueprint, request, jsonify #Tuodaan tarvittavat moduulit
import aiohttp #Tuodaan aiohttp-moduuli
from .config import Config #Tuodaan Config-luokka config-moduulista

location_bp = Blueprint('location', __name__) #Luodaan Blueprint location reititys

@location_bp.route('/api/locations', methods=['GET']) # Määritellään reitti /api/locations, joka ottaa vastaan vain GET-pyyntöjä
async def get_locations():                           #Määritellään asynkroninen funktio get_locations
    term = request.args.get('term')                  # Haetaan term-parametri pyynnöstä
    if not term:                                  #Jos term puuttuu
        return jsonify({'error': 'Missing term parameter'}), 400    # Palautetaan virheilmoitus 

    async with aiohttp.ClientSession() as session:                                     #Luodaan asynkroninen HTTP-istunto
        async with session.get(f'{Config.TEQUILA_ENDPOINT_LOCATION}/locations/query',  #Tehdään GET pyyntö Tequila API:lle
                               params={'term': term, 'location_types': 'city', 'limit': 5, 'active_only': 'True'}, #Lähetetään parametrit
                               headers={'apikey': Config.API_KEY}) as response:    # Lähetetään API-avain
            if response.status != 200:   #Jos vastauskoodi ei ole 200
                return jsonify({'error': 'Failed to fetch locations'}), response.status # Palautetaan virheilmoitus ja statuskoodi

            data = await response.json() # Odotetaan ja muutetaan vastaus JSON-muotoon
            return jsonify(data) # Palautetaan JSON-muotoinen vastaus

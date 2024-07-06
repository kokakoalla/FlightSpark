from quart import Blueprint, request, jsonify, current_app #Tuodaan tarvittavat moduulit
import aiohttp #Tuodaan aiohttp-moduuli
from .config import Config #Tuodaan Config-luokka config-moduulista
import time #Tuodaan time-moduuli
from .database import get_database_connection #Tuodaan get_database_connection-funktio database-moduulista

flight_bp = Blueprint('flight', __name__) #Luodaaan Blueprint flight reititys

@flight_bp.route('/api/flights', methods=['GET']) # Määritellään reitti /api/flights, joka ottaa vastaan vain GET-pyyntöjä
async def get_flights():                            #Määritellään asynkroninen funktio get_flights
        from_city = request.args.get('from')          # Haetaan from-parametri pyynnöstä
        to_city = request.args.get('to')               # Haetaan to-parametri pyynnöstä
        date = request.args.get('date')                    # Haetaan date-parametri pyynnöstä
        dateBack = request.args.get('dateBack')                 # Haetaan dateBack-parametri pyynnöstä
        adults = request.args.get('adults')                         # Haetaan adults-parametri pyynnöstä

        if not from_city or not date or not adults: #Jos from_city, to_city, date tai dateBack puuttuu
            return jsonify({'error': 'Please provide from_city, to_city, and date parameters'}), 400 # Palautetaan virheilmoitus ja statuskoodi 400

        try:                                                     #Yritetään suorittaa seuraava koodi
            async with aiohttp.ClientSession() as session:             #Luodaan asynkroninen HTTP-istunto
                async with session.get('https://api.tequila.kiwi.com/v2/search', #Haetaan lennot Tequila API:sta
                                       params={
                                           'fly_from': from_city,
                                           'fly_to': to_city,
                                           'date_from': date,
                                           'date_to': date,
                                           'return_from': dateBack,
                                           'return_to': dateBack,
                                           'adults': adults,
                                           'max_stopovers': '2',
                                           'limit': '30',
                                       },
                                       headers={'apikey': Config.API_KEY, 'Content-Type': 'application/json'}) as response: # Lisätään API-avain ja Content-Type-otsikko
                    if response.status != 200: # Jos vastauskoodi ei ole 200
                        return jsonify({'error': 'Failed to fetch flights'}), response.status # Palautetaan virheilmoitus 
                    
                    data = await response.json() # Haetaan vastauksen JSON-data
                    results = data.get("data", []) # Haetaan datasta data-avaimen arvo, jos sitä ei ole, käytetään tyhjää listaa

                    res = [] #Luodaan tyhjä lista res
                    for flight_data in results: #Käydään läpi lennot
                        formatted_data = {          #Määritellään lentojendata, joka sisältää lennon tiedot jotka tulee front-endille näyttää
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
                            'outbound_routes': [],   # Lenonot yhteen suuntaan
                            'return_routes': []        # Lenonot paluusuuntaan
                        }

                        for route in flight_data.get('route', []): #Käydään läpi route(meno- ja paluutiedot)
                            route_data = {       #Määritellään route tiedot
                                'airline': route.get('airline', 'N/A'),
                                'from': route.get('cityFrom', 'N/A'),
                                'to': route.get('cityTo', 'N/A'),
                                'departure': route.get('local_departure', 'N/A'),
                                'arrival': route.get('local_arrival', 'N/A')
                            }
                            if route.get('return') == 0: # Menosuuunta on 0, paluusuunta on 1
                                formatted_data['outbound_routes'].append(route_data) #Lisätään lähtöreitit 
                            else:
                                formatted_data['return_routes'].append(route_data) #Lisätään paluureitit
                        res.append(formatted_data) # Lisätään formatoitu lentotiedot res-listaan

                        
                        for route in flight_data.get('route', []): #Käydään läpi lennot tietokannaan tallennusta varten
                            con = await get_database_connection() #Haetaan tietokannan yhteys
                            try:
                                await con.execute('''
                                    INSERT INTO search_history (from_city, to_city, price, date_time, url, from_id, to_id, local_arrival, local_departure, stopovers,adults)
                                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11 )
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
                    return jsonify(res), 200 # Palautetaan lentotiedot

        except aiohttp.ClientError as e:  #Jos tulee aiohttp-virhe
            return jsonify({'error': f'Aiohttp Client Error: {str(e)}'}), 500

        except Exception as e: #Jos tulee joku muu virhe
            return jsonify({'error': f'Server Error: {str(e)}'}), 500
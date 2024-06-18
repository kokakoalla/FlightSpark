from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import sqlite3
import time
from datetime import datetime, timedelta
import aiohttp
from aiohttp import ClientSession
import json
import os
from dotenv import load_dotenv

load_dotenv()

aika_nyt = datetime.now().date()

date_plus_10 = aika_nyt + timedelta(days=10)
new_date_plus_10 = date_plus_10.strftime("%Y-%m-%d")

date_plus_20 = aika_nyt + timedelta(days=10)
new_date_plus_20 = date_plus_20.strftime("%Y-%m-%d")


app = Flask(__name__)
CORS(app)


con = sqlite3.connect("my_app.db", check_same_thread=False)
cur = con.cursor()

TEQUILA_ENDPOINT_LOCATION = 'https://tequila-api.kiwi.com'
API_KEY = os.getenv('API_KEY')

@app.route('/api/location/radius', methods=['GET'])
def receive_location():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if not latitude or not longitude:
        return jsonify({'error': 'puuttu latitude or longitude'}), 400

    print(f'Received coordinates: Latitude = {latitude}, Longitude = {longitude}')

    try:                                                 
        kiwi_response = requests.get(
            f'{TEQUILA_ENDPOINT_LOCATION}/locations/radius',
            params={
                'lat': latitude,
                'lon': longitude,
                'radius': 50,  
                'locale': 'en-US',
                'location_types': 'city',
                'limit': 1 
            },
            headers={
                'apikey': API_KEY
            }
        )
        kiwi_data = kiwi_response.json()

        if 'locations' in kiwi_data:
            location = kiwi_data['locations'][0]
            if 'code' in location:
                code = location['code']
                print(f"The code for the location is: {code}")

                con = sqlite3.connect("my_app.db", check_same_thread=False)
                cur = con.cursor()

                query = '''  
                SELECT "from_city", "to_city", "price", "local_arrival", "local_departure" FROM 
                "search_history" WHERE "from_id" = ? ORDER BY "date_time" DESC LIMIT 3;
                '''

                cur.execute(query, (code,))
                search_history = cur.fetchall()
                con.close()

                db_data = []
                for result in search_history:
                    entry = {
                        'cityFrom': result[0],
                        'cityTo': result[1],
                        'price': result[2],
                        'local_arrival': result[3],
     #                   'local_arrival': result[4],
      #                  'local_departure': result[5]
                    }
                    db_data.append(entry)
   #            
                if db_data:
                    return jsonify(db_data)
                
                if len(search_history) < 4:
                    date_from = new_date_plus_10
                    date_to = new_date_plus_20

                    kiwi_response = requests.get('https://api.tequila.kiwi.com/v2/search',
                                                 params={
                                                     'fly_from': code,
                                                     'date_from': date_from,
                                                     'date_to': date_to,
                                                     'limit': 3
                                                 },
                                                 headers={'apikey': API_KEY, 'Content-Type': 'application/json'})

                    if kiwi_response.status_code != 200:
                        return jsonify({'error': 'Failed to fetch data from Kiwi API'}), 500

                    kiwi_data = kiwi_response.json()
  #                  print(kiwi_data)
                    return jsonify({
                        'kiwi_data': kiwi_data
                    })

                    
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred'}), 500
    
    return jsonify({'error': 'No location code found'}), 404


@app.route('/api/locations', methods=['GET'])
def get_locations():
    term = request.args.get('term')
    if not term:
        return jsonify({'error': 'term paramitteri puuttu'}), 400

    response = requests.get(f'{TEQUILA_ENDPOINT_LOCATION}/locations/query', 
                            params={'term': term, 'location_types': 'city', 'limit': 5, 'active_only': True},
                            headers={'apikey': API_KEY})
    if response.status_code != 200:
        return jsonify({'error': 'virhe1'}), response.status_code

    return jsonify(response.json())



@app.route('/api/flights', methods=['GET'])
def get_flights():
    con = sqlite3.connect("my_app.db", check_same_thread=False)
    cur = con.cursor()


    from_city = request.args.get('from')
    to_city = request.args.get('to')
    date = request.args.get('date')
 #   if not from_city or not to_city or not date:
  #      return jsonify({'error': 'virhe123'}), 400

    response = requests.get('https://api.tequila.kiwi.com/v2/search',
                            params={
                                'fly_from': from_city,
                                'fly_to': to_city,
                                'date_from': date,
                                'date_to': date,
                                'max_stopovers': '2',
                            },
                            headers={'apikey': API_KEY, 'Content-Type': 'application/json'})

    if response.status_code != 200:
        return jsonify({'error': 'Ei onnistunut löyttää lippuja'}), response.status_code

    results = response.json().get("data")
    result = response.json()
    res = []




    for i, data in enumerate(results):
        if data.get('airlines'):
            formatted_data = {
                'from': data.get('cityFrom', 'N/A'),
                'to': data.get('cityTo', 'N/A'),
                'arrival': data.get('local_arrival', 'N/A'),
                'departure': data.get('local_departure', 'N/A'),
                'price': data.get('price', 'N/A'),
                'url': data.get('deep_link', 'N/A'),
                'from_id': data.get('cityCodeFrom', 'N/A'),
                'to_id': data.get('cityCodeTo', 'N/A'),
                'stopovers': len(data.get('route', [])) - 1
            }
            res.append(formatted_data)

            insert_query = '''
            INSERT INTO "search_history" ("from_city", "to_city", "price",
             "date_time", "url", "from_id", "to_id", "local_arrival", "local_departure", "stopovers")
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            values_to_insert = (
                formatted_data['from'],
                formatted_data['to'],
                formatted_data['price'],
                int(time.time()),  # current timestamp
                formatted_data['url'],
                formatted_data['from_id'],
                formatted_data['to_id'],
                formatted_data['arrival'],
                formatted_data['departure'],
                formatted_data['stopovers']
            )
            cur.execute(insert_query, values_to_insert)

    con.commit()
    con.close()

    return jsonify(response.json())
#    return jsonify({'flights': flights})


    


@app.route('/test')
def test():
    return jsonify({'ok': 'server works'}), 400


if __name__ == '__main__':
    app.run(debug=True)
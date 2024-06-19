from flask import Blueprint, request, jsonify
import requests
from .config import Config
from .db import get_db_connection
import time
import sqlite3
import psycopg2

flight_bp = Blueprint('flight', __name__)

@flight_bp.route('/api/flights', methods=['GET'])

def get_flights():
    con = get_db_connection()
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
                            headers={'apikey': Config.API_KEY, 'Content-Type': 'application/json'})

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

        cur.execute('''
            INSERT INTO search_history (from_city, to_city, price, date_time, url, from_id, to_id, local_arrival, local_departure, stopovers)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            formatted_data['from'], formatted_data['to'], formatted_data['price'], int(time.time()), formatted_data['url'],
            formatted_data['from_id'], formatted_data['to_id'], formatted_data['arrival'], formatted_data['departure'], formatted_data['stopovers']
        ))

    conn.commit()
    cur.close()
    conn.close()


    return jsonify(response.json())





from quart import Quart, jsonify, request, send_from_directory  # tuodaan tarvittavat moduulit
from routes import create_app # tuodaan create_app-funktio routes-moduulista
import asyncio # tuodaan asyncio-moduuli
import logging
from flask_vite import Vite


logging.basicConfig(level=logging.INFO) # Määritetään perusasetukset loggingille, INFO-tasolla
logger = logging.getLogger(__name__) #Luodaan logger-olio

app = create_app() #luodan sovelluksen olio(istanssi) käyttäen create_app-funktiota 123123
print(app) #tulostetaan sovelluksen olio(istanssi)

@app.before_request
async def log_request_info():
    logging.info(f"Request: {request.method} {request.url}")

@app.after_request
async def log_response_info(response):
    logging.info(f"Response: {response.status}")
    return response

@app.route('/')
async def serve_index():
    return await send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
async def serve_static(path):
    return await send_from_directory(app.static_folder, path)

@app.after_request
async def cors_after_request(response): #määritellään asynkroninen funktio, joka lisää CORS-otsikot jokaiseen vastaukseen
    response.headers['Access-Control-Allow-Origin'] = '*' #sallitaan kaikki alkuperät
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS' #Sallitaan kaikki HTTP-metodit
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization' #Sallitaan kaikki otsikot
    return response #Paluttetaan muokattu vastaus

if __name__ == '__main__': # Jos tiedostoa ajetaan suoraan, käynnistetään sovellus
    from quart import Quart, jsonify, request # tuodaan tarvittavat moduulit
from routes import create_app # tuodaan create_app-funktio routes-moduulista
import asyncio # tuodaan asyncio-moduuli

app = create_app() #luodan sovelluksen olio(istanssi) käyttäen create_app-funktiota 123123
print(app) #tulostetaan sovelluksen olio(istanssi)

@app.route('/')
async def serve_index():
    return await send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
async def serve_static(path):
    return await send_from_directory(app.static_folder, path)
    
@app.after_request
async def cors_after_request(response): #määritellään asynkroninen funktio, joka lisää CORS-otsikot jokaiseen vastaukseen
    response.headers['Access-Control-Allow-Origin'] = '*' #sallitaan kaikki alkuperät
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS' #Sallitaan kaikki HTTP-metodit
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization' #Sallitaan kaikki otsikot
    return response #Paluttetaan muokattu vastaus

if __name__ == '__main__': # Jos tiedostoa ajetaan suoraan, käynnistetään sovellus
    app.run(port=8000, debug=False)
    # asyncio.run(app.run_task()) # Käynnistetään sovellus asynkronisesti



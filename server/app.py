from quart import Quart, jsonify, request # tuodaan tarvittavat moduulit
from routes import create_app # tuodaan create_app-funktio routes-moduulista
import asyncio # tuodaan asyncio-moduuli

app = create_app() #luodan sovelluksen olio(istanssi) käyttäen create_app-funktiota 123123
print(app) #tulostetaan sovelluksen olio(istanssi)

@app.after_request
async def cors_after_request(response): #määritellään asynkroninen funktio, joka lisää CORS-otsikot jokaiseen vastaukseen
    response.headers['Access-Control-Allow-Origin'] = '*' #sallitaan kaikki alkuperät
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS' #Sallitaan kaikki HTTP-metodit
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization' #Sallitaan kaikki otsikot
    return response #Paluttetaan muokattu vastaus

if __name__ == '__main__': # Jos tiedostoa ajetaan suoraan, käynnistetään sovellus
    asyncio.run(app.run_task()) # Käynnistetään sovellus asynkronisesti


# Path: server/routes/__init__.py
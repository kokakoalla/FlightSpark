from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
from quart import Quart, send_from_directory, jsonify
from flask_cors import CORS
from routes import create_app

app = create_app()

CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
async def serve_index():
    return await send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
async def serve_static(path):
    return await send_from_directory(app.static_folder, path)


@app.route('/test')
async def test():
    return jsonify({'message': 'hello:hello'})


if __name__ == "__main__":
    config = Config()
    config.bind = ["0.0.0.0:8000"]
    asyncio.run(serve(app, config))


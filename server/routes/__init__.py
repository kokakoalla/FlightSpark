from quart import Quart
from .flight import flight_bp
from .location import location_bp
from .radius import radius_bp
from .config import Config
import asyncpg

def create_app():
    app = Quart(__name__)
    
    app.register_blueprint(location_bp)
    app.register_blueprint(flight_bp)
    app.register_blueprint(radius_bp)

    @app.before_serving
    async def create_db_pool():
        app.db_pool = await asyncpg.create_pool(Config.DATABASE_URL)
    
    @app.after_serving
    async def close_db_pool():
        await app.db_pool.close()

    return app

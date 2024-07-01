from quart import Quart
from .flight import flight_bp
from .location import location_bp
from .radius import radius_bp
from .config import Config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncpg
import asyncio

async def cleanup_old_records():
    async with app.db_pool.acquire() as con:
        await con.execute('''
            DELETE FROM search_history
            WHERE date_time < EXTRACT(EPOCH FROM (NOW() - INTERVAL '10 days'))
        ''')

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(cleanup_old_records, IntervalTrigger(days=1))
    scheduler.start()

def create_app():
    app = Quart(__name__)
    
    app.register_blueprint(location_bp)
    app.register_blueprint(flight_bp)
    app.register_blueprint(radius_bp)

    @app.before_serving
    async def create_db_pool():
        app.db_pool = await asyncpg.create_pool(Config.DATABASE_URL)
        start_scheduler()

    @app.after_serving
    async def close_db_pool():
        await app.db_pool.close()

    return app

if __name__ == "__main__":
    app = create_app()
    asyncio.get_event_loop().run_until_complete(app.run_task())

import logging
from quart import Quart
from .flight import flight_bp
from .location import location_bp
from .radius import radius_bp
from .config import Config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import datetime

# logging.basicConfig(level=logging.INFO)  # Set logging level to INFO
# logger = logging.getLogger(__name__)  # Create logger instance

async def cleanup_old_records(app):
    """Remove old records from the database."""
    async with app.db_pool.acquire() as con:
        current_time = datetime.datetime.now().timestamp()
        time_10_days_ago = (
            datetime.datetime.now() - datetime.timedelta(days=10)
        ).timestamp()
        
        logger.info(f"Current Unix time: {current_time}")
        logger.info(f"Unix time 10 days ago: {time_10_days_ago}")

        old_records = await con.fetch('''
            SELECT * FROM search_history
            WHERE date_time < $1
        ''', time_10_days_ago)
        
        # if old_records:
        #     logger.info(f"Old records to be deleted: {old_records}")
        # else:
        #     logger.info("No old records found.")

        await con.execute('''
            DELETE FROM search_history
            WHERE date_time < $1
        ''', time_10_days_ago)
        # logger.info("Old records deleted successfully.")

def start_scheduler(app):
    """Start the scheduler to clean up old records daily."""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        cleanup_old_records, IntervalTrigger(days=1), args=[app]
    )
    scheduler.start()

def create_app():
    """Create and configure the Quart application."""
    app = Quart(__name__)

    app.register_blueprint(location_bp)
    app.register_blueprint(flight_bp)
    app.register_blueprint(radius_bp)

    @app.before_serving
    async def create_db_pool():
        """Create a database connection pool before serving."""
        app.db_pool = await asyncpg.create_pool(Config.DATABASE_URL)

    @app.after_serving
    async def close_db_pool():
        """Close the database connection pool after serving."""
        await app.db_pool.close()

    return app

import asyncio
from app import app  # Import the Quart app from app.py

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level="info")

from flask import Flask
from flask_cors import CORS
from routes import create_app

app = create_app()
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)

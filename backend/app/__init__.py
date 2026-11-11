
from flask import Flask
from flask_cors import CORS

from backend.app.api.routes import api


def create_app():
    app = Flask(__name__)

    CORS(app, origins=["http://localhost:5173"])

    app.register_blueprint(api)

    @app.get("/")
    def home():
        return {
            "message": "Transaction Risk Analysis Application",
            "api": "/api",
            "health": "/api/health",
        }

    return app

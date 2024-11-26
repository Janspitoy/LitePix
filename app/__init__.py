from flask import Flask
from app.routes import bp as routes_bp


def create_app():
    app = Flask(__name__)

    # Регистрация маршрутов
    app.register_blueprint(routes_bp)

    return app
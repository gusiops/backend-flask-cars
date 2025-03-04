from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from config import Config
from routes import cars_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)  # Разрешить запросы с любого источника

    # Настройка логирования
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Регистрация Blueprint
    app.register_blueprint(cars_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT']
    )
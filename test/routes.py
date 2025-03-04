from flask import Blueprint, request, jsonify
import logging
from data import cars_data

cars_bp = Blueprint('cars', __name__)

@cars_bp.route('/cars-data', methods=['GET'])
def get_cars():
    filter_name = request.args.get('filter', '')
    
    # Фильтрация по названию
    if filter_name in ['', 'Все марки']:
        return jsonify(cars_data)
    
    filtered = [
        car for car in cars_data 
        if filter_name.lower() in car['title'].lower()
    ]
    return jsonify(filtered)

@cars_bp.route('/cars-order', methods=['POST', 'OPTIONS'])
def create_order():
    if request.method == 'OPTIONS':
        # Обработка предварительных CORS-запросов
        return jsonify({"status": "ok"}), 200
    
    data = request.json
    
    # Валидация данных
    if not all([
        data.get('car'),
        data.get('name'),
        len(data.get('phone', '')) >= 10
    ]):
        return jsonify({
            "message": "Ошибка валидации",
            "error": True
        }), 400
    
    # Здесь можно добавить запись в БД
    logging.info(f"Новый заказ: {data}")
    
    return jsonify({
        "message": "Заказ успешно создан! Мы свяжемся с вами в ближайшее время.",
        "error": False
    })
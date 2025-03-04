from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)

# Настройка CORS
CORS(
    app,
    origins=["https://filatov.website", "http://filatov.website:5000", "http://filatov.website"],
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True,
    max_age=600
)

# Логирование
app.logger.setLevel(logging.DEBUG)

# data

cars_data = [
  {
    "image": "https://testologia.ru/cars-images/1.png",
    "title": "BMW M4 Competition",
    "text": "Идеальный баланс скорости и стиля. BMW M4 Competition — 510 л.с. и драйв, созданный для покорения трасс и городских улиц.",
    "prices": [
      1450,
      1300,
      1100
    ]
  },
  {
    "image": "https://testologia.ru/cars-images/2.png",
    "title": "BMW M5",
    "text": "Бизнес-класс с душой гонщика. BMW M5: 600 л.с., интеллектуальный полный привод и комфорт для самых требовательных.",
    "prices": [
      1600,
      1450,
      1250
    ]
  },
  {
    "image": "https://testologia.ru/cars-images/3.png",
    "title": "Lamborghini Huracan Spyder Green",
    "text": "Воплощение скорости и страсти. Зеленый Lamborghini Huracan Spyder — мощь 640 л.с. и открытый верх для ярких приключений.",
    "prices": [
      3200,
      2900,
      2600
    ]
  },
  {
    "image": "https://testologia.ru/cars-images/4.png",
    "title": "Ferrari F8 Spider",
    "text": "Мечта на колесах. Ferrari F8 Spider: 720 л.с., аэродинамика F1 и открытая кабина для тех, кто живет на полной скорости.",
    "prices": [
      3500,
      3200,
      2900
    ]
  },
  {
    "image": "https://testologia.ru/cars-images/5.png",
    "title": "Porsche 911 Targa 4S Yellow",
    "text": "Элегантная мощь в ярком цвете. Porsche 911 Targa 4S: полный привод, 450 л.с. и уникальный стиль Targa.",
    "prices": [
      1800,
      1650,
      1450
    ]
  },
  {
    "image": "https://testologia.ru/cars-images/6.png",
    "title": "Mercedes SL 55 AMG",
    "text": "Классика спортивного шика. Mercedes SL 55 AMG: роскошь, кабриолет и мощь 469 л.с. для незабываемых поездок.",
    "prices": [
      1700,
      1550,
      1350
    ]
  },
  {
    "image": "https://testologia.ru/cars-images/7.png",
    "title": "BMW Z4",
    "text": "Компактный кабриолет для стильных путешествий. BMW Z4: идеальный союз маневренности, мощности и элегантного дизайна.",
    "prices": [
      1200,
      1100,
      950
    ]
  },
  {
    "image": "https://testologia.ru/cars-images/8.png",
    "title": "Mercedes C180 Convertible",
    "text": "Идеальный выбор для солнечного дня. Mercedes C180 Convertible: кабриолет для легкого и комфортного вождения.",
    "prices": [
      1000,
      900,
      801
    ]
  },
  {
    "image": "https://testologia.ru/cars-images/9.png",
    "title": "Chevrolet Corvette Orange",
    "text": "Яркий, мощный, незабываемый. Chevrolet Corvette в оранжевом цвете: 495 л.с. и стиль, который говорит сам за себя.",
    "prices": [
      1400,
      1250,
      1100
    ]
  },
  {
    "image": "https://testologia.ru/cars-images/10.png",
    "title": "Audi R8 Blue",
    "text": "Суперкар, созданный для влюбленных в скорость. Audi R8 Blue: полный привод, 570 л.с. и потрясающий дизайн.",
    "prices": [
      2000,
      1850,
      1600
    ]
  },
  {
    "image": "https://testologia.ru/cars-images/11.png",
    "title": "Chevrolet Corvette White",
    "text": "Классическая мощь в изысканном цвете. Chevrolet Corvette White: мощность, динамика и стиль для настоящих ценителей.",
    "prices": [
      1350,
      1200,
      1000
    ]
  },
  {
    "image": "https://testologia.ru/cars-images/12.png",
    "title": "Ford Mustang Convertible Black",
    "text": "Легенда в открытом формате. Ford Mustang Convertible Black: 450 л.с., культовый стиль и свобода под открытым небом.",
    "prices": [
      1250,
      1150,
      1000
    ]
  }
]


# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vlad:1g2h5749@filatov.website:5432/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Исправленная опечатка

db = SQLAlchemy(app)

# Модель Order

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Имя клиента
    car = db.Column(db.String(100), nullable=False)  # Название автомобиля
    phone = db.Column(db.String(20), nullable=False)  # Номер телефона (строка)

# Создание таблицы
with app.app_context():
    db.create_all()

@app.route('/cars-data', methods=['GET'])
def get_cars():
    filter_name = request.args.get('filter', '')
    if filter_name in ['', 'Все марки']:
        return jsonify(cars_data)
    filtered = [car for car in cars_data if filter_name.lower() in car['title'].lower()]
    return jsonify(filtered)

@app.route('/cars-order', methods=['POST'])
def create_order_car():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400

        name = data.get('name')
        car = data.get('car')
        phone = data.get('phone')

        if not name or not car or not phone:
            return jsonify({"error": "Missing required fields"}), 400

        new_order = Order(name=name, car=car, phone=phone)
        db.session.add(new_order)
        db.session.commit()

        return jsonify({
            "message": "Заказ успешно создан! Мы свяжемся с вами в ближайшее время.",
            "error": False
        })

    except Exception as e:
        app.logger.error(f"Ошибка при создании заказа: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

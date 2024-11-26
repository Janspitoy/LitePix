from flask import Blueprint, jsonify, request
from libs.database.database import SessionLocal, get_user_by_id, init_db
from libs.database.models import User

# Создаем объект Blueprint для маршрутов
bp = Blueprint("routes", __name__)


# Функция для управления сессией базы данных
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Маршрут для инициализации базы данных (если нужно вручную)
@bp.route('/api/init_db', methods=['POST'])
def initialize_database():
    try:
        init_db()
        return jsonify({"message": "Database initialized successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Маршрут для получения всех пользователей
@bp.route('/api/users', methods=['GET'])
def get_all_users():
    db = next(get_db_session())
    users = db.query(User).all()
    result = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    return jsonify(result)


# Маршрут для получения информации о пользователе по ID
@bp.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = next(get_db_session())
    user = get_user_by_id(user_id, db)
    if user:
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })
    return jsonify({"error": "User not found"}), 404


# Маршрут для создания нового пользователя
@bp.route('/api/user', methods=['POST'])
def create_user():
    db = next(get_db_session())
    data = request.json
    if not data or 'name' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input"}), 400

    # Создание нового пользователя
    new_user = User(
        name=data['name'],
        email=data['email'],
        hashed_password=data['password']  # Хешируйте пароль перед сохранением
    )
    db.add(new_user)
    db.commit()
    return jsonify({"message": "User created", "id": new_user.id}), 201


# Маршрут для обновления информации о пользователе
@bp.route('/api/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    db = next(get_db_session())
    data = request.json
    user = get_user_by_id(user_id, db)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Обновление полей пользователя
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.hashed_password = data['password']  # Хешируйте пароль перед сохранением

    db.commit()
    return jsonify({"message": "User updated"}), 200


# Маршрут для удаления пользователя
@bp.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = next(get_db_session())
    user = get_user_by_id(user_id, db)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.delete(user)
    db.commit()
    return jsonify({"message": "User deleted"}), 200

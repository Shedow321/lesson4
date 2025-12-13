from flask import Flask
from .models import db
import json
import os
import sqlite3

# Функція для перевірки та додавання колонок у таблицю SQLite 
def _ensure_columns(sqlite_path, table, columns):
    """Перевіряє наявність колонок та додає їх, якщо вони відсутні."""
    if not os.path.exists(sqlite_path):
        return

    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()
    try:
        cur.execute(f"PRAGMA table_info('{table}')")
        existing = {row[1] for row in cur.fetchall()} 

        for col, col_type in columns.items():
            if col not in existing:
                stmt = f"ALTER TABLE {table} ADD COLUMN {col} {col_type};"
                try:
                    cur.execute(stmt)
                except Exception:
                    pass

        # Оновлення часових позначок значень 
        try:
            if 'created_at' in columns:
                cur.execute(f"UPDATE {table} SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL;")
            if 'updated_at' in columns:
                cur.execute(f"UPDATE {table} SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL;")
        except Exception:
            pass

        conn.commit()
    finally:
        cur.close()
        conn.close()

def create_app():
    # Визначаємо місцезнаходження проєкту 
    base_dir = os.path.abspath(os.path.dirname(__file__) + '/..')

    # Створюємо Flask-додаток 
    app = Flask(__name__, 
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'))

    # Завантажуємо конфігурацію з JSON 
    config_path = os.path.join(base_dir, 'config.json')
    with open(config_path) as f:
        config = json.load(f)
    app.config.update(config)

    # Налаштовуємо шлях до бази данних 
    db_path = os.path.abspath(os.path.join(base_dir, config['DB_PATH']))
    
    # Створюємо направлення для БД, якщо вона не існує 
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Викликаємо функцію для додавання всіх необхідних колонок (+ ті, що з ДЗ) 
    _ensure_columns(db_path, 'products', {
        'description': 'TEXT',
        'created_at': 'DATETIME',
        'updated_at': 'DATETIME',
        'stock': 'INTEGER',
        'is_active': 'BOOLEAN',
        'category': 'STRING(50)',
        'rating': 'REAL',
        'sale': 'BOOLEAN'
    })
    
    # Запускаємо SQLAlchemy 
    db.init_app(app)
    
    # Створюємо таблиці, якщо вони ще не створені (в app context)
    with app.app_context():
        db.create_all()

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Text

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    
    # Основні поля 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False) # Рядок до 100 символів, обов'язкове 
    price = db.Column(db.Float, nullable=False)      # Дробове число, обов'язкове 

    # Додаткові поля (з Домашньої роботи 3) 
    description = db.Column(db.Text, nullable=True) # Довгий текст, необов'язкове
    stock = db.Column(db.Integer, nullable=True, default=0) # Ціле число, за замовчуванням 0
    is_active = db.Column(db.Boolean, nullable=True, default=True) # True/False, за замовчуванням True
    category = db.Column(db.String(50), nullable=True) # Рядок до 50 символів
    rating = db.Column(db.Float, nullable=True, default=0) # Дробове число (1-5), за замовчуванням 0
    sale = db.Column(db.Boolean, nullable=True, default=False) # True/False, за замовчуванням False

    # Дата створення та оновлення 
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return f'<Product {self.id}: {self.name}>'
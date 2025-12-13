from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Product

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    """Головна сторінка."""
    return render_template('index.html')

@bp.route('/products')
def product():
    """Сторінка зі списком усіх товарів."""
    # Отримати всі продукти з бази даних
    products = Product.query.all()
    return render_template('product_list.html', products=products)

@bp.route('/add', methods=['GET', 'POST'])
def add_product():
    """Сторінка для додавання нового продукту[cite: 8]."""
    
    if request.method == 'POST':
        # 1. Отримання даних з форми
        name = request.form['name']
        price = request.form['price']
        
        # Отримання даних з додаткових полів ( з ДЗ)
        description = request.form.get('description')
        stock = request.form.get('stock', 0)
        is_active = request.form.get('is_active') == 'on' 
        category = request.form.get('category')
        rating = request.form.get('rating')
        sale = request.form.get('sale') == 'on' 

        # 2. Створення об'єкта Product
        try:
            new_product = Product(
                name=name,
                price=float(price),
                description=description,
                stock=int(stock) if stock else 0,
                is_active=is_active,
                category=category,
                rating=float(rating) if rating else 0.0,
                sale=sale
            )
        except ValueError:
            flash('Помилка: Невірний формат даних для ціни, кількості чи рейтингу!', 'error')
            return redirect(url_for('routes.add_product'))

        # 3. Додавання в базу данних та збереження 
        db.session.add(new_product)
        db.session.commit()
        
        flash('Продукт успішно додано!', 'success')
        return redirect(url_for('routes.product')) # Перенаправлення на список товарів 

    
    return render_template('product_form.html', action='Add', product=None)
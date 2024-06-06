from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for Flask application")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Routes
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    formatted_products = [
        {'id': p.id, 'name': p.name, 'price': p.price} for p in products
    ]
    return jsonify({
        'products': formatted_products,
        'total': len(formatted_products)
    })

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()

    # Validate input data
    if not data or not 'name' in data or not 'price' in data:
        abort(400, description="Request must contain 'name' and 'price' fields")

    try:
        new_product = Product(name=data['name'], price=float(data['price']))
        db.session.add(new_product)
        db.session.commit()
    except (ValueError, TypeError):
        abort(400, description="Invalid input data format")

    return jsonify({'id': new_product.id, 'name': new_product.name, 'price': new_product.price}), 201

# Initialize database and add initial products
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Add initial products
        initial_products = [
            {"name": "Ice Cream", "price": 5.99},
            {"name": "Chocolate", "price": 3.99},
            {"name": "Fruits", "price": 4.99}
        ]

        for product_data in initial_products:
            if not Product.query.filter_by(name=product_data["name"]).first():
                product = Product(name=product_data["name"], price=product_data["price"])
                db.session.add(product)
        db.session.commit()

    app.run(host='0.0.0.0', port=5000)


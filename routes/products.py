from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category', '')
    search = request.args.get('search', '')

    query = Product.query

    if category:
        query = query.filter(Product.category.ilike(f'%{category}%'))
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    products = query.all()
    return jsonify({'products': [p.to_dict() for p in products], 'total': len(products)}), 200


@products_bp.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict()), 200


@products_bp.route('/api/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()

    if not data or not data.get('name') or not data.get('price'):
        return jsonify({'message': 'Name and price are required'}), 400

    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        stock=data.get('stock', 0),
        category=data.get('category', '')
    )
    db.session.add(product)
    db.session.commit()

    return jsonify({'message': 'Product added', 'product': product.to_dict()}), 201


@products_bp.route('/api/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()

    for key, value in data.items():
        setattr(product, key, value)

    db.session.commit()
    return jsonify({'message': 'Product updated', 'product': product.to_dict()}), 200


@products_bp.route('/api/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200
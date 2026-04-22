from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, CartItem, Product

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/api/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    items = CartItem.query.filter_by(user_id=user_id).all()
    
    total = 0
    cart_items = []
    for item in items:
        product = Product.query.get(item.product_id)
        if product:
            subtotal = product.price * item.quantity
            total += subtotal
            cart_items.append({
                'cart_item_id': item.id,
                'product': product.to_dict(),
                'quantity': item.quantity,
                'subtotal': subtotal
            })

    return jsonify({'cart': cart_items, 'total': round(total, 2)}), 200


@cart_bp.route('/api/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get('product_id'):
        return jsonify({'message': 'Product ID is required'}), 400

    product = Product.query.get_or_404(data['product_id'])

    if product.stock < 1:
        return jsonify({'message': 'Product out of stock'}), 400

    existing = CartItem.query.filter_by(
        user_id=user_id,
        product_id=data['product_id']
    ).first()

    if existing:
        existing.quantity += data.get('quantity', 1)
    else:
        item = CartItem(
            user_id=user_id,
            product_id=data['product_id'],
            quantity=data.get('quantity', 1)
        )
        db.session.add(item)

    db.session.commit()
    return jsonify({'message': 'Item added to cart'}), 201


@cart_bp.route('/api/cart/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    user_id = get_jwt_identity()
    item = CartItem.query.filter_by(id=item_id, user_id=user_id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart'}), 200
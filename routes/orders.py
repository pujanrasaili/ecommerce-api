from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Order, CartItem, Product

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/api/orders', methods=['POST'])
@jwt_required()
def place_order():
    user_id = get_jwt_identity()
    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({'message': 'Cart is empty'}), 400

    total = 0
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if not product or product.stock < item.quantity:
            return jsonify({'message': f'Product {item.product_id} is out of stock'}), 400
        total += product.price * item.quantity

    order = Order(user_id=user_id, total_price=round(total, 2))
    db.session.add(order)

    for item in cart_items:
        product = Product.query.get(item.product_id)
        product.stock -= item.quantity
        db.session.delete(item)

    db.session.commit()
    return jsonify({'message': 'Order placed successfully', 'order': order.to_dict()}), 201


@orders_bp.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify({'orders': [o.to_dict() for o in orders]}), 200


@orders_bp.route('/api/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=user_id).first_or_404()
    return jsonify(order.to_dict()), 200
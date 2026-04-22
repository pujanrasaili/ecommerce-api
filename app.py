from flask import Flask
from config import Config
from models import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from auth import auth_bp
from routes.products import products_bp
from routes.cart import cart_bp
from routes.orders import orders_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
swagger = Swagger(app)

app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(orders_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
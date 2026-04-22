import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ecommerce-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ecommerce.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-ecommerce-key-2024'
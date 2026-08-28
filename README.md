# 🛒 E-Commerce REST API

A REST API built with Flask, SQLAlchemy, and JWT Authentication.

## 🚀 Features
- User Authentication (Register/Login with JWT)
- Product Management (CRUD)
- Shopping Cart
- Order Management

## 🛠️ Tech Stack
- Python + Flask
- SQLAlchemy (SQLite)
- JWT Authentication
- Flasgger (Swagger UI)

## ⚙️ Setup

```bash
pip install -r requirements.txt
python app.py
```

## �endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /api/register | Register user | No |
| POST | /api/login | Login user | No |
| GET | /api/products | Get all products | No |
| POST | /api/products | Add product | Yes |
| PUT | /api/products/:id | Update product | Yes |
| DELETE | /api/products/:id | Delete product | Yes |
| GET | /api/cart | Get cart | Yes |
| POST | /api/cart | Add to cart | Yes |
| DELETE | /api/cart/:id | Remove from cart | Yes |
| POST | /api/orders | Place order | Yes |
| GET | /api/orders | Get orders | Yes |


## 👨‍💻 Author

**Pujan Rasaili**

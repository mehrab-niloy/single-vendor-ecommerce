# 🛒 Single Vendor E-Commerce Web Application

A full-stack e-commerce web application built with **Django** that allows customers to browse products, manage their shopping cart, place orders, and complete secure online payments. The project includes user authentication, role-based access control, product management, and an integrated payment gateway.

---

## 🚀 Features

- 🔐 User registration with Email OTP verification
- 👤 Secure login and session-based authentication
- 🛡️ Role-Based Access Control (RBAC)
- 📦 Product and category management (CRUD)
- 🔍 Product search and filtering
- 🛒 Shopping cart with AJAX-based quantity updates
- 🎟️ Coupon/discount system
- 💳 SSLCommerz payment gateway integration
- 📋 Order creation and checkout workflow
- 📜 Order history for customers
- 👤 User profile management
- 🖥️ Admin dashboard for managing products, categories, users, and orders
- ✅ Form validation and error handling throughout the application

---

## 🛠️ Tech Stack

### Backend
- Python
- Django
- MySQL

### Frontend
- Django Templates
- Bootstrap
- JavaScript
- AJAX
- HTML5
- CSS3

### Authentication
- Django Session Authentication
- Email OTP Verification

### Payment Gateway
- SSLCommerz

---



---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/single-vendor-ecommerce.git
```

### 2. Navigate to the project

```bash
cd single-vendor-ecommerce
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure MySQL Database

Update your `settings.py` database configuration.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 7. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create a superuser

```bash
python manage.py createsuperuser
```

### 9. Run the development server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---


---

## 📌 Future Improvements

- Wishlist functionality
- Product reviews and ratings
- Inventory management
- REST API using Django REST Framework
- React frontend
- Docker support
- Deployment on AWS or Render

---

## 👨‍💻 Author

**Md. Niloy**

Backend Developer | Python | Django | MySQL

GitHub: https://github.com/mehrab-niloy

---

## 📄 License

This project is developed for learning and portfolio purposes.

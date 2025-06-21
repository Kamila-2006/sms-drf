# DRF Project

This project is built using Django Rest Framework (DRF). Follow the steps below to set up and run the project in a local development environment.

## Getting Started

```bash
# Clone the repository
git clone <repo-url>
cd <project-name>/backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/development.txt

# Set up the environment variables
cp env-example.txt .env
# Open the .env file and fill in the required values

# Install and configure pre-commit hooks
pre-commit install
pre-commit autoupdate

# Make the start script executable
chmod +x start.sh

# Run the project
./start.sh
```

```commandline
celery -A config worker --loglevel=info
```

# ENDPOINTS

# Users
## POST api/v1/users/authorize/ - авторизация
## POST api/v1/users/verify - проверка смс кода
## POST api/v1/users/login - вход в систему
## POST api/v1/users/logout - выход
## POST api/v1/users/token/refresh/ - рефреш токен
## POST api/v1/users/forgot-password/ - забыли пароль
## POST api/v1/users/reset-password/ - восстановить пароль
## GET api/v1/users/profile/ - посмотреть профиль юзера
## PUT api/v1/users/profile/ - изменить профиль юзера

# Products
## GET api/v1/shop/products/ - список товаров
## GET api/v1/shop/products/id/ - детали товара
## POST api/v1/shop/products/id/like/ - лайкнуть товар

# Cart
## GET api/v1/shop/cart/ - корзина
## POST api/v1/shop/cart/ - добавить товар в корзину
## DELETE api/v1/shop/cart/product_id - убрать товар из корзины

# Orders
## GET api/v1/shop/orders/ - список заказов
## POST api/v1/shop/orders/create/ - оформить заказ
## GET api/v1/shop/orders/id/ - детали заказа

# Reviews
## POST api/v1/shop/products/product_id/review/ - оставить отзыв к товару
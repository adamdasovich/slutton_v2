# Louis Slutton - Backend API

Django REST Framework backend for the Louis Slutton e-commerce platform.

## Features

- ✅ Django REST Framework API
- ✅ JWT Authentication
- ✅ WebSocket support for real-time comments (Django Channels)
- ✅ Stripe payment integration
- ✅ Product catalog with categories
- ✅ Shopping cart functionality
- ✅ Order management
- ✅ Product ratings and comments
- ✅ Video content support
- ✅ Age verification system

## Tech Stack

- Django 5.2
- Django REST Framework
- Django Channels (WebSocket)
- PostgreSQL / SQLite (development)
- Redis (for WebSocket channels)
- Stripe API
- JWT Authentication

## Prerequisites

- Python 3.12+
- Redis server (for WebSocket support)
- PostgreSQL (for production)

## Installation

### 1. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

# Stripe
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key

# Redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```

### 4. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

#### Start Redis (required for WebSocket)

```bash
# Windows (install from https://redis.io/download)
redis-server

# Mac
brew services start redis

# Linux
sudo systemctl start redis
```

#### Start Django Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - Login (get JWT tokens)
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/verify-age/` - Age verification
- `GET /api/auth/profile/` - Get user profile
- `PATCH /api/auth/profile/update/` - Update profile

### Products
- `GET /api/products/` - List all products
- `GET /api/products/{slug}/` - Product detail
- `GET /api/categories/` - List categories
- `GET /api/products/{slug}/videos/` - Product videos

### Cart
- `GET /api/cart/` - Get current cart
- `POST /api/cart/add_item/` - Add item to cart
- `PATCH /api/cart/update_item/` - Update cart item quantity
- `DELETE /api/cart/remove_item/` - Remove item from cart
- `DELETE /api/cart/clear/` - Clear cart

### Orders
- `GET /api/orders/` - List user orders
- `GET /api/orders/{order_number}/` - Order detail
- `POST /api/orders/create_payment_intent/` - Create Stripe payment intent
- `POST /api/orders/confirm_order/` - Confirm order after payment

### Ratings
- `GET /api/products/{slug}/ratings/` - Get product ratings
- `POST /api/products/{slug}/ratings/` - Create/update rating

### Comments (with WebSocket support)
- `GET /api/products/{slug}/comments/` - Get product comments
- `POST /api/products/{slug}/comments/` - Create comment
- `WS /ws/comments/{slug}/` - WebSocket for real-time comments

## WebSocket Usage

Connect to: `ws://localhost:8000/ws/comments/{product_slug}/`

### Send Message:
```json
{
  "action": "new_comment",
  "content": "Great product!",
  "parent_comment": null
}
```

### Receive Message:
```json
{
  "action": "new",
  "comment": {
    "id": 1,
    "username": "user123",
    "content": "Great product!",
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

## Admin Panel

Access the Django admin at `http://localhost:8000/admin/`

Login with the superuser credentials you created.

## Production Deployment

### Environment Variables for Production

```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECRET_KEY=your-secure-secret-key

# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/slutton_db

# Stripe Production Keys
STRIPE_SECRET_KEY=sk_live_your_live_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_live_webhook_secret

# Redis
REDIS_HOST=your-redis-host
REDIS_PORT=6379

# AWS S3 (for media files)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=louis-slutton-media
```

### Deployment Checklist

1. Set `DEBUG=False`
2. Configure PostgreSQL database
3. Set up Redis for production
4. Configure AWS S3 for media files
5. Set up Stripe webhooks
6. Configure CORS for your frontend domain
7. Collect static files: `python manage.py collectstatic`
8. Run migrations: `python manage.py migrate`

## License

Proprietary - All rights reserved

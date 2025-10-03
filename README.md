# 🌸 Louis Slutton - E-Commerce Platform

A full-stack e-commerce platform for adult novelty products and games, featuring a stunning glassmorphism design with hot pink accents, real-time features, and seamless payment processing.

![Tech Stack](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![Stripe](https://img.shields.io/badge/Stripe-008CDD?style=for-the-badge&logo=stripe&logoColor=white)

## 🎯 Project Overview

**Louis Slutton** is a modern, full-featured e-commerce platform designed for selling adult novelty products. The project emphasizes:

- **Stunning UI/UX**: Glassmorphism design with hot pink color scheme (NO generic blue/purple gradients)
- **Real-Time Features**: WebSocket-powered live comments and updates
- **Secure Payments**: Full Stripe integration for checkout
- **Age Verification**: Mandatory 18+ verification system
- **Rich Media**: Video demos with streaming and download capabilities
- **User Engagement**: Star ratings, live discussions, and user profiles

## 🏗️ Architecture

### Backend (Django)
- **Framework**: Django 5.2 + Django REST Framework
- **Real-Time**: Django Channels + WebSockets
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Caching**: Redis
- **Payments**: Stripe API
- **Authentication**: JWT (Simple JWT)

### Frontend (Next.js)
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + Custom Glassmorphism
- **State**: Zustand
- **API Client**: Axios with auto token refresh
- **Payments**: Stripe.js + React Stripe.js

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- Redis Server
- PostgreSQL (for production)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd slutton_v2
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file (see backend/.env.example)
# Add your Stripe keys and other secrets

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start Redis (required for WebSocket)
redis-server

# Run server
python manage.py runserver
```

Backend will be running at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file (see .env.local example)
# Add API URL and Stripe publishable key

# Run development server
npm run dev
```

Frontend will be running at `http://localhost:3000`

## 📋 Features

### ✅ Core E-Commerce
- Product catalog with categories
- Advanced search and filtering
- Shopping cart (session-based + user-based)
- Inventory management
- Order processing and history

### ✅ Payment Processing
- Stripe checkout integration
- Payment intent creation
- Webhook handling for order confirmation
- Secure card processing (PCI compliant via Stripe)

### ✅ User Features
- User registration and authentication (JWT)
- Age verification system (18+)
- User profiles
- Order history
- Wishlist capabilities

### ✅ Product Engagement
- 5-star rating system
- Real-time comment system (WebSocket)
- Threaded discussions
- Video demonstrations with download

### ✅ Real-Time Features
- Live product comments via WebSocket
- Instant comment updates across all connected users
- Edit and delete capabilities
- Reply threading

### ✅ Design & UX
- Glassmorphism aesthetic with frosted glass effects
- Hot pink primary color scheme
- Fully responsive design
- Dark theme optimized
- Custom scrollbars
- Smooth animations and transitions

## 📁 Project Structure

```
slutton_v2/
├── backend/                    # Django backend
│   ├── slutton_backend/       # Main project settings
│   ├── users/                 # User authentication & profiles
│   ├── products/              # Product catalog
│   ├── cart/                  # Shopping cart
│   ├── orders/                # Order management & Stripe
│   ├── ratings/               # Product ratings
│   ├── comments/              # Comments + WebSocket
│   ├── requirements.txt       # Python dependencies
│   └── README.md             # Backend documentation
├── frontend/                   # Next.js frontend
│   ├── app/                   # Next.js app directory
│   ├── components/            # React components
│   ├── lib/                   # API client & utilities
│   ├── store/                 # Zustand state management
│   ├── package.json           # Node dependencies
│   └── README.md             # Frontend documentation
└── README.md                  # This file
```

## 🎨 Design System

### Color Palette
- **Primary Hot Pink**: `#FF1493`
- **Pink Light**: `#FF69B4`
- **Pink Dark**: `#C71585`
- **Background Dark**: `#0a0a0a`
- **Text Primary**: `#ffffff`

### Glassmorphism Components
- `glass-card` - Frosted glass card effect
- `glass-button` - Glassmorphic button
- `glass-input` - Frosted input fields

### Design Principles
- NO blue/purple generic gradients
- Extensive use of backdrop-filter blur
- Semi-transparent backgrounds
- Soft pink glow effects
- Modern, sexy, and sophisticated

## 🔐 Security Features

- JWT token authentication with auto-refresh
- Age verification middleware
- HTTPS required in production
- CORS properly configured
- Stripe webhook signature verification
- SQL injection protection (Django ORM)
- XSS protection
- CSRF protection

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - Login
- `POST /api/auth/verify-age/` - Age verification

### Products
- `GET /api/products/` - List products
- `GET /api/products/{slug}/` - Product detail
- `GET /api/categories/` - List categories

### Cart & Orders
- `GET /api/cart/` - Get cart
- `POST /api/cart/add_item/` - Add to cart
- `POST /api/orders/create_payment_intent/` - Create Stripe payment
- `POST /api/orders/confirm_order/` - Confirm order

### Ratings & Comments
- `GET /api/products/{slug}/ratings/` - Get ratings
- `POST /api/products/{slug}/ratings/` - Rate product
- `WS /ws/comments/{slug}/` - Real-time comments (WebSocket)

[See full API documentation in backend/README.md]

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📦 Deployment

### Backend (Railway / Render / AWS)
1. Set up PostgreSQL database
2. Configure Redis instance
3. Set environment variables
4. Run migrations
5. Collect static files
6. Deploy with Daphne (ASGI server)

### Frontend (Vercel)
1. Push to GitHub
2. Import to Vercel
3. Configure environment variables
4. Auto-deploy on push

[See detailed deployment instructions in respective READMEs]

## 🔧 Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-django-secret
DEBUG=False
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
DATABASE_URL=postgresql://...
REDIS_HOST=your-redis-host
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com/ws
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
```

## 🛠️ Technologies Used

### Backend
- Django 5.2
- Django REST Framework 3.16
- Django Channels 4.0 (WebSocket)
- channels-redis 4.2
- Stripe Python SDK
- PostgreSQL / SQLite
- Redis

### Frontend
- Next.js 15
- React 19
- TypeScript 5
- Tailwind CSS 4
- Zustand 5
- Axios 1.6
- Stripe.js
- React Hot Toast

## 📝 License

Proprietary - All rights reserved

## 👨‍💻 Development

This project was built as a comprehensive full-stack e-commerce platform showcasing modern web development practices, real-time features, and payment processing.

### Key Highlights:
- ✅ Complete Django REST API with all CRUD operations
- ✅ WebSocket integration for real-time features
- ✅ Full Stripe payment flow (frontend + backend)
- ✅ Modern Next.js 15 with App Router
- ✅ Custom glassmorphism design system
- ✅ JWT authentication with auto-refresh
- ✅ Responsive mobile-first design

---

**Built with ❤️ and lots of hot pink ✨**

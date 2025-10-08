# Louis Slutton - Frontend

Next.js frontend for the Louis Slutton e-commerce platform featuring a stunning glassmorphism design with hot pink accents.

## Features

- ✅ Modern glassmorphism UI design
- ✅ Hot pink color scheme (no generic blue/purple gradients!)
- ✅ Product catalog with search and filtering
- ✅ Shopping cart functionality
- ✅ Stripe checkout integration
- ✅ Real-time product comments via WebSocket
- ✅ Star rating system
- ✅ Video player with download support
- ✅ User authentication with age verification
- ✅ Order history and profile management
- ✅ Fully responsive design

## Tech Stack

- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- Zustand (state management)
- Axios (API calls)
- Stripe.js & React Stripe.js
- React Hot Toast (notifications)
- WebSocket API (real-time comments)

## Prerequisites

- Node.js 18+ and npm
- Backend API running (see backend README)

## Installation

### 1. Install dependencies

```bash
npm install
```

### 2. Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── app/                      # Next.js app directory
│   ├── (auth)/              # Auth route group
│   │   ├── login/
│   │   ├── register/
│   │   └── age-verify/
│   ├── products/            # Product pages
│   ├── cart/                # Shopping cart
│   ├── checkout/            # Checkout flow
│   ├── account/             # User account
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Homepage
├── components/
│   ├── ui/                  # Reusable UI components
│   │   ├── GlassCard.tsx
│   │   ├── GlassButton.tsx
│   │   └── GlassInput.tsx
│   ├── layout/              # Layout components
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   ├── product/             # Product components
│   ├── cart/                # Cart components
│   └── checkout/            # Checkout components
├── lib/
│   └── api.ts               # API client & functions
├── store/
│   ├── authStore.ts         # Authentication state
│   └── cartStore.ts         # Cart state
└── hooks/                   # Custom React hooks
```

## Design System

### Glassmorphism Classes

```css
.glass-card        /* Frosted glass card effect */
.glass-button      /* Glassmorphic button */
.glass-input       /* Frosted input field */
```

### Color Variables

```css
--primary-hot-pink: #FF1493
--primary-pink-light: #FF69B4
--primary-pink-dark: #C71585
--bg-dark: #0a0a0a
--text-primary: #ffffff
```

### Usage Example

```tsx
import GlassCard from '@/components/ui/GlassCard';
import GlassButton from '@/components/ui/GlassButton';

export default function MyComponent() {
  return (
    <GlassCard className="p-6">
      <h2>Beautiful Glassmorphism</h2>
      <GlassButton onClick={() => console.log('Clicked!')}>
        Click Me
      </GlassButton>
    </GlassCard>
  );
}
```

## API Integration

The frontend uses Axios with automatic JWT token refresh:

```typescript
import api, { productsAPI } from '@/lib/api';

// Fetch products
const products = await productsAPI.getAll({ category: 'toys' });

// Add to cart
await cartAPI.addItem(productId, quantity);
```

## State Management

Using Zustand for global state:

```typescript
import { useAuthStore } from '@/store/authStore';
import { useCartStore } from '@/store/cartStore';

function MyComponent() {
  const { user, isAuthenticated } = useAuthStore();
  const { cart } = useCartStore();

  // Use state...
}
```

## WebSocket for Real-Time Comments

```typescript
const ws = new WebSocket(`${process.env.NEXT_PUBLIC_WS_URL}/comments/${productSlug}/`);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.action === 'new') {
    // Handle new comment
  }
};

// Send comment
ws.send(JSON.stringify({
  action: 'new_comment',
  content: 'Great product!'
}));
```

## Building for Production

```bash
npm run build
npm start
```

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel
3. Add environment variables
4. Deploy

### Environment Variables for Production

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com/ws
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_your_live_publishable_key
```

## Key Features Implementation

### Age Verification Flow
1. User registers
2. Prompted for age verification
3. Must confirm 18+ and provide DOB
4. Access granted after verification

### Stripe Checkout
1. Add items to cart
2. Proceed to checkout
3. Create payment intent
4. Stripe Elements for card details
5. Confirm payment
6. Order created

### Real-Time Comments
1. WebSocket connection per product
2. Live updates when users comment
3. Support for threaded replies
4. Edit and delete capabilities

## Performance Optimizations

- Image optimization with Next.js Image component
- Route-based code splitting
- API response caching
- Lazy loading for heavy components

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## License

Proprietary - All rights reserved
# Deploy trigger

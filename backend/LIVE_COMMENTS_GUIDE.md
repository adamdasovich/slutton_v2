# Live Comments Setup & Testing Guide

## Overview
The live comments system uses WebSockets via Django Channels for real-time communication. Users can post comments on product pages and see updates instantly across all connected clients.

---

## Prerequisites

### ✅ **NO REDIS NEEDED!** (Development Mode)

**Current Setup:**
- Using **InMemoryChannelLayer** - works immediately!
- Perfect for development and testing
- No external dependencies required

**For Production:**
- When scaling to multiple servers, switch to Redis
- See [NO_REDIS_SETUP.md](NO_REDIS_SETUP.md) for details

---

## Backend Setup

### 1. Dependencies (Already Installed)
```bash
cd backend
venv/Scripts/pip install channels
# channels-redis only needed for production
```

### 2. Start Django with Daphne (ASGI Server)
```bash
cd backend
venv/Scripts/python manage.py runserver
# Or explicitly use Daphne:
# venv/Scripts/daphne -b 0.0.0.0 -p 8000 slutton_backend.asgi:application
```

---

## Frontend Setup

The WebSocket connection is already integrated into the product detail page at:
`frontend/app/products/[slug]/page.tsx`

No additional setup needed!

---

## Testing Live Comments

### Test Scenario 1: Single User

1. **Start Backend:**
   ```bash
   cd backend
   venv/Scripts/python manage.py runserver
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open Product Page:**
   - Go to `http://localhost:3001/products/[any-product-slug]`
   - Scroll to "Live Comments" section

4. **Post a Comment:**
   - Type in comment box
   - Click "Post Comment"
   - Should appear immediately

**Expected Console Output:**
```
WebSocket connected
WebSocket message received: {action: 'new', comment: {...}}
```

---

### Test Scenario 2: Multiple Users (Real-Time)

1. **Open TWO browser windows** side-by-side:
   - Window 1: `http://localhost:3001/products/[product-slug]`
   - Window 2: `http://localhost:3001/products/[product-slug]` (same product!)

2. **Log in as different users** in each window

3. **Post a comment in Window 1:**
   - Type and submit

4. **Watch Window 2:**
   - Comment should appear **instantly** without refresh!

5. **Post from Window 2:**
   - Should also appear in Window 1 instantly

---

## How It Works

### Backend Flow

1. **WebSocket Connection**
   ```
   ws://localhost:8000/ws/comments/{product_slug}/
   ```

2. **Consumer** (`comments/consumers.py`)
   - Handles WebSocket connections
   - Groups users by product slug
   - Broadcasts comments to all users viewing same product

3. **Message Format:**
   ```json
   // Client sends:
   {
     "action": "new_comment",
     "content": "Great product!"
   }

   // Server broadcasts to all:
   {
     "action": "new",
     "comment": {
       "id": 1,
       "username": "john",
       "content": "Great product!",
       "created_at": "2025-10-06T..."
     }
   }
   ```

### Frontend Flow

1. **Connection** - Opens WebSocket on component mount
2. **Send** - Posts comment via WebSocket
3. **Receive** - Listens for new comments from all users
4. **Update UI** - Adds comment to list instantly

---

## Features

### ✅ Currently Working

- Real-time comment posting
- Instant updates across all connected clients
- User avatars (first letter of username)
- Timestamps
- Threaded replies support
- "Edited" indicator
- Empty state when no comments

### 🚧 Future Enhancements

- Delete own comments
- Edit own comments
- Reply to specific comments
- Like/react to comments
- @mentions
- Typing indicators
- Online user count

---

## Troubleshooting

### "WebSocket error" in console

**Cause:** Redis not running or backend not started

**Fix:**
```bash
# Start Redis
redis-server

# Start Django with ASGI support
cd backend
venv/Scripts/python manage.py runserver
```

### Comments don't appear in real-time

**Check:**
1. Are both users on the SAME product page?
2. Is WebSocket connected? (Check browser console)
3. Is Redis running? (`redis-cli ping`)
4. Are you logged in? (Comments require authentication)

### "You must be authenticated to comment"

**Fix:** Log in first at `/login`

### Comments appear but with wrong username

**Issue:** Using `comment.user` instead of `comment.username`

**Fix:** Already fixed in latest code. Make sure you're using:
```tsx
{comment.username}
```

---

## API Endpoints

### REST API (Fallback)
```
GET    /api/products/{slug}/comments/     # List comments
POST   /api/products/{slug}/comments/     # Create comment
```

### WebSocket
```
ws://localhost:8000/ws/comments/{product_slug}/

Actions:
- new_comment: Post new comment
- edit_comment: Edit your comment
- delete_comment: Delete your comment
```

---

## Production Considerations

### For Deployment:

1. **Use secure WebSocket (wss://)**
   ```javascript
   const wsUrl = `wss://yourdomain.com/ws/comments/${slug}/`;
   ```

2. **Redis in Production**
   - Use managed Redis (AWS ElastiCache, Redis Cloud, etc.)
   - Update `CHANNEL_LAYERS` in settings.py

3. **Run with Daphne/Uvicorn**
   ```bash
   daphne -b 0.0.0.0 -p 8000 slutton_backend.asgi:application
   # Or
   uvicorn slutton_backend.asgi:application --host 0.0.0.0 --port 8000
   ```

4. **Use Nginx for WebSocket proxying**
   ```nginx
   location /ws/ {
       proxy_pass http://127.0.0.1:8000;
       proxy_http_version 1.1;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection "upgrade";
   }
   ```

---

## Quick Commands

```bash
# Start everything
cd backend && venv/Scripts/python manage.py runserver &
cd ../frontend && npm run dev &
redis-server &

# Check Redis
redis-cli ping

# View Django channels
cd backend
venv/Scripts/python manage.py shell
>>> from channels.layers import get_channel_layer
>>> channel_layer = get_channel_layer()
>>> await channel_layer.group_send('product_comments_test', {'type': 'test'})
```

---

## Success Criteria

✅ Redis responds to `PONG`
✅ Backend starts without errors
✅ WebSocket connects (console log: "WebSocket connected")
✅ Comment posted in Window 1 appears in Window 2 instantly
✅ Avatars show user's first letter
✅ Timestamps display correctly
✅ No page refresh needed

---

Enjoy your real-time live comments system! 🎉

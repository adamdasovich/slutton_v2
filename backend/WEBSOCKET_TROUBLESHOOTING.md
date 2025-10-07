# WebSocket Troubleshooting Guide

## Common Issues & Solutions

### ❌ "WebSocket is already in CLOSING or CLOSED state"

**Cause:** Trying to send a message before WebSocket is fully connected, or after it has closed.

**Fixed in latest code:**
- ✅ Added `wsConnected` state to track connection
- ✅ Check `readyState` before sending
- ✅ Disable "Post Comment" button when disconnected
- ✅ Visual indicator (green/red dot) shows connection status
- ✅ Auto-reconnect on unexpected disconnect

**Manual Fix (if still occurs):**
1. Refresh the page
2. Check console for "WebSocket connected successfully"
3. Green dot should appear next to "Live Comments"

---

### ❌ WebSocket won't connect

**Check these in order:**

#### 1. Is Redis running?
```bash
redis-cli ping
# Should return: PONG
```

**If not:**
```bash
# Start Redis
redis-server
# Or on Windows: redis-server.exe
```

#### 2. Is Django running?
```bash
cd backend
venv/Scripts/python manage.py runserver
# Should see: Starting development server at http://127.0.0.1:8000/
```

#### 3. Check Django console for errors
Look for:
```
WebSocket HANDSHAKING /ws/comments/[slug]/ [127.0.0.1:xxxxx]
WebSocket CONNECT /ws/comments/[slug]/ [127.0.0.1:xxxxx]
```

If you see errors, Redis might not be configured correctly.

#### 4. Check browser console
```
Connecting to WebSocket: ws://localhost:8000/ws/comments/[slug]/
WebSocket connected successfully
```

If stuck on "Connecting..." → Backend issue
If immediately closed → Authentication or Redis issue

---

### ❌ "You must be authenticated to comment"

**Cause:** Not logged in or session expired

**Fix:**
1. Log in at `/login`
2. Go back to product page
3. WebSocket will auto-connect

---

### ❌ Comments don't appear in real-time

**Checklist:**
- [ ] Both users on SAME product page?
- [ ] Green "Connected" indicator showing?
- [ ] Comment successfully posted (no error)?
- [ ] Redis running?
- [ ] Backend showing WebSocket CONNECT messages?

**Test:**
1. Open browser DevTools → Console
2. Post comment
3. Should see: `WebSocket message received: {action: 'new', comment: {...}}`
4. If not → Backend consumer not broadcasting

---

### ❌ WebSocket keeps disconnecting/reconnecting

**Possible causes:**
1. **Redis crashed** → Restart Redis
2. **Network issue** → Check localhost connection
3. **Backend restarted** → Normal, will auto-reconnect
4. **Browser throttling** → Tab is backgrounded too long

**Auto-reconnect feature:**
- Waits 3 seconds after unexpected disconnect
- Attempts to reconnect automatically
- Shows "Connection lost. Reconnecting..." message

---

### ❌ Backend error: "Invalid HTTP_HOST header"

**Fix:** Add to `backend/slutton_backend/settings.py`:
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

---

### ❌ CORS error on WebSocket

**WebSockets don't use CORS**, but check:
```python
# backend/slutton_backend/settings.py
ASGI_APPLICATION = 'slutton_backend.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

---

## Debugging Steps

### 1. Check Connection Status
**Browser Console:**
```javascript
// Should see:
Connecting to WebSocket: ws://localhost:8000/ws/comments/product-slug/
WebSocket connected successfully
```

**Django Console:**
```
WebSocket HANDSHAKING /ws/comments/product-slug/ [127.0.0.1:xxxxx]
WebSocket CONNECT /ws/comments/product-slug/ [127.0.0.1:xxxxx]
```

### 2. Test Message Flow
**Send comment:**
```javascript
// Browser console should show:
WebSocket message received: {
  action: 'new',
  comment: {
    id: 1,
    username: 'testuser',
    content: 'Test comment',
    ...
  }
}
```

### 3. Check Redis Channels
```bash
redis-cli
> KEYS *
# Should see channel groups like: asgi:group:product_comments_[slug]
```

### 4. Test WebSocket Manually
```javascript
// In browser console:
const ws = new WebSocket('ws://localhost:8000/ws/comments/test-product/');
ws.onopen = () => console.log('Connected!');
ws.onmessage = (e) => console.log('Message:', e.data);
ws.send(JSON.stringify({action: 'new_comment', content: 'Test'}));
```

---

## Visual Indicators

### Connection Status Dot
- 🟢 **Green** = Connected, can post comments
- 🔴 **Red** = Disconnected, attempting to reconnect

### Button States
- **Enabled** = Connected and ready
- **Disabled (grayed out)** = Disconnected or empty comment

### Messages
- "Connected" = All good ✅
- "Disconnected" = Trying to reconnect ⚠️
- "Connection lost. Reconnecting..." = Auto-reconnect in progress 🔄

---

## Production Checklist

Before deploying:

- [ ] Change `ws://` to `wss://` (secure WebSocket)
- [ ] Update WebSocket URL to production domain
- [ ] Configure production Redis (e.g., ElastiCache)
- [ ] Set up Nginx WebSocket proxy
- [ ] Use Daphne/Uvicorn for ASGI
- [ ] Enable WebSocket ping/pong for keepalive
- [ ] Set reasonable reconnect limits
- [ ] Add rate limiting for comments

---

## Quick Fixes

### Restart Everything
```bash
# 1. Kill all processes
# Ctrl+C on Django
# Ctrl+C on Frontend
# Ctrl+C on Redis

# 2. Restart in order:
redis-server &
cd backend && venv/Scripts/python manage.py runserver &
cd frontend && npm run dev &
```

### Clear Redis
```bash
redis-cli FLUSHALL
# Then restart Django
```

### Reset WebSocket Connection
```javascript
// In browser console:
window.location.reload()
```

---

## Success Criteria

✅ Green dot shows "Connected"
✅ Can post comment without errors
✅ Comment appears immediately in same window
✅ **Open 2nd window:** Comment from Window 1 appears in Window 2 instantly
✅ No errors in browser console
✅ No errors in Django console
✅ Redis shows channel groups

---

## Still Having Issues?

1. Check all logs (browser, Django, Redis)
2. Verify versions: `channels==4.x`, `channels-redis==4.x`
3. Test with simple WebSocket client first
4. Ensure no firewall blocking port 8000
5. Try different browser
6. Clear browser cache

---

## Working Example

**Expected flow:**
1. User visits product page
2. Console: "Connecting to WebSocket..."
3. Console: "WebSocket connected successfully"
4. Green dot appears: "Connected"
5. User types comment → clicks "Post Comment"
6. Comment appears instantly at top of list
7. All other users see it instantly (no refresh!)

That's it! 🎉

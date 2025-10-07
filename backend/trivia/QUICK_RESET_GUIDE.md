# Quick Reset Guide for Superusers

## TL;DR - Reset Today's Trivia

### Option 1: Django Admin (Recommended)
1. Go to `http://localhost:8000/admin/trivia/dailytrivia/`
2. Select today's date
3. Choose action: **"Reset all sessions"** → Click Go
4. Select today's date again
5. Choose action: **"Regenerate questions with Claude AI"** → Click Go

### Option 2: Command Line
```bash
cd backend
venv/Scripts/python manage.py reset_trivia --force
```

---

## What Each Method Does

### Admin Actions

| Action | What It Does | Safe? |
|--------|-------------|--------|
| 🔄 Regenerate questions | Replace questions with new Claude-generated ones | ✅ Blocked if users played |
| 🗑️ Reset all sessions | Delete user progress (scores, answers) | ⚠️ DESTRUCTIVE |

### CLI Commands

```bash
# Show help
python manage.py reset_trivia --help

# Check what would happen (safe)
python manage.py reset_trivia

# Force reset (deletes sessions + regenerates)
python manage.py reset_trivia --force

# Reset specific date
python manage.py reset_trivia --date 2025-10-07 --force

# Keep sessions but change questions (DANGEROUS!)
python manage.py reset_trivia --keep-sessions
```

---

## Common Scenarios

### "I want different questions RIGHT NOW"
```bash
python manage.py reset_trivia --force
```
✅ Deletes all user sessions
✅ Generates 15 new questions with Claude
⚠️ Users can replay from scratch

### "A question has a typo, let me fix it"
1. Admin → Daily trivia games → Click date
2. Scroll to questions → Edit the question inline
3. Save

(No reset needed!)

### "Users found a bug, let them replay"
Admin → Select date → Action: "Reset all sessions"

(Questions stay same, just delete progress)

---

## Safety Features

✅ **Won't accidentally delete progress** - Shows warning first
✅ **Requires --force flag** - Extra confirmation in CLI
✅ **Superuser only** - Regular users can't access
✅ **Shows session count** - Know how many users affected

---

## Full Documentation

See [ADMIN_GUIDE.md](ADMIN_GUIDE.md) for complete details, troubleshooting, and advanced usage.

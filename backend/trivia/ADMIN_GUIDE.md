# Trivia Admin Guide - Resetting & Regenerating Questions

## Overview
As a superuser, you can override and reset trivia questions at any time, even before the automatic midnight change. This guide covers all available methods.

---

## Method 1: Django Admin Interface (Easiest)

### Access Admin Panel
1. Go to `http://localhost:8000/admin/`
2. Log in with superuser credentials
3. Navigate to **Trivia → Daily trivia games**

### Available Actions

#### 🔄 Regenerate Questions with Claude AI
**When to use:** You want fresh questions but no one has played yet, OR you've already reset sessions.

**Steps:**
1. Select the trivia date(s) you want to regenerate
2. Choose **Action:** "🔄 Regenerate questions with Claude AI (if no sessions)"
3. Click **Go**

**What happens:**
- ✅ Deletes old questions
- ✅ Generates 15 new questions with Claude
- ✅ Updates theme and description
- ⚠️ BLOCKED if users have already played (shows warning)

**Safety:** Won't delete user progress. Shows warning if sessions exist.

---

#### 🗑️ Reset All Sessions (Allow Replays)
**When to use:** You want users to be able to replay today's trivia (erases their progress).

**Steps:**
1. Select the trivia date(s) you want to reset
2. Choose **Action:** "🗑️ Reset all sessions (allow replays) - DESTRUCTIVE!"
3. Click **Go**

**What happens:**
- ⚠️ Deletes all user game sessions for selected dates
- ⚠️ Deletes all user answers
- ⚠️ Users lose their scores/rankings
- ✅ Users can replay the trivia

**Safety:** DESTRUCTIVE! Cannot be undone. Use carefully.

---

#### Combined Workflow: Full Reset + Regenerate
**When to use:** You want completely new questions AND let users replay.

**Steps:**
1. **First:** Select date → Run "🗑️ Reset all sessions"
2. **Then:** Same date → Run "🔄 Regenerate questions with Claude AI"

Result: Fresh questions, users can play again from scratch.

---

## Method 2: Management Command (CLI)

### Command Syntax
```bash
python manage.py reset_trivia [OPTIONS]
```

### Options

#### Reset Today's Trivia
```bash
python manage.py reset_trivia
```
- Checks if users played
- Shows warning if sessions exist
- Requires `--force` or `--keep-sessions` to proceed

#### Reset Specific Date
```bash
python manage.py reset_trivia --date 2025-10-07
```

#### Force Reset (Delete Sessions)
```bash
python manage.py reset_trivia --force
```
- Deletes all user sessions
- Deletes all answers
- Regenerates questions with Claude
- Users can replay

#### Keep Sessions (Dangerous!)
```bash
python manage.py reset_trivia --keep-sessions
```
- Keeps user sessions intact
- Regenerates questions
- ⚠️ **WARNING:** Sessions become invalid (wrong question IDs)
- Don't use this unless you know what you're doing

---

## Method 3: Manual Script

### Using create_15_question_trivia.py
```bash
# Edit the script to change questions, then run:
cd backend
venv/Scripts/python create_15_question_trivia.py
```

**What it does:**
- Deletes today's trivia
- Creates new trivia with pre-defined 15 questions
- No Claude AI needed
- Good for testing or when API is unavailable

---

## Common Scenarios

### Scenario 1: "I want different questions for today"
**No one has played yet:**
```bash
# Via CLI
python manage.py reset_trivia --force

# Via Admin
Select today → "🔄 Regenerate questions with Claude AI"
```

**Users have already played:**
```bash
# WARNING: This erases user progress!
python manage.py reset_trivia --force

# Or via Admin (2 steps):
# 1. Select today → "🗑️ Reset all sessions"
# 2. Select today → "🔄 Regenerate questions with Claude AI"
```

---

### Scenario 2: "Users reported a bug, let them replay"
```bash
# Via CLI
python manage.py reset_trivia --force

# Via Admin
Select today → "🗑️ Reset all sessions"
```
(Questions stay the same, users can just replay)

---

### Scenario 3: "Generate questions for next week"
```bash
# Generate for 7 days ahead
python manage.py generate_daily_trivia --days-ahead 7

# Then edit via admin if needed
```

---

### Scenario 4: "Claude API is down, use backup questions"
```bash
# Edit create_15_question_trivia.py with your questions, then:
cd backend
venv/Scripts/python create_15_question_trivia.py
```

---

## Safety Checklist

Before resetting trivia, ask yourself:

- [ ] How many users have played? (Check "Sessions" column in admin)
- [ ] Do I need to preserve user scores/rankings?
- [ ] Is the Claude API key configured and working?
- [ ] Should I notify users about the reset?
- [ ] Do I have a backup of the current questions? (Optional)

---

## Troubleshooting

### "Cannot regenerate - users have already played"
**Solution:** Use `--force` flag or run "Reset all sessions" first.

### "Error generating trivia with Claude: authentication_error"
**Solution:** Check your `ANTHROPIC_API_KEY` in `.env` file.

### "Questions were deleted but not replaced!"
**Solution:**
1. Claude API failed after deleting questions
2. Run `create_15_question_trivia.py` to add backup questions
3. Or fix API key and run `reset_trivia` again

### "Invalid question structure"
**Solution:** Claude returned malformed JSON. Run command again.

---

## Best Practices

1. **Preview First:** Check existing questions in admin before regenerating
2. **Low-Traffic Times:** Reset during off-peak hours (3 AM - 6 AM)
3. **Backup:** Copy questions to a text file before major changes
4. **Test:** Use `--date` with future dates to test before affecting today
5. **Communicate:** Notify users if you reset a popular trivia session
6. **Monitor:** Check admin logs after regeneration to ensure 15 questions were created

---

## Automatic Daily Generation

To set up automatic question generation at midnight:

**Windows (Task Scheduler):**
```powershell
# Run daily at 12:01 AM
$action = New-ScheduledTaskAction -Execute "C:\path\to\venv\Scripts\python.exe" -Argument "manage.py generate_daily_trivia" -WorkingDirectory "C:\path\to\backend"
$trigger = New-ScheduledTaskTrigger -Daily -At "00:01"
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "GenerateDailyTrivia"
```

**Linux/Mac (Cron):**
```bash
# Add to crontab
1 0 * * * cd /path/to/backend && venv/bin/python manage.py generate_daily_trivia
```

---

## Quick Reference

| Task | Admin Method | CLI Method |
|------|-------------|------------|
| New questions (no sessions) | Regenerate action | `reset_trivia` |
| New questions (has sessions) | Reset + Regenerate | `reset_trivia --force` |
| Let users replay (same Qs) | Reset sessions action | N/A (use admin) |
| Generate future dates | N/A | `generate_daily_trivia --days-ahead N` |
| Use backup questions | N/A | Run `create_15_question_trivia.py` |

---

## Support

If you encounter issues:
1. Check Django admin logs
2. Check `ANTHROPIC_API_KEY` in `.env`
3. Verify database has trivia record for the date
4. Check backend logs for detailed errors

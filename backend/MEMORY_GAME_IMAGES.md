# Memory Match - Daily Images Management

## Overview
The Memory Match game uses Claude AI to automatically generate 8 sensual/risky image URLs daily. Each day features a unique theme with cohesive imagery.

## Generated Today
**Date:** 2025-10-07
**Theme:** Crimson Temptation
**Description:** A seductive collection celebrating the allure of red - from velvety rose petals and scarlet lips to ruby wine and passionate crimson textures.

## Automatic Daily Generation

### Setup Cron Job (Production)
To automatically generate new images daily at midnight:

```bash
# Edit crontab
crontab -e

# Add this line (runs at midnight daily)
0 0 * * * cd /path/to/backend && python manage.py generate_memory_images
```

### Manual Generation
Generate images for today:
```bash
python manage.py generate_memory_images
```

Generate for specific date:
```bash
python manage.py generate_memory_images --date 2025-10-08
```

Generate for next 7 days:
```bash
python manage.py generate_memory_images --days-ahead 7
```

Force regenerate (overwrite existing):
```bash
python manage.py generate_memory_images --force
```

## Superuser Admin Override

### Via Django Admin Panel

1. **Navigate to Admin:**
   - Go to `http://localhost:8000/admin/games/dailymemoryimages/`

2. **View Daily Images:**
   - See all generated image sets by date
   - Check theme, active status, image count

3. **Regenerate Images (Bulk Action):**
   - Select one or more dates
   - Choose "Regenerate images with Claude AI" from Actions dropdown
   - Click "Go"
   - Claude will generate fresh images for selected dates

4. **Manual Edit:**
   - Click on a specific date
   - Edit theme, description, or images JSON array manually
   - Save changes

### Via Management Command

Reset today's images:
```bash
python manage.py generate_memory_images --force
```

Reset specific date:
```bash
python manage.py generate_memory_images --date 2025-10-08 --force
```

## API Endpoints

### Get Today's Images
```
GET /api/games/memory-images/today/
```

**Response:**
```json
{
  "date": "2025-10-07",
  "theme": "Crimson Temptation",
  "description": "A seductive collection...",
  "images": [
    "https://images.unsplash.com/photo-1515688594390-b649af70d282?w=400&q=80",
    "https://images.unsplash.com/photo-1571875257727-256c39da42af?w=400&q=80",
    ...8 total images
  ]
}
```

## Claude AI Image Themes

Claude generates themed image sets. Example themes:
- **Red Hot Passion** - red items: lips, roses, wine, lingerie
- **Midnight Silk** - black/dark luxury items
- **Golden Hour** - champagne, gold jewelry, warm tones
- **Lace & Leather** - fashion-forward provocative items
- **Bedroom Eyes** - intimate settings, soft lighting
- **French Luxury** - perfume, macarons, champagne, chic items
- **Crimson Temptation** - red velvet, scarlet, ruby wine

## Image Requirements

Claude selects images that are:
- ✅ Sensual and provocative
- ✅ Tasteful yet sexy
- ✅ Adult-oriented (18+)
- ✅ From Unsplash (free stock photos)
- ✅ 400px wide, optimized quality
- ✅ Visually distinct for memory game
- ✅ Cohesive with daily theme

## Troubleshooting

### No images available error
**Error:** "No images available for today"
**Solution:**
```bash
python manage.py generate_memory_images
```

### Claude API error
**Error:** "Claude API error: ..."
**Solution:** Check `ANTHROPIC_API_KEY` environment variable is set correctly

### Images not updating
**Solution:** Use `--force` flag to overwrite:
```bash
python manage.py generate_memory_images --force
```

## Database Model

```python
class DailyMemoryImages(models.Model):
    date = models.DateField(unique=True)
    theme = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    images = models.JSONField()  # Array of 8 URLs
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## Frontend Integration

The Memory Match game automatically fetches today's images:
- API call to `/api/games/memory-images/today/` on page load
- Displays theme at top of game
- Falls back to hardcoded images if API fails
- Shows loading spinner while fetching

## Best Practices

1. **Daily Generation:** Set up cron job for automatic midnight generation
2. **Preview Future Days:** Generate images 1-2 days ahead for testing
3. **Theme Variety:** Let Claude choose diverse themes for daily variety
4. **Quality Check:** Review generated images in admin occasionally
5. **Backup:** Use `--force` carefully as it overwrites existing images

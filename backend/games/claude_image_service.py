"""
Claude AI integration for generating daily memory game images
"""
import anthropic
import os
import json
from datetime import date


class ClaudeImageGenerator:
    """Generate daily image URLs for Memory Match game using Claude AI"""

    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get('ANTHROPIC_API_KEY')
        )

    def generate_daily_images(self, image_date=None):
        """
        Generate 8 sensual/risky image URLs for Memory Match game

        Returns:
            dict: {
                'theme': str,
                'description': str,
                'images': list of 8 image URLs
            }
        """
        if image_date is None:
            image_date = date.today()

        prompt = f"""You are curating a daily set of sensual, provocative images for "Louis Slutton" - an upscale adult products e-commerce platform's Memory Match game.

Generate exactly 8 image selections for {image_date.strftime('%B %d, %Y')}.

REQUIREMENTS:
- Images should be SENSUAL, PROVOCATIVE, TASTEFUL yet SEXY
- Appropriate for an adult audience (18+)
- Think: lingerie, red lips, high heels, silk/satin, champagne, roses, candles, perfume, jewelry, bedroom settings
- Maintain sophistication - Louis Vuitton meets Victoria's Secret aesthetic
- Each image should be visually distinct and memorable for the memory game
- Use Unsplash or similar free stock photo sources

THEME IDEAS:
- "Red Hot Passion" (red items: lips, roses, wine, lingerie)
- "Midnight Silk" (black/dark luxury items)
- "Golden Hour" (champagne, gold jewelry, warm tones)
- "Lace & Leather" (fashion-forward provocative items)
- "Bedroom Eyes" (intimate settings, soft lighting)
- "French Luxury" (perfume, macarons, champagne, chic items)

RESPONSE FORMAT (valid JSON only):
{{
  "theme": "A catchy theme name for today's set (e.g., 'Scarlet Seduction', 'Midnight Desires')",
  "description": "1-2 sentence description of today's theme and vibe",
  "images": [
    "https://images.unsplash.com/photo-XXXXX?w=400&q=80",
    "https://images.unsplash.com/photo-XXXXX?w=400&q=80",
    "https://images.unsplash.com/photo-XXXXX?w=400&q=80",
    "https://images.unsplash.com/photo-XXXXX?w=400&q=80",
    "https://images.unsplash.com/photo-XXXXX?w=400&q=80",
    "https://images.unsplash.com/photo-XXXXX?w=400&q=80",
    "https://images.unsplash.com/photo-XXXXX?w=400&q=80",
    "https://images.unsplash.com/photo-XXXXX?w=400&q=80"
  ]
}}

IMPORTANT:
- Provide real, working Unsplash URLs
- Add ?w=400&q=80 to optimize image size
- Each URL must be unique and different
- Images should be visually cohesive with the theme
- Think about what makes a good memory game: clear, distinct, recognizable images

Return ONLY valid JSON, no other text."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2000,
                temperature=1.0,  # More creative
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Extract JSON from response
            response_text = message.content[0].text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                lines = response_text.split('\n')
                # Remove first line (```json) and last line (```)
                response_text = '\n'.join(lines[1:-1])

            # Parse JSON
            image_data = json.loads(response_text)

            # Validate structure
            if not all(key in image_data for key in ['theme', 'description', 'images']):
                raise ValueError("Missing required keys in Claude response")

            if len(image_data['images']) != 8:
                raise ValueError(f"Expected 8 images, got {len(image_data['images'])}")

            # Validate all URLs start with https://
            for url in image_data['images']:
                if not url.startswith('https://'):
                    raise ValueError(f"Invalid image URL: {url}")

            return image_data

        except anthropic.APIError as e:
            raise Exception(f"Claude API error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response from Claude: {str(e)}")
        except Exception as e:
            raise Exception(f"Error generating images: {str(e)}")

"""
Claude AI integration for automatic trivia question generation
"""
import anthropic
import os
import json
from datetime import date


class ClaudeTriviaGenerator:
    """Generate daily trivia questions using Claude AI"""

    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get('ANTHROPIC_API_KEY')
        )

    def generate_daily_trivia(self, trivia_date=None):
        """
        Generate 15 witty, sexy, sensual, challenging adult trivia questions

        Returns:
            dict: {
                'theme': str,
                'description': str,
                'questions': list of 15 question dicts
            }
        """
        if trivia_date is None:
            trivia_date = date.today()

        prompt = f"""You are creating a daily adult trivia game for "Louis Slutton" - a sophisticated, upscale adult products e-commerce platform.

Generate exactly 15 trivia questions for {trivia_date.strftime('%B %d, %Y')}.

REQUIREMENTS:
- Keep it WITTY, SEXY, SENSUAL, INTRIGUING, and CHALLENGING
- Questions should be tasteful but provocative - think sophisticated adult humor
- Mix of difficulty levels: 5 easy, 5 medium, 5 hard
- Mix of question types: multiple choice, true/false
- Topics: seductive history, anatomy, psychology of attraction, aphrodisiacs, famous lovers, sensual arts, erotic literature, adult film history, sexual wellness, relationship dynamics
- Each question should be educational yet entertaining
- Avoid being crude - maintain elegance and sophistication
- Include fascinating facts in explanations

RESPONSE FORMAT (valid JSON only):
{{
  "theme": "A catchy theme name for today (e.g., 'Seductive Secrets', 'Passionate History')",
  "description": "1-2 sentence description of today's theme",
  "questions": [
    {{
      "question_text": "The question itself",
      "question_type": "multiple_choice" or "true_false",
      "difficulty": "easy" or "medium" or "hard",
      "options": {{"A": "option1", "B": "option2", "C": "option3", "D": "option4"}} (for multiple choice only),
      "correct_answer": "A" (or "B", "C", "D" for multiple choice) or "True"/"False" (for true/false),
      "explanation": "Fascinating explanation of the answer with historical/scientific context",
      "max_points": 10 (easy), 15 (medium), or 20 (hard),
      "order": 1-15
    }},
    ... (14 more questions)
  ]
}}

Make each question captivating and worth pondering. This should keep users excited to come back daily!

Return ONLY valid JSON, no other text."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=8000,
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
                response_text = '\n'.join(lines[1:-1])

            # Parse JSON
            trivia_data = json.loads(response_text)

            # Validate structure
            if not all(key in trivia_data for key in ['theme', 'description', 'questions']):
                raise ValueError("Missing required keys in Claude response")

            if len(trivia_data['questions']) != 15:
                raise ValueError(f"Expected 15 questions, got {len(trivia_data['questions'])}")

            return trivia_data

        except anthropic.APIError as e:
            raise Exception(f"Claude API error: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response from Claude: {str(e)}")
        except Exception as e:
            raise Exception(f"Error generating trivia: {str(e)}")

    def validate_question_structure(self, question):
        """Validate a question has all required fields"""
        required_fields = [
            'question_text', 'question_type', 'difficulty',
            'correct_answer', 'explanation', 'max_points', 'order'
        ]

        for field in required_fields:
            if field not in question:
                raise ValueError(f"Question missing required field: {field}")

        # Validate question type
        if question['question_type'] not in ['multiple_choice', 'true_false']:
            raise ValueError(f"Invalid question_type: {question['question_type']}")

        # Validate difficulty
        if question['difficulty'] not in ['easy', 'medium', 'hard']:
            raise ValueError(f"Invalid difficulty: {question['difficulty']}")

        # Validate points match difficulty
        expected_points = {'easy': 10, 'medium': 15, 'hard': 20}
        if question['max_points'] != expected_points[question['difficulty']]:
            question['max_points'] = expected_points[question['difficulty']]

        # Validate multiple choice has options
        if question['question_type'] == 'multiple_choice' and 'options' not in question:
            raise ValueError("Multiple choice question missing options")

        return True

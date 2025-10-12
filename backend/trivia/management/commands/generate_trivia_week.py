"""
Management command to generate trivia for the next 7 days
Run: python manage.py generate_trivia_week
"""
from django.core.management.base import BaseCommand
from datetime import date, timedelta
from trivia.models import DailyTrivia, TriviaQuestion
import random


class Command(BaseCommand):
    help = 'Generate trivia for the next 7 days'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days ahead to generate (default: 7)',
        )

    def handle(self, *args, **options):
        days_ahead = options['days']

        # Pool of themes
        themes = [
            "Sensual Knowledge",
            "Lingerie Legends",
            "Fashion & Desire",
            "Intimate History",
            "Seductive Science",
            "Luxury & Lace",
            "Passion & Style"
        ]

        # Base question templates (15 questions)
        question_templates = self.get_question_templates()

        created_count = 0
        for day_offset in range(days_ahead):
            trivia_date = date.today() + timedelta(days=day_offset)

            # Check if already exists
            if DailyTrivia.objects.filter(date=trivia_date).exists():
                self.stdout.write(f"Trivia already exists for {trivia_date}")
                continue

            # Create DailyTrivia with random theme
            theme = random.choice(themes)
            daily_trivia = DailyTrivia.objects.create(
                date=trivia_date,
                theme=theme,
                description=f"Test your knowledge with today's {theme.lower()} trivia questions",
                is_active=True
            )

            # Shuffle questions for variety
            questions = random.sample(question_templates, len(question_templates))

            # Create questions
            for order, q_data in enumerate(questions, 1):
                TriviaQuestion.objects.create(
                    daily_trivia=daily_trivia,
                    order=order,
                    question_text=q_data["question_text"],
                    question_type=q_data["question_type"],
                    difficulty=q_data["difficulty"],
                    options=q_data["options"],
                    correct_answer=q_data["correct_answer"],
                    explanation=q_data["explanation"]
                )

            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f"✅ Created trivia for {trivia_date}: {theme}")
            )

        self.stdout.write(
            self.style.SUCCESS(f"\nDone! Generated trivia for {created_count} day(s)")
        )

    def get_question_templates(self):
        """Return pool of 15+ trivia questions"""
        return [
            {
                "question_text": "What ancient civilization is credited with inventing lingerie?",
                "question_type": "multiple_choice",
                "difficulty": "medium",
                "options": {"A": "Ancient Egypt", "B": "Ancient Rome", "C": "Ancient Greece", "D": "Ancient China"},
                "correct_answer": "A",
                "explanation": "Ancient Egyptians were the first to create decorative undergarments, often made from fine linen."
            },
            {
                "question_text": "In what year was Victoria's Secret founded?",
                "question_type": "multiple_choice",
                "difficulty": "hard",
                "options": {"A": "1965", "B": "1977", "C": "1982", "D": "1990"},
                "correct_answer": "B",
                "explanation": "Victoria's Secret was founded in 1977 by Roy Raymond in San Francisco."
            },
            {
                "question_text": "What is the most popular lingerie color worldwide?",
                "question_type": "multiple_choice",
                "difficulty": "easy",
                "options": {"A": "Red", "B": "Black", "C": "White", "D": "Pink"},
                "correct_answer": "B",
                "explanation": "Black is the most popular lingerie color globally, known for its timeless elegance."
            },
            {
                "question_text": "The word 'lingerie' comes from which language?",
                "question_type": "multiple_choice",
                "difficulty": "easy",
                "options": {"A": "Italian", "B": "Spanish", "C": "French", "D": "Latin"},
                "correct_answer": "C",
                "explanation": "Lingerie comes from the French word 'linge', meaning linen or washables."
            },
            {
                "question_text": "What percentage of women wear the wrong bra size?",
                "question_type": "multiple_choice",
                "difficulty": "medium",
                "options": {"A": "50%", "B": "60%", "C": "70%", "D": "80%"},
                "correct_answer": "D",
                "explanation": "Studies show that approximately 80% of women wear the wrong bra size."
            },
            {
                "question_text": "Which material is NOT commonly used in luxury lingerie?",
                "question_type": "multiple_choice",
                "difficulty": "medium",
                "options": {"A": "Silk", "B": "Lace", "C": "Polyester", "D": "Satin"},
                "correct_answer": "C",
                "explanation": "Luxury lingerie typically uses natural materials like silk, lace, and satin rather than synthetic polyester."
            },
            {
                "question_text": "The push-up bra was invented in which decade?",
                "question_type": "multiple_choice",
                "difficulty": "hard",
                "options": {"A": "1940s", "B": "1950s", "C": "1960s", "D": "1970s"},
                "correct_answer": "A",
                "explanation": "The push-up bra was invented in 1948 by Frederick Mellinger, founder of Frederick's of Hollywood."
            },
            {
                "question_text": "What is a 'teddy' in lingerie terminology?",
                "question_type": "multiple_choice",
                "difficulty": "easy",
                "options": {"A": "A type of robe", "B": "A one-piece garment", "C": "A type of stocking", "D": "A bra style"},
                "correct_answer": "B",
                "explanation": "A teddy is a one-piece lingerie garment that combines a camisole and panty."
            },
            {
                "question_text": "Which country produces the most lingerie globally?",
                "question_type": "multiple_choice",
                "difficulty": "medium",
                "options": {"A": "France", "B": "USA", "C": "China", "D": "Italy"},
                "correct_answer": "C",
                "explanation": "China is the world's largest producer of lingerie, manufacturing over 70% of global supply."
            },
            {
                "question_text": "What does 'décolletage' refer to?",
                "question_type": "multiple_choice",
                "difficulty": "medium",
                "options": {"A": "A type of fabric", "B": "The neckline/cleavage area", "C": "A lingerie brand", "D": "A fitting technique"},
                "correct_answer": "B",
                "explanation": "Décolletage refers to the low neckline of a garment that reveals the neck, shoulders, and cleavage."
            },
            {
                "question_text": "The modern bra was patented in which year?",
                "question_type": "multiple_choice",
                "difficulty": "hard",
                "options": {"A": "1889", "B": "1903", "C": "1914", "D": "1925"},
                "correct_answer": "C",
                "explanation": "Mary Phelps Jacob patented the first modern bra in 1914, made from two handkerchiefs and ribbon."
            },
            {
                "question_text": "What is a 'babydoll' style?",
                "question_type": "multiple_choice",
                "difficulty": "easy",
                "options": {"A": "A tight bodysuit", "B": "A short, loose nightgown", "C": "A type of corset", "D": "A robe style"},
                "correct_answer": "B",
                "explanation": "A babydoll is a short, loose-fitting nightgown or negligee, typically with a hem above the knees."
            },
            {
                "question_text": "Which metal is most commonly used in bra underwires?",
                "question_type": "multiple_choice",
                "difficulty": "medium",
                "options": {"A": "Aluminum", "B": "Steel", "C": "Copper", "D": "Titanium"},
                "correct_answer": "B",
                "explanation": "Steel is most commonly used for bra underwires due to its flexibility and durability."
            },
            {
                "question_text": "The term 'negligée' literally means what in French?",
                "question_type": "multiple_choice",
                "difficulty": "hard",
                "options": {"A": "Beautiful", "B": "Delicate", "C": "Neglected", "D": "Soft"},
                "correct_answer": "C",
                "explanation": "Negligée comes from the French verb 'négliger' meaning to neglect, referring to casual, informal attire."
            },
            {
                "question_text": "What is the average lifespan of a well-maintained bra?",
                "question_type": "multiple_choice",
                "difficulty": "medium",
                "options": {"A": "3-6 months", "B": "6-12 months", "C": "1-2 years", "D": "3-5 years"},
                "correct_answer": "B",
                "explanation": "A well-maintained bra typically lasts 6-12 months or about 180 wears before losing elasticity."
            }
        ]

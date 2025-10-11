"""
Quick script to create sample daily trivia
Run this on Railway: python create_sample_trivia.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slutton_backend.settings')
django.setup()

from datetime import date
from trivia.models import DailyTrivia, TriviaQuestion

def create_sample_trivia():
    today = date.today()

    # Check if already exists
    if DailyTrivia.objects.filter(date=today).exists():
        print(f"Trivia already exists for {today}")
        return

    # Create DailyTrivia
    daily_trivia = DailyTrivia.objects.create(
        date=today,
        theme="Sensual Knowledge",
        description="Test your knowledge with today's tantalizing trivia questions",
        is_active=True
    )

    # Sample questions
    questions = [
        {
            "order": 1,
            "question_text": "What ancient civilization is credited with inventing lingerie?",
            "question_type": "multiple_choice",
            "difficulty": "medium",
            "options": {"A": "Ancient Egypt", "B": "Ancient Rome", "C": "Ancient Greece", "D": "Ancient China"},
            "correct_answer": "A",
            "explanation": "Ancient Egyptians were the first to create decorative undergarments, often made from fine linen."
        },
        {
            "order": 2,
            "question_text": "In what year was Victoria's Secret founded?",
            "question_type": "multiple_choice",
            "difficulty": "hard",
            "options": {"A": "1965", "B": "1977", "C": "1982", "D": "1990"},
            "correct_answer": "B",
            "explanation": "Victoria's Secret was founded in 1977 by Roy Raymond in San Francisco."
        },
        {
            "order": 3,
            "question_text": "What is the most popular lingerie color worldwide?",
            "question_type": "multiple_choice",
            "difficulty": "easy",
            "options": {"A": "Red", "B": "Black", "C": "White", "D": "Pink"},
            "correct_answer": "B",
            "explanation": "Black is the most popular lingerie color globally, known for its timeless elegance."
        },
        {
            "order": 4,
            "question_text": "The word 'lingerie' comes from which language?",
            "question_type": "multiple_choice",
            "difficulty": "easy",
            "options": {"A": "Italian", "B": "Spanish", "C": "French", "D": "Latin"},
            "correct_answer": "C",
            "explanation": "Lingerie comes from the French word 'linge', meaning linen or washables."
        },
        {
            "order": 5,
            "question_text": "What percentage of women wear the wrong bra size?",
            "question_type": "multiple_choice",
            "difficulty": "medium",
            "options": {"A": "50%", "B": "60%", "C": "70%", "D": "80%"},
            "correct_answer": "D",
            "explanation": "Studies show that approximately 80% of women wear the wrong bra size."
        },
        {
            "order": 6,
            "question_text": "Which material is NOT commonly used in luxury lingerie?",
            "question_type": "multiple_choice",
            "difficulty": "medium",
            "options": {"A": "Silk", "B": "Lace", "C": "Polyester", "D": "Satin"},
            "correct_answer": "C",
            "explanation": "Luxury lingerie typically uses natural materials like silk, lace, and satin rather than synthetic polyester."
        },
        {
            "order": 7,
            "question_text": "The push-up bra was invented in which decade?",
            "question_type": "multiple_choice",
            "difficulty": "hard",
            "options": {"A": "1940s", "B": "1950s", "C": "1960s", "D": "1970s"},
            "correct_answer": "A",
            "explanation": "The push-up bra was invented in 1948 by Frederick Mellinger, founder of Frederick's of Hollywood."
        },
        {
            "order": 8,
            "question_text": "What is a 'teddy' in lingerie terminology?",
            "question_type": "multiple_choice",
            "difficulty": "easy",
            "options": {"A": "A type of robe", "B": "A one-piece garment", "C": "A type of stocking", "D": "A bra style"},
            "correct_answer": "B",
            "explanation": "A teddy is a one-piece lingerie garment that combines a camisole and panty."
        },
        {
            "order": 9,
            "question_text": "Which country produces the most lingerie globally?",
            "question_type": "multiple_choice",
            "difficulty": "medium",
            "options": {"A": "France", "B": "USA", "C": "China", "D": "Italy"},
            "correct_answer": "C",
            "explanation": "China is the world's largest producer of lingerie, manufacturing over 70% of global supply."
        },
        {
            "order": 10,
            "question_text": "What does 'décolletage' refer to?",
            "question_type": "multiple_choice",
            "difficulty": "medium",
            "options": {"A": "A type of fabric", "B": "The neckline/cleavage area", "C": "A lingerie brand", "D": "A fitting technique"},
            "correct_answer": "B",
            "explanation": "Décolletage refers to the low neckline of a garment that reveals the neck, shoulders, and cleavage."
        },
        {
            "order": 11,
            "question_text": "The modern bra was patented in which year?",
            "question_type": "multiple_choice",
            "difficulty": "hard",
            "options": {"A": "1889", "B": "1903", "C": "1914", "D": "1925"},
            "correct_answer": "C",
            "explanation": "Mary Phelps Jacob patented the first modern bra in 1914, made from two handkerchiefs and ribbon."
        },
        {
            "order": 12,
            "question_text": "What is a 'babydoll' style?",
            "question_type": "multiple_choice",
            "difficulty": "easy",
            "options": {"A": "A tight bodysuit", "B": "A short, loose nightgown", "C": "A type of corset", "D": "A robe style"},
            "correct_answer": "B",
            "explanation": "A babydoll is a short, loose-fitting nightgown or negligee, typically with a hem above the knees."
        },
        {
            "order": 13,
            "question_text": "Which metal is most commonly used in bra underwires?",
            "question_type": "multiple_choice",
            "difficulty": "medium",
            "options": {"A": "Aluminum", "B": "Steel", "C": "Copper", "D": "Titanium"},
            "correct_answer": "B",
            "explanation": "Steel is most commonly used for bra underwires due to its flexibility and durability."
        },
        {
            "order": 14,
            "question_text": "The term 'negligée' literally means what in French?",
            "question_type": "multiple_choice",
            "difficulty": "hard",
            "options": {"A": "Beautiful", "B": "Delicate", "C": "Neglected", "D": "Soft"},
            "correct_answer": "C",
            "explanation": "Negligée comes from the French verb 'négliger' meaning to neglect, referring to casual, informal attire."
        },
        {
            "order": 15,
            "question_text": "What is the average lifespan of a well-maintained bra?",
            "question_type": "multiple_choice",
            "difficulty": "medium",
            "options": {"A": "3-6 months", "B": "6-12 months", "C": "1-2 years", "D": "3-5 years"},
            "correct_answer": "B",
            "explanation": "A well-maintained bra typically lasts 6-12 months or about 180 wears before losing elasticity."
        }
    ]

    # Create questions
    for q_data in questions:
        TriviaQuestion.objects.create(
            daily_trivia=daily_trivia,
            order=q_data["order"],
            question_text=q_data["question_text"],
            question_type=q_data["question_type"],
            difficulty=q_data["difficulty"],
            options=q_data["options"],
            correct_answer=q_data["correct_answer"],
            explanation=q_data["explanation"]
        )

    print(f"✅ Created daily trivia for {today} with 15 questions")
    print(f"Theme: {daily_trivia.theme}")

if __name__ == "__main__":
    create_sample_trivia()

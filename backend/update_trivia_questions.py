"""
Script to manually update or add trivia questions
Run this: python update_trivia_questions.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slutton_backend.settings')
django.setup()

from datetime import date
from trivia.models import DailyTrivia, TriviaQuestion

def update_questions():
    today = date.today()

    # Get today's trivia
    try:
        daily_trivia = DailyTrivia.objects.get(date=today)
    except DailyTrivia.DoesNotExist:
        print(f"No trivia found for {today}")
        return

    # Example: Update question #1
    question = TriviaQuestion.objects.get(daily_trivia=daily_trivia, order=1)
    question.question_text = "What year was the first bra patented?"
    question.options = {"A": "1889", "B": "1903", "C": "1914", "D": "1925"}
    question.correct_answer = "C"
    question.explanation = "Mary Phelps Jacob patented the first modern bra in 1914."
    question.save()
    print(f"Updated question {question.order}")

    # Example: Add a new question (order 16)
    TriviaQuestion.objects.create(
        daily_trivia=daily_trivia,
        order=16,
        question_text="Which fabric is known as the 'queen of fabrics' in lingerie?",
        question_type="multiple_choice",
        difficulty="medium",
        options={"A": "Cotton", "B": "Silk", "C": "Lace", "D": "Polyester"},
        correct_answer="B",
        explanation="Silk is called the 'queen of fabrics' for its luxurious feel and natural beauty."
    )
    print("Added new question #16")

    # Example: Delete a question
    # question_to_delete = TriviaQuestion.objects.get(daily_trivia=daily_trivia, order=15)
    # question_to_delete.delete()
    # print("Deleted question #15")

    print(f"\n✅ Done! Trivia now has {daily_trivia.questions.count()} questions")

if __name__ == "__main__":
    update_questions()

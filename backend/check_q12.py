#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slutton_backend.settings')
django.setup()

from trivia.models import TriviaQuestion
from datetime import date

# Get question 12 from today's trivia
q12 = TriviaQuestion.objects.filter(question_text__contains='colletage').first()

if q12:
    print(f"Question ID: {q12.id}")
    print(f"Question text: {q12.question_text}")
    print(f"Correct answer: |{q12.correct_answer}|")
    print(f"Answer length: {len(q12.correct_answer)}")
    print(f"Answer repr: {repr(q12.correct_answer)}")
    print(f"Answer bytes: {q12.correct_answer.encode()}")
    print(f"Options: {q12.options}")

    # Test the comparison
    user_answer = "B"
    is_correct = user_answer.strip().lower() == q12.correct_answer.strip().lower()
    print(f"\nTest comparison:")
    print(f"User answer: '{user_answer}'")
    print(f"Is correct: {is_correct}")
else:
    print("Question not found!")

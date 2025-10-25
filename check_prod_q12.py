import requests
import json

# Fetch today's trivia from production
response = requests.get('https://api.louisslutton.com/api/trivia/today/', verify=False)
data = response.json()

# Get question 12 (index 11)
q12 = data['trivia']['questions'][11]

print(f"Question 12 (Index 11):")
print(f"ID: {q12['id']}")
print(f"Order: {q12['order']}")
print(f"Text: {q12['question_text']}")
print(f"Options: {json.dumps(q12['options'], indent=2)}")
print(f"Type: {q12['question_type']}")
print(f"Difficulty: {q12['difficulty']}")

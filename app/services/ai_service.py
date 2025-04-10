# app/services/ai_service.py

import openai
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class AIService:
    def __init__(self):
        pass

    def summarize_code(self, code: str) -> str:
        # Placeholder for code summarization
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or whatever engine you prefer
            prompt=f"Summarize the following code:\n{code}",
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def generate_test_case(self, code: str) -> str:
        # Placeholder for test case generation
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate test cases for the following code:\n{code}",
            max_tokens=150
        )
        return response.choices[0].text.strip()


    def divide(self, a, b):
        return a/b

    def subtract(self, a, b):
        return a-b

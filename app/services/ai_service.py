# app/services/ai_service.py

import openai
import re
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class AIService:
    def __init__(self):
        pass

    def summarize_code(self, code: str) -> str:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you want
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes code in great detail."},
                {"role": "user", "content": f"Summarize the following code, highlighting the specific changes made and the rationale behind them:\n{code}"}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    def generate_test_case(self, code: str) -> str:
        # Separate test cases by methods
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you want
            messages=[
                {"role": "system", "content": "You are an assistant that generates meaningful test cases for each method in a code."},
                {"role": "user", "content": f"Please determine if the following content is code or plain text. Use reasoning like the existence of functions, language or framework resemblance to determine if the file itself is code or plain text. If it's code, identify methods and generate detailed test cases for each method, making sure to separate test cases by methods. If it's text only document, return a clear message stating that no test cases can be generated and explain why:\n{code}"}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    def generate_diagram(self, code: str) -> str:
        # Generate Mermaid diagram based on code analysis
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that generates diagrams for code in Mermaid.js format."},
                {"role": "user", "content": f"Analyze the following code and generate a Mermaid.js diagram that represents its structure. Focus on classes, methods, and their relationships.\n{code}"}
            ],
            max_tokens=600
        )
        
        diagram_code = response.choices[0].message.content.strip()

        if diagram_code:
        # Check if diagram_code already starts with 'classDiagram' and remove it if it does.
            if diagram_code.startswith("classDiagram"):
                diagram_code = diagram_code[len("classDiagram"):].strip()
            diagram_code = re.sub(r'\[:"(.*?)"\]', r': "\1"', diagram_code) # fix [:"label"] to : "label"
            diagram_code = re.sub(r'\.code', '', diagram_code) # remove .code occurrences
            diagram_code = re.sub(r'\[code\]', '', diagram_code) # remove [code] occurrences
            if not diagram_code.startswith("```mermaid"):
                diagram_code = f"```mermaid\nclassDiagram\n{diagram_code}\n```"
            diagram_code = f"```mermaid\nclassDiagram\n{diagram_code}\n```"
        else:
            diagram_code = """
            ```mermaid
            classDiagram
                class CodeStructure {
                    +method1()
                    +method2()
                }
            ```
            """
        
        # Return the formatted diagram code for GitHub (ensure proper syntax)
        return diagram_code.strip()

    def divide(self, a, b):
        return a/b

import google.generativeai as genai
from flask import current_app

class AIResumeEnhancer:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
    
    def enhance_text(self, text):
        prompt = """
        Enhance this text to be more professional and polished by:
        - Improving grammar and spelling
        - Making the language more professional
        - Enhancing clarity and conciseness
        - Maintaining the original meaning
        
        Text to enhance:
        {text}
        """.format(text=text)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Error enhancing text: {str(e)}")
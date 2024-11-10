import google.generativeai as genai
from flask import current_app

# Class to enhance text.
class AIResumeEnhancer:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        
    # Function to enhance text.
    def enhance_text(self, text):
        # Prompts the model to enhance the text.
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
            # Generates the response.
            response = self.model.generate_content(prompt)
            # Returns the response.
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Error enhancing text: {str(e)}")
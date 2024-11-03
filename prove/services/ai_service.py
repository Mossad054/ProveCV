class AIResumeEnhancer:
    def __init__(self):
        # Remove the genai.configure from __init__
        pass  # We'll configure it when needed

    def initialize_genai(self, app):
        # Add this new method to initialize Gemini
        genai.configure(api_key=app.config['GEMINI_API_KEY'])
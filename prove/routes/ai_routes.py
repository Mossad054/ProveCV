from flask import Blueprint, request, jsonify
from services.ai_service import AIResumeEnhancer

# Creates a blueprint for the AI routes.
ai_bp = Blueprint('ai', __name__)
ai_service = AIResumeEnhancer()

# Function to enhance text.
@ai_bp.route('/enhance', methods=['POST'])
def enhance_text():
    try:
        data = request.get_json()
        # Gets the JSON data from the request.
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        # Checks if the text is provided.
        text = data['text']
        # Enhances the text.
        enhanced_text = ai_service.enhance_text(text)
        # Returns the original and enhanced text.
        return jsonify({
            'original_text': text,
            'enhanced_text': enhanced_text
        })
        # Returns the original and enhanced text.
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    # Returns an error if the text is not provided.
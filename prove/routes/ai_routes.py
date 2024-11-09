from flask import Blueprint, request, jsonify
from services.ai_service import AIResumeEnhancer

ai_bp = Blueprint('ai', __name__)
ai_service = AIResumeEnhancer()

@ai_bp.route('/enhance', methods=['POST'])
def enhance_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
            
        text = data['text']
        enhanced_text = ai_service.enhance_text(text)
        
        return jsonify({
            'original_text': text,
            'enhanced_text': enhanced_text
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
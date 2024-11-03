from flask import Blueprint, current_app
from services.ai_service import AIResumeEnhancer

ai_bp = Blueprint('ai', __name__)
ai_service = AIResumeEnhancer()

@ai_bp.route('/enhance', methods=['POST'])
def enhance_text():
    # Your route logic here
    pass
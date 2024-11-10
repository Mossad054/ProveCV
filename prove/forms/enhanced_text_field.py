from wtforms import TextAreaField
from wtforms.widgets import TextArea

class EnhancedTextAreaField(TextAreaField):
    def __init__(self, label=None, validators=None, **kwargs):
        super().__init__(label, validators, **kwargs)
        self.widget = TextArea()
        
    def __call__(self, **kwargs):
        # Adds AI enhancement button next to the textarea.
        field_html = super().__call__(**kwargs)
        button_html = f"""
        <button type="button" 
                class="ai-enhance-btn" 
                data-field-id="{self.id}"
                onclick="enhanceText('{self.id}')">
            Enhance with AI
        </button>
        """
        #returns button_html
        return f"{field_html}{button_html}" 
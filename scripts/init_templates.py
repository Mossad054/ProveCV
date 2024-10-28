import sys
import os
# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Template

def init_templates():
    app = create_app()
    with app.app_context():
        templates = [
            Template(name='template1', content='Basic Template'),
            Template(name='template2', content='Professional Template')
        ]
        
        for template in templates:
            db.session.add(template)
        
        db.session.commit()

if __name__ == '__main__':
    init_templates() 
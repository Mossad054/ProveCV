from flask import Blueprint, render_template
from app.models import Template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    templates = Template.query.filter_by(is_active=True).all()  # Fetch active templates
    return render_template('index.html', templates=templates)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Template(db.Model):
    __tablename__ = 'templates'
    
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=True) 
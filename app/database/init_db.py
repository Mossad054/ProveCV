from app import create_app, db

app = create_app()

with app.app_context():
    # Create all database tables
    db.create_all()
    print("Database initialized successfully!")

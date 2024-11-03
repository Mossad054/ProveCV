from flask import Flask
from flask_migrate import Migrate, upgrade, migrate
from app import app, db

def run_migrations():
    try:
        # Create Flask app instance
        app = app
        
        # Initialize migration with app and db
        migrate = Migrate(app, db)
        
        with app.app_context():
            # Create migration
            migrate()
            
            # Apply migration
            upgrade()
            
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")

if __name__ == "__main__":
    run_migrations() 
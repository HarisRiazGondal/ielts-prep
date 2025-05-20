from flask_migrate import Migrate
from app import app, db
from models import User, Role, Section, Difficulty, Exercise, PracticeRecord
from models import Badge, UserBadge, Score, ReadingPassage, ReadingTest, ReadingQuestion, Article, ArticleView
import os
import sys

# Initialize Flask-Migrate
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # Check if database exists and has users
        try:
            user_count = User.query.count()
            print(f"Database exists with {user_count} users.")
        except:
            print("Database doesn't exist, initializing...")
            db.create_all()
            print("Database created.")

        # Check if migrations folder exists
        if not os.path.exists('migrations'):
            print("Initializing migrations folder...")
            os.system("flask db init")

        # Create migration
        print("Creating migration for schema changes...")
        os.system('flask db migrate -m "Add ArticleView model"')
        
        # Apply migration
        print("Applying migration...")
        os.system("flask db upgrade")
        
        print("Migration complete!") 
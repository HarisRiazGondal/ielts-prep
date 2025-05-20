from app import app, db
from models import Exercise

def verify_test():
    """Verify that the listening test was added to the database"""
    with app.app_context():
        # Look for the test by title
        test = Exercise.query.filter_by(title="IELTS Listening Mock Test").first()
        
        if test:
            print(f"Found test with ID: {test.id}")
            print(f"Title: {test.title}")
            print(f"Description: {test.description}")
            print(f"Section: {test.section.name}")
            print(f"Difficulty: {test.difficulty.name}")
            print(f"Duration: {test.duration} minutes")
            print(f"Audio file: {test.audio_file}")
            print(f"Is mock test: {test.is_mock_test}")
        else:
            print("No test found with title 'IELTS Listening Mock Test'")

if __name__ == "__main__":
    verify_test() 
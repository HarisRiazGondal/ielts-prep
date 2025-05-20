import json
import os
import shutil
from app import app, db
from models import Exercise, Section, Difficulty

def create_mock_listening_test():
    """Create a mock IELTS listening test using data from JSON"""
    with app.app_context():
        # Load test data from JSON file
        with open('listening_test_structure.json', 'r') as f:
            test_data = json.load(f)
        
        # Get listening section
        listening_section = Section.query.filter_by(name='Listening').first()
        if not listening_section:
            print("Listening section not found in database")
            return
        
        # Get Advanced difficulty
        advanced_difficulty = Difficulty.query.filter_by(name='Advanced').first()
        if not advanced_difficulty:
            print("Advanced difficulty not found in database")
            return
        
        # Create the exercise
        mock_test = Exercise(
            title="IELTS Listening Mock Test",
            description="A complete IELTS Listening test with 40 questions across 4 sections: social conversation, monologue, academic discussion, and academic lecture.",
            section_id=listening_section.id,
            difficulty_id=advanced_difficulty.id,
            duration=30,  # Standard IELTS listening test duration
            points=40,    # One point per question
            is_mock_test=True,
            audio_file="ielts_listening_test1.mp3",
            content=json.dumps(test_data)
        )
        
        db.session.add(mock_test)
        db.session.commit()
        
        print(f"Created mock IELTS listening test with ID: {mock_test.id}")
        
        # Ensure audio file is in the right location
        source_audio = os.path.join('listing test material', 'tset 1.mp3')
        dest_audio = os.path.join('static', 'uploads', 'audio', 'ielts_listening_test1.mp3')
        
        try:
            if not os.path.exists(dest_audio):
                shutil.copy2(source_audio, dest_audio)
                print(f"Copied audio file to {dest_audio}")
            else:
                print(f"Audio file already exists at {dest_audio}")
        except Exception as e:
            print(f"Error copying audio file: {e}")
        
        print("Mock listening test created successfully!")

if __name__ == '__main__':
    create_mock_listening_test() 
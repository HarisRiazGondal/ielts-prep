from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import func

class Role(db.Model):
    """Role model for defining user roles"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(255))
    users = db.relationship('User', backref='role', lazy=True)

class User(UserMixin, db.Model):
    """User model for authentication and profile"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Profile fields
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    target_score = db.Column(db.Float, default=7.0)
    
    # Relationships
    scores = db.relationship('Score', backref='user', lazy=True)
    practice_records = db.relationship('PracticeRecord', backref='user', lazy=True)
    badges = db.relationship('UserBadge', backref='user', lazy=True)
    article_views = db.relationship('ArticleView', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @property
    def is_admin(self):
        return self.role.name == 'admin'
    
    @property
    def points(self):
        total = 0
        for record in self.practice_records:
            total += record.points_earned
        return total

class Section(db.Model):
    """IELTS exam sections"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)  # Reading, Writing, Listening, Speaking
    description = db.Column(db.Text)
    
    # Relationships
    exercises = db.relationship('Exercise', backref='section', lazy=True)
    
    def __repr__(self):
        return f'<Section {self.name}>'

class Difficulty(db.Model):
    """Difficulty levels for exercises"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)  # Beginner, Intermediate, Advanced
    description = db.Column(db.Text)
    
    # Relationships
    exercises = db.relationship('Exercise', backref='difficulty', lazy=True)
    
    def __repr__(self):
        return f'<Difficulty {self.name}>'

class Exercise(db.Model):
    """Exercises for practice"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    difficulty_id = db.Column(db.Integer, db.ForeignKey('difficulty.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_mock_test = db.Column(db.Boolean, default=False)
    content = db.Column(db.Text, nullable=False)  # JSON content storing questions, answers, etc.
    duration = db.Column(db.Integer, default=0)  # Duration in minutes
    points = db.Column(db.Integer, default=10)  # Points awarded for completion
    
    # For listening exercises
    audio_file = db.Column(db.String(255))
    
    # Relationships
    records = db.relationship('PracticeRecord', backref='exercise', lazy=True)
    
    def __repr__(self):
        return f'<Exercise {self.title}>'

class PracticeRecord(db.Model):
    """Record of user's practice sessions"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    answers = db.Column(db.Text)  # JSON answers provided by user
    score = db.Column(db.Float)  # Score between 0-9
    feedback = db.Column(db.Text)  # AI feedback
    points_earned = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<PracticeRecord {self.id}>'
    
    @property
    def duration(self):
        """Calculate duration in minutes"""
        if self.completed_at and self.started_at:
            delta = self.completed_at - self.started_at
            return delta.total_seconds() / 60
        return 0

class Score(db.Model):
    """Overall IELTS scores for the user"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reading = db.Column(db.Float, default=0)  # 0-9 score
    writing = db.Column(db.Float, default=0)  # 0-9 score
    listening = db.Column(db.Float, default=0)  # 0-9 score
    speaking = db.Column(db.Float, default=0)  # 0-9 score
    overall = db.Column(db.Float, default=0)  # 0-9 score
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    mock_test = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Score {self.id}>'
    
    def calculate_overall(self):
        """Calculate overall score as average of section scores"""
        total = (self.reading + self.writing + self.listening + self.speaking)
        self.overall = round(total / 4, 1)
        return self.overall

class Badge(db.Model):
    """Badges for gamification"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(100))
    points_required = db.Column(db.Integer, default=0)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    
    # Relationships
    user_badges = db.relationship('UserBadge', backref='badge', lazy=True)
    section = db.relationship('Section', backref='badges', lazy=True)
    
    def __repr__(self):
        return f'<Badge {self.name}>'

class UserBadge(db.Model):
    """Association table for users and their earned badges"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserBadge {self.id}>'

class ReadingPassage(db.Model):
    """Model to store reading passages"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationship with questions
    questions = db.relationship('ReadingQuestion', backref='passage', lazy=True, cascade="all, delete-orphan")
    
    # Relationship with test
    test_id = db.Column(db.Integer, db.ForeignKey('reading_test.id'))
    
    def __repr__(self):
        return f'<ReadingPassage {self.title}>'

class ReadingTest(db.Model):
    """Model to store complete reading tests"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_published = db.Column(db.Boolean, default=False)
    
    # Relationship with passages (one test has multiple passages)
    passages = db.relationship('ReadingPassage', backref='test', lazy=True, cascade="all, delete-orphan")
    
    # Link to Exercise model for the actual test
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    exercise = db.relationship('Exercise')
    
    def __repr__(self):
        return f'<ReadingTest {self.title}>'

class ReadingQuestion(db.Model):
    """Model to store reading questions"""
    id = db.Column(db.Integer, primary_key=True)
    passage_id = db.Column(db.Integer, db.ForeignKey('reading_passage.id'), nullable=False)
    question_number = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)
    options = db.Column(db.Text)  # JSON for multiple choice, matching, etc.
    correct_answer = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'<ReadingQuestion {self.question_number}>'

class Article(db.Model):
    """Model to store resource articles/blogs"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    category = db.Column(db.String(50))  # e.g., "Reading Tips", "IELTS Strategy", "Writing Samples"
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)
    
    # Relationships
    section = db.relationship('Section', backref='articles', lazy=True)
    author = db.relationship('User', backref='articles', lazy=True)
    views = db.relationship('ArticleView', backref='article', lazy=True)
    
    def __repr__(self):
        return f'<Article {self.title}>'
    
    @property
    def view_count(self):
        """Get the total number of views for this article"""
        return len(self.views)
    
    @property
    def unique_view_count(self):
        """Get the number of unique users who viewed this article"""
        unique_users = set([view.user_id for view in self.views])
        return len(unique_users)

class ArticleView(db.Model):
    """Model to track article views"""
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ArticleView article_id={self.article_id} user_id={self.user_id}>'

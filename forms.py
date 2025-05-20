from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, IntegerField, FloatField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange, Optional, URL
from models import User

class LoginForm(FlaskForm):
    """Form for user login"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """Form for user registration"""
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=50)])
    target_score = FloatField('Target IELTS Score', validators=[Optional(), NumberRange(min=0, max=9)])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please use a different email or login.')

class ResetPasswordRequestForm(FlaskForm):
    """Form for requesting password reset"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    """Form for resetting password"""
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class WritingResponseForm(FlaskForm):
    """Form for writing exercise responses"""
    content = TextAreaField('Your Answer', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SpeakingResponseForm(FlaskForm):
    """Form for speaking exercise responses"""
    audio_data = TextAreaField('Recorded Audio Data')  # Will be populated by JavaScript
    submit = SubmitField('Submit')

class ProfileForm(FlaskForm):
    """Form for user profile updates"""
    first_name = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=50)])
    target_score = FloatField('Target IELTS Score', validators=[Optional(), NumberRange(min=0, max=9)])
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=8)])
    password_confirm = PasswordField('Confirm New Password', validators=[EqualTo('new_password')])
    submit = SubmitField('Update Profile')

class AdminUserForm(FlaskForm):
    """Form for admin to create/edit users"""
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=8)])
    role_id = SelectField('Role', validators=[DataRequired()], coerce=int)
    first_name = StringField('First Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=50)])
    submit = SubmitField('Save User')

class ExerciseForm(FlaskForm):
    """Form for creating/editing exercises"""
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    section_id = SelectField('Section', validators=[DataRequired()], coerce=int)
    difficulty_id = SelectField('Difficulty Level', validators=[DataRequired()], coerce=int)
    content = TextAreaField('Content (JSON)', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    points = IntegerField('Points', validators=[DataRequired(), NumberRange(min=1)])
    is_mock_test = BooleanField('Is Mock Test')
    audio_file = FileField('Audio File (for Listening exercises)')
    submit = SubmitField('Save Exercise')

class ReadingPassageForm(FlaskForm):
    """Form for creating a reading passage"""
    title = StringField('Passage Title', validators=[DataRequired()])
    content = TextAreaField('Passage Content', validators=[DataRequired()])
    submit = SubmitField('Save Passage')

class BaseQuestionForm(FlaskForm):
    """Base form for all question types"""
    question_text = TextAreaField('Question Text', validators=[DataRequired()])
    question_number = IntegerField('Question Number', validators=[DataRequired(), NumberRange(min=1)])
    
class MatchingInfoForm(BaseQuestionForm):
    """Form for matching information questions"""
    options = TextAreaField('Options (One per line)', validators=[DataRequired()])
    correct_answer = StringField('Correct Answer', validators=[DataRequired()])
    submit = SubmitField('Add Question')
    
class TrueFalseNotGivenForm(BaseQuestionForm):
    """Form for true/false/not given questions"""
    correct_answer = SelectField('Correct Answer', choices=[
        ('TRUE', 'True'), 
        ('FALSE', 'False'), 
        ('NOT GIVEN', 'Not Given')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Question')
    
class FillBlankForm(BaseQuestionForm):
    """Form for fill in the blank questions"""
    correct_answer = StringField('Correct Answer', validators=[DataRequired()])
    submit = SubmitField('Add Question')
    
class MultipleChoiceForm(BaseQuestionForm):
    """Form for multiple choice questions"""
    option_a = StringField('Option A', validators=[DataRequired()])
    option_b = StringField('Option B', validators=[DataRequired()])
    option_c = StringField('Option C', validators=[DataRequired()])
    option_d = StringField('Option D', validators=[DataRequired()])
    correct_answer = SelectField('Correct Answer', choices=[
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')
    ], validators=[DataRequired()])
    submit = SubmitField('Add Question')

class HeadingMatchingForm(BaseQuestionForm):
    """Form for heading matching questions"""
    options = TextAreaField('Headings (One per line)', validators=[DataRequired()])
    correct_answer = StringField('Correct Answer', validators=[DataRequired()])
    submit = SubmitField('Add Question')

class ShortAnswerForm(BaseQuestionForm):
    """Form for short answer questions"""
    correct_answer = StringField('Correct Answer', validators=[DataRequired()])
    submit = SubmitField('Add Question')

class SummaryCompletionForm(BaseQuestionForm):
    """Form for summary completion questions"""
    correct_answer = StringField('Correct Answer', validators=[DataRequired()])
    submit = SubmitField('Add Question')

class ReadingTestForm(FlaskForm):
    """Form for creating a complete reading test"""
    title = StringField('Test Title', validators=[DataRequired()])
    description = TextAreaField('Test Description', validators=[DataRequired()])
    difficulty_id = SelectField('Difficulty', validators=[DataRequired()], coerce=int)
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Create Test')

class ListeningExerciseForm(FlaskForm):
    """Form for creating listening exercises"""
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    difficulty_id = SelectField('Difficulty', validators=[DataRequired()], coerce=int)
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    points = IntegerField('Points', validators=[DataRequired(), NumberRange(min=1)])
    is_mock_test = BooleanField('Is Mock Test')
    audio_file = FileField('Audio File', validators=[DataRequired()])
    transcript = TextAreaField('Transcript (Optional)')
    question_count = IntegerField('Number of Questions', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Save Listening Exercise')

class ReadingExerciseForm(FlaskForm):
    """Form for creating reading exercises"""
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    difficulty_id = SelectField('Difficulty', validators=[DataRequired()], coerce=int)
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    points = IntegerField('Points', validators=[DataRequired(), NumberRange(min=1)])
    is_mock_test = BooleanField('Is Mock Test')
    passage = TextAreaField('Reading Passage', validators=[DataRequired()])
    question_count = IntegerField('Number of Questions', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Save Reading Exercise')

class WritingExerciseForm(FlaskForm):
    """Form for creating writing exercises"""
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    difficulty_id = SelectField('Difficulty', validators=[DataRequired()], coerce=int)
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    points = IntegerField('Points', validators=[DataRequired(), NumberRange(min=1)])
    is_mock_test = BooleanField('Is Mock Test')
    prompt = TextAreaField('Writing Prompt', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    word_count = IntegerField('Minimum Word Count', validators=[DataRequired(), NumberRange(min=1)])
    example = TextAreaField('Example Answer (Optional)')
    submit = SubmitField('Save Writing Exercise')

class ArticleForm(FlaskForm):
    """Form for creating and editing resource articles"""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    summary = TextAreaField('Summary', validators=[DataRequired(), Length(max=500)])
    image_url = StringField('Image URL', validators=[Optional(), URL()])
    category = SelectField('Category', choices=[
        ('reading-tips', 'Reading Tips'),
        ('writing-tips', 'Writing Tips'),
        ('listening-tips', 'Listening Tips'),
        ('speaking-tips', 'Speaking Tips'),
        ('vocabulary', 'Vocabulary Building'),
        ('grammar', 'Grammar Tips'),
        ('test-strategy', 'IELTS Test Strategy'),
        ('practice-material', 'Practice Material')
    ])
    section_id = SelectField('Related Section', validators=[Optional()], coerce=int)
    is_published = BooleanField('Publish Now', default=True)
    submit = SubmitField('Save Article')

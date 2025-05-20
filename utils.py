import re
import json
from datetime import datetime

def analyze_writing(text):
    """
    Simple rule-based assessment of a writing sample
    Returns a dict with scores and feedback
    """
    # Basic metrics
    word_count = len(text.split())
    unique_words = len(set(text.lower().split()))
    avg_word_length = sum(len(word) for word in text.split()) / max(1, word_count)
    
    # Simple scoring based on length and complexity
    if word_count < 150:
        score = 4.0
        feedback = "Your response is too short. Aim for at least 250 words for Task 2 or 150 words for Task 1."
    elif word_count < 250:
        score = 5.5
        feedback = "Your response meets the minimum length but could be more developed."
    else:
        # Basic score based on word complexity
        if avg_word_length < 4.0 or unique_words / max(1, word_count) < 0.4:
            score = 6.0
            feedback = "Good length, but try to use more varied vocabulary and complex sentence structures."
        elif avg_word_length < 4.5 or unique_words / max(1, word_count) < 0.5:
            score = 7.0
            feedback = "Good work! Your writing shows good vocabulary range and sentence structure."
        else:
            score = 8.0
            feedback = "Excellent! You have a wide vocabulary range and good control of complex sentences."
    
    return {
        'score': score,
        'feedback': feedback,
        'word_count': word_count,
        'unique_words': unique_words,
        'avg_word_length': avg_word_length
    }

def format_datetime(value, format='%Y-%m-%d %H:%M'):
    """Format a datetime object to a string"""
    if value is None:
        return ""
    return value.strftime(format)

def is_valid_json(json_str):
    """Check if a string is valid JSON"""
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False

def parse_json(json_str):
    """Safely parse JSON string and return a dictionary"""
    try:
        if isinstance(json_str, dict):
            return json_str
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return {}

def check_badge_eligibility(user):
    """Check if user is eligible for any new badges"""
    from app import db
    from models import Badge, UserBadge, Section
    
    # Check section-based badges
    for section in Section.query.all():
        # Get completed exercises for this section
        section_records = [r for r in user.practice_records 
                          if r.completed_at and r.exercise.section_id == section.id]
        
        # Count completed exercises
        completed_count = len(section_records)
        
        # Check for badges based on completion count
        if completed_count >= 5:
            # Find badge for completing 5 exercises in this section
            badge = Badge.query.filter_by(
                section_id=section.id, 
                points_required=50
            ).first()
            
            if badge and not UserBadge.query.filter_by(user_id=user.id, badge_id=badge.id).first():
                # Award badge
                user_badge = UserBadge()
                user_badge.user_id = user.id
                user_badge.badge_id = badge.id
                db.session.add(user_badge)
                db.session.commit()
    
    # Check for overall score badges
    high_scores = [r.score for r in user.practice_records 
                   if r.completed_at and r.score and r.score >= 7.0]
    
    if len(high_scores) >= 3:
        # Find badge for achieving high scores
        badge = Badge.query.filter_by(
            section_id=None,  # Overall badge
            points_required=200
        ).first()
        
        if badge and not UserBadge.query.filter_by(user_id=user.id, badge_id=badge.id).first():
            # Award badge
            user_badge = UserBadge()
            user_badge.user_id = user.id
            user_badge.badge_id = badge.id
            db.session.add(user_badge)
            db.session.commit()
            
def get_user_stats(user):
    """Get statistics for user dashboard"""
    # Get completed practice records
    completed_records = [r for r in user.practice_records if r.completed_at]
    
    # Get section data
    from models import Section
    section_data = {}
    
    for section in Section.query.all():
        section_records = [r for r in completed_records if r.exercise.section_id == section.id]
        avg_score = sum([r.score for r in section_records if r.score]) / max(1, len([r for r in section_records if r.score]))
        
        section_data[section.name] = {
            'completed': len(section_records),
            'average_score': avg_score if section_records else 0
        }
    
    # Calculate recent progress
    recent_records = sorted(completed_records, key=lambda r: r.completed_at or datetime.min, reverse=True)[:5]
    
    return {
        'total_completed': len(completed_records),
        'section_data': section_data,
        'recent_records': recent_records,
        'badges_earned': len(user.badges),
        'average_score': sum([r.score for r in completed_records if r.score]) / max(1, len([r for r in completed_records if r.score]))
    }
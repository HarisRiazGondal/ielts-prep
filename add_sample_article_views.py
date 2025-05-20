"""
Add sample article views to test analytics features
"""
import random
from datetime import datetime, timedelta
from app import create_app, db
from models import Article, User, ArticleView

def add_sample_views():
    """Add sample article views"""
    print("Adding sample article views...")
    app = create_app()
    
    with app.app_context():
        articles = Article.query.all()
        users = User.query.all()
        
        if not articles or not users:
            print("No articles or users found!")
            return
        
        # Clear existing views for testing
        ArticleView.query.delete()
        
        # Generate views over the last 30 days
        now = datetime.utcnow()
        start_date = now - timedelta(days=30)
        
        views_added = 0
        
        # For each day in the last 30 days
        for day_offset in range(30):
            day = start_date + timedelta(days=day_offset)
            
            # Number of views increases as we get closer to today
            daily_views = int(5 + day_offset * 0.5)
            
            for _ in range(daily_views):
                # Random article
                article = random.choice(articles)
                # Random user
                user = random.choice(users)
                # Random time during the day
                hour = random.randint(0, 23)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                timestamp = day.replace(hour=hour, minute=minute, second=second)
                
                # Create the view
                view = ArticleView(
                    article_id=article.id,
                    user_id=user.id,
                    viewed_at=timestamp
                )
                db.session.add(view)
                views_added += 1
        
        # Add more views to the first few articles to create distinct "popular" articles
        popular_articles = articles[:min(3, len(articles))]
        for article in popular_articles:
            extra_views = random.randint(15, 30) 
            for _ in range(extra_views):
                user = random.choice(users)
                days_ago = random.randint(0, 29)
                timestamp = now - timedelta(days=days_ago, 
                                          hours=random.randint(0, 23),
                                          minutes=random.randint(0, 59))
                
                view = ArticleView(
                    article_id=article.id,
                    user_id=user.id,
                    viewed_at=timestamp
                )
                db.session.add(view)
                views_added += 1
        
        db.session.commit()
        print(f"Added {views_added} sample article views.")

if __name__ == "__main__":
    add_sample_views() 
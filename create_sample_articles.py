import os
import sys
from datetime import datetime
from app import create_app, db
from models import Article, User, Section

# Sample article data
sample_articles = [
    {
        "title": "5 Effective Reading Strategies for IELTS",
        "category": "reading-tips",
        "summary": "Master these reading techniques to improve your IELTS score and save time during the exam.",
        "image_url": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1000&q=80",
        "content": """
# 5 Effective Reading Strategies for IELTS

The IELTS Reading section challenges many test-takers because of its time constraints and complex passages. Here are five proven strategies to help you improve your score:

## 1. Skim First, Read Later

Don't start by reading every word of the passage. Instead:

- Take 2-3 minutes to skim the passage
- Focus on headings, first sentences of paragraphs, and any bold/italicized text
- Get a general idea of the topic and structure before tackling the questions

This approach gives you a mental map of where information is located, saving precious time when answering specific questions.

## 2. Master the Art of Keyword Spotting

Exam questions often contain keywords that can be matched to the passage:

- Highlight key terms in the questions before reading closely
- Look for synonyms and paraphrases of these terms in the text
- Pay attention to names, dates, numbers, and specialized terminology

Remember that IELTS rarely uses exact word matches - they test your ability to recognize paraphrasing.

## 3. Don't Get Stuck on Difficult Questions

Time management is critical:

- Allocate about 20 minutes per passage
- If a question seems too challenging, mark it and move on
- Return to difficult questions after completing the easier ones

This ensures you have time to attempt all questions, maximizing your potential score.

## 4. Practice Careful Paragraph Selection

For questions that ask where specific information is located:

- Identify the key information required
- Scan for relevant paragraphs rather than reading the entire text
- Once located, read that section thoroughly to find the precise answer

This targeted approach saves time while maintaining accuracy.

## 5. Improve Your Vocabulary Systematically

A strong vocabulary is essential for the reading section:

- Study academic word lists specifically designed for IELTS
- Learn words in context rather than in isolation
- Pay attention to collocations (words that naturally go together)
- Use new vocabulary in your speaking and writing practice

Remember: consistent practice with timed conditions is key to success in the IELTS Reading section!
"""
    },
    {
        "title": "Writing Task 2: How to Structure Your Essay",
        "category": "writing-tips",
        "summary": "Learn the ideal structure for IELTS Writing Task 2 essays to improve your organization and coherence score.",
        "image_url": "https://images.unsplash.com/photo-1455390582262-044cdead277a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1000&q=80",
        "content": """
# Writing Task 2: How to Structure Your Essay

A well-structured essay is essential for achieving a high score in IELTS Writing Task 2. This guide will help you organize your ideas effectively.

## Introduction (40-60 words)

Your introduction should:

1. **Paraphrase the question** - Restate the topic in your own words
2. **Present your position** - Make your stance clear (if it's an opinion essay)
3. **Outline main points** - Briefly mention what you'll discuss in your body paragraphs

Example:
*The question of whether governments should invest in arts or focus solely on essential services is increasingly debated. While basic services are undeniably important, I believe that funding for arts and culture is also necessary for a well-functioning society. This essay will examine both the importance of essential services and the valuable contributions of the arts.*

## Body Paragraphs (2-3 paragraphs, 80-100 words each)

Each body paragraph should:

1. **Begin with a topic sentence** that clearly states the main idea
2. **Provide explanations** to develop your point
3. **Include specific examples** to support your argument
4. **Use linking words** to create coherence

### Body Paragraph Structure:
- **Point** - State your main argument
- **Explain** - Elaborate on why this point is valid
- **Example** - Provide a concrete example
- **Link** - Connect back to the question

Example:
*Essential public services form the foundation of a functioning society. Healthcare, education, and infrastructure are vital for citizens' wellbeing and economic development. For instance, countries with robust healthcare systems, such as Norway and Finland, consistently rank higher in quality of life indices. Without adequate funding for these basic services, communities would struggle to meet their fundamental needs.*

## Conclusion (40-50 words)

Your conclusion should:

1. **Summarize your main points** without adding new information
2. **Restate your position** (if applicable)
3. **Provide a final thought** or recommendation

Example:
*In conclusion, while governments must prioritize essential services, allocating reasonable funding to the arts creates a balanced society. The ideal approach would be a carefully considered budget that acknowledges both practical necessities and cultural enrichment.*

## Tips for Coherence and Cohesion

- Use a variety of linking words (however, furthermore, in addition)
- Use referencing words (this, these, such)
- Use paragraph transitions effectively
- Maintain a logical flow of ideas throughout the essay

Remember, practice is key to mastering this structure. Time yourself regularly and analyze model essays to improve your approach.
"""
    },
    {
        "title": "Active Listening: The Key to IELTS Success",
        "category": "listening-tips",
        "summary": "Develop active listening skills to improve your performance in the IELTS listening section.",
        "image_url": "https://images.unsplash.com/photo-1516223725307-6f76b9ec8742?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1000&q=80",
        "content": """
# Active Listening: The Key to IELTS Success

The IELTS Listening test evaluates your ability to understand spoken English in various contexts. Active listening—the practice of fully engaging with audio material—can significantly improve your performance.

## What is Active Listening?

Active listening involves:

- Concentrating fully on the audio
- Understanding the message
- Responding thoughtfully
- Remembering key information

Unlike passive listening, where you simply hear sounds, active listening requires mental engagement and strategic focus.

## Techniques for Active Listening in IELTS

### 1. Predict Content Before Listening

Before each section begins:

- Read the questions carefully
- Underline key words in the questions
- Predict likely answers and topics
- Anticipate vocabulary you might hear

This preparation activates relevant language in your mind and creates a framework for understanding.

### 2. Focus on Signpost Language

Speakers often use phrases that signal important information:

- "The most significant aspect is..."
- "There are three main reasons..."
- "In conclusion..."
- "However, on the other hand..."

These phrases highlight key points and transitions that often contain answers.

### 3. Listen for Specific Details

Train yourself to catch:

- Numbers and dates
- Names and places
- Spellings (especially in Section 1)
- Descriptive adjectives

Practice by listening to podcasts or interviews and writing down specific facts.

### 4. Recognize Distractors

The IELTS often includes information designed to mislead:

- Initial statements that are later corrected
- Similar-sounding options
- Information that partially matches the answer

Stay alert for phrases like "Actually..." or "On second thought..." which often signal a change in information.

### 5. Maintain Concentration

Sustained focus is essential:

- Practice listening for increasingly longer periods
- Eliminate distractions during practice sessions
- Take brief notes to stay engaged
- Visualize what you're hearing

## Practice Exercises for Active Listening

1. **Shadow speaking**: Listen to short clips and repeat what you hear verbatim
2. **Dictation practice**: Write down exactly what you hear, then check for accuracy
3. **Summarization**: Listen to a 2-3 minute clip and write a summary
4. **Note-taking practice**: Develop personal shorthand for quick notes during listening

Remember that active listening is a skill that improves with consistent practice. Dedicate time to these techniques, and you'll see improvement not only in your IELTS score but in your overall English communication abilities.
"""
    },
    {
        "title": "Speaking Part 2: Mastering the Long Turn",
        "category": "speaking-tips",
        "summary": "Strategies to excel in the IELTS Speaking Part 2 with a well-structured 2-minute response.",
        "image_url": "https://images.unsplash.com/photo-1543269865-cbf427effbad?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1000&q=80",
        "content": """
# Speaking Part 2: Mastering the Long Turn

Part 2 of the IELTS Speaking test - often called the "long turn" - requires you to speak for 1-2 minutes on a given topic card. This section can be challenging, but with proper structure and preparation, you can excel.

## Understanding the Format

In Speaking Part 2:

- You receive a task card with a topic and points to include
- You have one minute to prepare
- You need to speak for 1-2 minutes uninterrupted
- The examiner will stop you when the time is up

## The PREP Strategy for One-Minute Preparation

Make the most of your preparation time with the PREP approach:

### P - Points
- Quickly identify which points you'll cover
- Choose experiences or examples you know well
- Decide on a logical sequence

### R - Reasons/Results
- Think of reasons why this topic is significant
- Consider results or outcomes related to your experience
- Prepare to explain the "why" behind your points

### E - Examples
- Think of specific details to make your talk authentic
- Prepare personal anecdotes or specific situations
- Remember names, places, or dates if relevant

### P - Perspective
- Consider how to start and conclude your talk
- Think about your personal feelings/opinions
- Plan a final reflection or lesson learned

## Structuring Your 2-Minute Response

A clear structure helps you maintain fluency and coherence:

### Introduction (15-20 seconds)
- Rephrase the topic in your own words
- State your main idea or choice
- Give a brief overview of what you'll discuss

*Example: "I'd like to talk about my favorite teacher from high school, Mr. Johnson, who taught history. He had a profound impact on my academic development and even influenced my career choices later in life. I'll explain what made him special and why I still remember him so vividly."*

### Body (60-80 seconds)
- Cover each point from the cue card
- Expand with specific details
- Use a variety of descriptive language
- Connect ideas with appropriate linking words

*Example: "Mr. Johnson had an incredibly engaging teaching style. Rather than just focusing on dates and facts, he would tell historical events as captivating stories with characters and drama. For instance, when teaching us about World War II, he would assume the persona of different historical figures to present various perspectives..."*

### Conclusion (15-20 seconds)
- Summarize your main points
- Share a final thought or reflection
- Signal that you've finished

*Example: "In conclusion, Mr. Johnson stands out in my memory because he made learning an adventure rather than a chore. His creative teaching methods and genuine interest in his students' success set an example that I've tried to follow in my own career. He showed me that passion for a subject is contagious."*

## Common Pitfalls to Avoid

1. **Running out of things to say** - Practice expanding ideas with examples
2. **Speaking too fast** - Maintain a natural pace
3. **Using simple vocabulary** - Incorporate appropriate idiomatic expressions
4. **Monotonous intonation** - Vary your pitch and emphasis
5. **Going off-topic** - Regularly refer back to the cue card points

## Practice Technique: The 5-a-Day Method

Develop your Part 2 skills by:
- Preparing 5 different topics each day
- Recording your responses
- Listening and self-evaluating
- Focusing on one improvement area each time

With consistent practice and proper structure, the long turn can become one of your strongest sections in the IELTS Speaking test.
"""
    },
    {
        "title": "IELTS Vocabulary: Quality Over Quantity",
        "category": "vocabulary",
        "summary": "Learn how to effectively build and use vocabulary for higher IELTS scores across all sections.",
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1000&q=80",
        "content": """
# IELTS Vocabulary: Quality Over Quantity

Many IELTS candidates believe that memorizing thousands of words is the key to vocabulary success. However, the IELTS exam values how you use vocabulary more than how many words you know. This guide focuses on a quality-based approach to vocabulary development.

## Understanding Vocabulary Assessment in IELTS

The IELTS evaluates your vocabulary usage in several ways:

- **Range**: Using varied vocabulary appropriate to the topic
- **Precision**: Selecting the exact word that conveys your meaning
- **Naturalness**: Using collocations that sound native-like
- **Flexibility**: Adapting vocabulary to different contexts and purposes

## Focus Areas for Vocabulary Development

### 1. Academic Word List (AWL)

The Academic Word List contains 570 word families that appear frequently in academic texts. These words are particularly valuable for:

- Reading comprehension
- Writing Task 1 and 2
- Speaking Part 3 (abstract discussions)

**Study approach**: Learn 10 AWL words weekly, focusing on:
- Definition
- Word forms (noun, verb, adjective, adverb)
- Example sentences
- Common collocations

### 2. Topic-Specific Vocabulary

IELTS regularly features certain topics:

- Environment
- Education
- Technology
- Health
- Work and careers
- Social issues

For each topic, develop a vocabulary bank of:
- Key terms
- Useful phrases
- Topic-specific collocations

### 3. Collocations

Collocations are words that naturally occur together. Using them correctly makes your English sound more natural.

Examples:
- make a decision (not ~~take a decision~~)
- heavy rain (not ~~strong rain~~)
- deeply concerned (not ~~greatly concerned~~)

**Study approach**: Learn collocations in chunks rather than individual words.

### 4. Synonyms with Precision

Instead of using basic words repeatedly, learn precise alternatives:

| Basic Word | More Precise Alternatives |
|------------|---------------------------|
| Good       | beneficial, advantageous, favorable |
| Bad        | detrimental, adverse, unfavorable |
| Big        | substantial, significant, considerable |
| Small      | minimal, negligible, insignificant |

**Remember**: Choose synonyms based on context and connotation.

## Practical Vocabulary Building Strategies

### 1. Vocabulary Notebook System

Organize your vocabulary notebook by:
- Topic
- Word family
- Collocation patterns

For each entry, include:
- Definition
- Example sentence
- Pronunciation notes
- Personal association or memory aid

### 2. Contextual Learning

Learn words in context through:
- Reading IELTS-style articles
- Listening to academic podcasts
- Creating topic-based mind maps
- Writing practice essays using target vocabulary

### 3. Spaced Repetition

Review vocabulary using a spaced repetition system:
- Day 1: Initial learning
- Day 2: First review
- Day 4: Second review
- Day 7: Third review
- Day 14: Fourth review
- Monthly: Maintenance review

### 4. Active Use

Apply new vocabulary through:
- Speaking practice (record yourself)
- Writing sample sentences
- Explaining concepts to yourself
- Teaching words to others

## Common Vocabulary Pitfalls in IELTS

- **Overusing memorized phrases**: Examiners recognize scripted language
- **Misusing academic words**: Using formal vocabulary inappropriately
- **Neglecting collocations**: Creating unnatural word combinations
- **Ignoring connotation**: Choosing words with inappropriate tone

Remember: The IELTS rewards lexical resource that is accurate, appropriate, and natural. Focus on using words precisely rather than impressing with complexity.
"""
    },
]

def create_articles():
    """Create sample articles for the platform"""
    print("Creating sample articles...")
    app = create_app()
    
    with app.app_context():
        # Get admin user
        admin = User.query.filter_by(email='admin@ieltsapp.com').first()
        if not admin:
            print("Error: Admin user not found.")
            return
        
        for article_data in sample_articles:
            # Check if article already exists
            existing = Article.query.filter_by(title=article_data['title']).first()
            if existing:
                print(f"Article '{article_data['title']}' already exists.")
                continue
            
            # Get section if specified
            section = None
            if article_data.get('category') == 'reading-tips':
                section = Section.query.filter_by(name='Reading').first()
            elif article_data.get('category') == 'writing-tips':
                section = Section.query.filter_by(name='Writing').first()
            elif article_data.get('category') == 'listening-tips':
                section = Section.query.filter_by(name='Listening').first()
            elif article_data.get('category') == 'speaking-tips':
                section = Section.query.filter_by(name='Speaking').first()
            
            # Create new article
            article = Article(
                title=article_data['title'],
                content=article_data['content'],
                summary=article_data['summary'],
                image_url=article_data['image_url'],
                category=article_data['category'],
                author_id=admin.id,
                section_id=section.id if section else None,
                created_at=datetime.utcnow(),
                is_published=True
            )
            
            db.session.add(article)
        
        db.session.commit()
        print(f"Created {len(sample_articles)} sample articles.")

if __name__ == "__main__":
    create_articles() 
import json
import os
from app import app, db
from models import User, Role, Section, Difficulty, Exercise, Badge
from werkzeug.security import generate_password_hash
from datetime import datetime

def setup_database():
    """Set up the initial database schema and seed data"""
    # Set up proper database path
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'instance', 'ielts_prep.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)  # Ensure instance directory exists
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    
    with app.app_context():
        db.create_all()
        
        # Create roles if they don't exist
        if not Role.query.first():
            roles = [
                Role(name='admin', description='Administrator with full access'),
                Role(name='student', description='Regular student user')
            ]
            db.session.add_all(roles)
            db.session.commit()
            print("Created roles")
        
        # Create admin user if it doesn't exist
        admin_role = Role.query.filter_by(name='admin').first()
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                role_id=admin_role.id,
                first_name='Admin',
                last_name='User'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Created admin user")
        
        # Create sections if they don't exist
        if not Section.query.first():
            sections = [
                Section(name='Reading', description='IELTS Reading section tests your ability to understand written texts.'),
                Section(name='Writing', description='IELTS Writing section tests your ability to produce written responses.'),
                Section(name='Listening', description='IELTS Listening section tests your ability to understand spoken language.'),
                Section(name='Speaking', description='IELTS Speaking section tests your ability to communicate verbally.')
            ]
            db.session.add_all(sections)
            db.session.commit()
            print("Created sections")
        
        # Create difficulties if they don't exist
        if not Difficulty.query.first():
            difficulties = [
                Difficulty(name='Beginner', description='For those just starting IELTS preparation (Bands 4-5)'),
                Difficulty(name='Intermediate', description='For those with some IELTS experience (Bands 5.5-6.5)'),
                Difficulty(name='Advanced', description='For those aiming for high IELTS scores (Bands 7-9)')
            ]
            db.session.add_all(difficulties)
            db.session.commit()
            print("Created difficulties")
        
        # Create badges if they don't exist
        if not Badge.query.first():
            reading_section = Section.query.filter_by(name='Reading').first()
            writing_section = Section.query.filter_by(name='Writing').first()
            listening_section = Section.query.filter_by(name='Listening').first()
            speaking_section = Section.query.filter_by(name='Speaking').first()
            
            badges = [
                Badge(name='Reading Star', description='Complete 5 reading exercises', icon='fa-book', points_required=50, section_id=reading_section.id),
                Badge(name='Writing Master', description='Score 7+ on 3 writing tasks', icon='fa-pen', points_required=100, section_id=writing_section.id),
                Badge(name='Listening Expert', description='Complete 5 listening exercises', icon='fa-headphones', points_required=50, section_id=listening_section.id),
                Badge(name='Speaking Pro', description='Complete 5 speaking exercises', icon='fa-microphone', points_required=50, section_id=speaking_section.id),
                Badge(name='IELTS Champion', description='Score 7+ overall in a mock test', icon='fa-trophy', points_required=200)
            ]
            db.session.add_all(badges)
            db.session.commit()
            print("Created badges")
        
        # Create a reading exercise with data from "The world is our oyster" passage
        reading_section = Section.query.filter_by(name='Reading').first()
        intermediate_difficulty = Difficulty.query.filter_by(name='Intermediate').first()
        
        # Check if we already have the exercise
        existing_exercise = Exercise.query.filter_by(title='The World is Our Oyster').first()
        if not existing_exercise:
            # Prepare content for the reading exercise
            reading_content = {
                "passage": """
                <h3>The world is our oyster</h3>
                
                <p><strong>A.</strong> Independent travel is on the increase and while package holidays which offer an all-inclusive
                price for transport, accommodation and often even food are financially attractive to many,
                according to tourism analyst Thomas Cooper, an increasing number of people now prefer a
                less-tailored holiday and the freedom to make spur of the moment decisions and changes to
                their intended plan.</p>
                
                <p><strong>B.</strong> Internet based information sites about backpacking destinations are prolific and publications
                aimed at independent travellers on a budget exist for almost every destination imaginable.
                Some people, particularly first-time backpackers, may elect to travel with a friend or
                acquaintance; however, a large percentage of backpackers travel alone, assured by the
                knowledge that they are likely to meet, with ease, a number of like-minded individuals
                throughout their journey and staying in their backpacker accommodation. Alan Park, who has
                travelled extensively through Europe, Australasia and several other parts of the globe, says
                most accommodation establishments aimed at the backpacker market are designed with
                communal kitchens, dormitories and entertainment areas which lend themselves to allowing
                residents to socialize with ease and quickly breakdown barriers with strangers that may
                usually exist in day to day life.</p>
                
                <p><strong>C.</strong> Many backpackers of European origin are attracted to the Southern Hemisphere, Australia
                being a major destination of choice. Cooper attributes this high level of interest to the
                possibilities of legal working holiday visas for many nationalities and consequent short-term
                work opportunities making extended travel financially feasible, in addition to the attractive
                climate and outback appeal. Australia also has the reputation of being a relatively safe
                destination, with a warm and jovial population and its size and contrast between locations is
                alluring to many. University student Rebecca Thompson, who has just returned from a twelve
                month overseas trip, says that the cosmopolitan and modern nature of Australian cities such
                as Sydney and Melbourne contrasted with the rugged outback appeal of Western Australia
                and the Northern Territory, or the marine paradise of the Great Barrier Reef offer sufficient
                variation to attract a wide base of visitors. Sydney based travel consultant Brad Connor
                advises that it is also possible to obtain bargain deals on internal flights within this massive
                island when purchasing an international ticket, highly recommended, he says, for those who
                do not have the luxury of a long length of time, in order to ensure that key spots can be
                visited.</p>
                
                <p><strong>D.</strong> Equal in popularity to Australia, for the backpacking market is South East Asia and Rebecca
                Thompson says that, in her experience, the majority of travellers on extended trips to
                Australasia also include a visit to one or more South East Asia destinations in their itinerary.
                Thailand, in particular, has a long tourism history and well-established service industry. It is
                often considered one of the more accessible Asian destinations for the novice European
                backpacker due to its reasonable prices, large volume of Western visitors and well
                established backpacker trails. Brian Johnson, who is currently employed by the British
                Consulate in Bangkok, believes that the welcoming nature and level of English spoken by
                Thais involved in the tourism industry has also impacted positively on the destination's
                overseas image. Thai food is delicious and now fairly familiar to those outside the country
                and while precautions such as drinking bottled water and washing of fruit and vegetables
                should be practiced, generally standards of accommodation and restaurants are high.
                Thomas Cooper says Thailand's attractions are wide ranging, encompassing idyllic beaches,
                an insight into Buddhist culture and impressive ancient temples, mountain trekking, a vibrant
                nightlife and for bargain hunters bustling night markets and bazaars.</p>
                
                <p><strong>E.</strong> South East Asia neighbour, Vietnam, alongside its rapidly developing economy has also over
                recent years established a solid tourism industry, the majority of visitors entering and exiting
                by plane via its urban centres Ho Chi Minh (formerly Saigon) in the south and Hanoi in the
                north. Vietnam offers incredible vistas and contrasts of rugged mountain areas, lush green
                rice paddies, crystal clear waters and dense forest areas. Alan Park, who spent a month
                travelling independently around the country, says bus and rail networks allow visitors to
                travel from centre to centre relatively inexpensively, though he does not recommend these
                forms of transport to visitors on a short time-frame as the pace is unhurried.</p>
                
                <p><strong>F.</strong> The list of potentially safe and enjoyable backpacking destinations is endless. Technology
                and transport developments over recent time have resulted in more areas of the world
                becoming increasingly accessible, it is now possible to keep in regular contact with friends
                and family back home via email or even mobile phone, providing added reassurance to those
                concerned about travelling and their worried parents. Brian Johnson says friends, family and
                acquaintances who have previously travelled to the destination of choice are a useful source
                of first-hand advice and information and Simon Hartwell of the Backpackers Association
                adds travellers are advised to ensure that they are aware of visa requirements for their
                destination and are urged to seek medical advice regarding any necessary vaccinations or
                medical precautions. It is always wise to be as well informed as possible prior to embarking
                on a trip.</p>
                
                <p><strong>G.</strong> The youth of today are undoubtedly becoming more adventurous, which Hartwell ascribes to
                higher disposable income in the developed world than were available to previous generations
                and also the fact that we can more easily familiarise ourselves with the unknown via the
                internet and other communication methods. Many travellers, particularly experienced
                backpackers, are keen to experience more obscure destinations well off the well-trodden
                backpacker trail.</p>
                """,
                "questions": [
                    {
                        "text": "Opportunities to fund expenses through casual work increase the volume of visitors to a particular destination.",
                        "type": "matching",
                        "options": ["Simon Hartwell", "Brian Johnson", "Thomas Cooper", "Rebecca Thompson"]
                    },
                    {
                        "text": "Attitude to the tourism industry of the local people has had a positive impact on visitor numbers.",
                        "type": "matching",
                        "options": ["Simon Hartwell", "Brian Johnson", "Thomas Cooper", "Rebecca Thompson"]
                    },
                    {
                        "text": "Diverse attractions mean a destination is able to appeal to a wider range of people.",
                        "type": "matching",
                        "options": ["Simon Hartwell", "Brian Johnson", "Thomas Cooper", "Rebecca Thompson"]
                    },
                    {
                        "text": "Motivations for different approaches to travel by different generations.",
                        "type": "matching",
                        "options": ["Simon Hartwell", "Brian Johnson", "Thomas Cooper", "Rebecca Thompson"]
                    },
                    {
                        "text": "Interaction with others is generally more difficult when travelling alone than in normal life situations.",
                        "type": "true_false_not_given"
                    },
                    {
                        "text": "Travelling by plane to other domestic destinations in Australia is cheaper than other forms of transport.",
                        "type": "true_false_not_given"
                    },
                    {
                        "text": "Train travel in Vietnam can be too time-consuming for short visits.",
                        "type": "true_false_not_given"
                    },
                    {
                        "text": "Experienced backpackers rarely travel to destinations such as Australia.",
                        "type": "true_false_not_given"
                    },
                    {
                        "text": "Vietnam - tourism industry growing as is its _______.",
                        "type": "fill_blank"
                    },
                    {
                        "text": "Thailand - certain _______ are advisable - e.g. wash fruit.",
                        "type": "fill_blank"
                    },
                    {
                        "text": "Australia - Great Barrier Reef can be described as a _______.",
                        "type": "fill_blank"
                    }
                ],
                "answers": {
                    "q1": "Thomas Cooper",
                    "q2": "Brian Johnson",
                    "q3": "Rebecca Thompson",
                    "q4": "Simon Hartwell",
                    "q5": "False",
                    "q6": "Not Given",
                    "q7": "True",
                    "q8": "False",
                    "q9": "economy",
                    "q10": "precautions",
                    "q11": "marine paradise"
                }
            }
            
            # Create the exercise
            ielts_reading_exercise = Exercise(
                title='The World is Our Oyster',
                description='IELTS Reading practice on travel and tourism, focused on backpacking destinations.',
                section_id=reading_section.id,
                difficulty_id=intermediate_difficulty.id,
                content=json.dumps(reading_content),
                duration=20,  # 20 minutes
                points=50,
                is_mock_test=True
            )
            
            db.session.add(ielts_reading_exercise)
            db.session.commit()
            print("Created reading exercise 'The World is Our Oyster'")

if __name__ == '__main__':
    setup_database()
    print("Database setup complete!")
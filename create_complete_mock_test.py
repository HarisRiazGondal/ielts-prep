import json
from app import app, db
from models import Section, Difficulty, Exercise
from datetime import datetime

def create_complete_mock_test():
    """Create a complete IELTS Reading mock test with three passages"""
    with app.app_context():
        # Get the reading section and intermediate difficulty
        reading_section = Section.query.filter_by(name='Reading').first()
        intermediate_difficulty = Difficulty.query.filter_by(name='Intermediate').first()
        
        if not reading_section or not intermediate_difficulty:
            print("ERROR: Required section or difficulty not found")
            return
        
        # Check if we already have the complete mock test
        existing_exercise = Exercise.query.filter_by(title='IELTS Reading Full Mock Test 1').first()
        if existing_exercise:
            print("Complete mock test already exists. Skipping.")
            return
        
        # Prepare content for the complete reading mock test with three passages
        reading_content = {
            "passage1": """
            <h3>Passage 1: The World is Our Oyster</h3>
            
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
            "passage2": """
            <h3>Passage 2: An Aviation Wonder and its Creator</h3>
            
            <p><strong>A.</strong> The Supermarine Spitfire was a single-seater fighter plane used by the British Royal Airforce and
            pilots from a number of the country's allies during the Second World War. The first flight of a
            Spitfire prototype was on 5 March 1936 and usage of the plane continued until the 1950s. It was
            said to be one of the most effective fighter planes available during that period and was produced
            by Vickers-Armstrongs, a British engineering corporation which was formed in 1927 as a result of
            the merger of Vickers Limited and Sir W G Armstrong Whitworth & Company.</p>
            
            <p><strong>B.</strong> The Spitfire was designed by aeronautical engineer Reginald Joseph Mitchell. His career began
            when he joined a locomotives engineering company in 1911 at the age of 16. However, in 1917 he
            moved from his home town to join the Supermarine Aviation works in Southampton and was
            promoted to Chief Designer within his first year of employment. By the time the company was
            taken over by Vickers-Armstrongs in 1928, Mitchell had held the post of Technical Director for a
            year; and his capabilities and contributions were deemed so significant Vickers-Armstrong made
            his continual employment for a five year period a condition of the purchase of the company.</p>
            
            <p><strong>C.</strong> In the fifteen years prior to 1936 Mitchell designed 24 aircraft of differing categories including
            fighter planes, bombers and seaplanes. The first predecessor of the Spitfire in the fighter plane
            category to gain him national acclaim was the Supermarine S.B for which he won the Schneider
            Trophy (a cup and monetary award for technical advances in aviation which came to focus mainly
            on speed) in 1931. Despite withdrawal of financial support from the British Government that year,
            the Supermarine S.B. was able to compete for the Schneider Trophy as a result of a private
            donation of 100,000 pounds. Mitchell's team won outright on September 13th their aircraft
            achieving a new world speed record of 606 km/h; within days the Supermarine S.B. went on to
            break its own newly achieved record when on the 29th of the same month it became the first
            aircraft ever to achieve speeds of over 400 miles per hour (640 kilometres) when it reached 407.5
            mph (640 kilometres per hour).</p>
            
            <p><strong>D.</strong> Reginald Joseph Mitchell was awarded a CBE in 1932 for his contributions to high speed flight.
            CBEs being awarded by the British Monarch and reserved to recognise individuals who have
            'fulfilled a conspicuous leading role in regional affairs, through achievement or service to the
            community, or making a highly distinguished, innovative contribution in his or her area of
            activity'. Mitchell's achievements with the Supermarine S.B. also prompted the Air Ministry to
            contract his company for design of a new fighter aircraft, despite the organisation's reputation
            being built predominantly on sea-plane and not fighter plane manufacturing.</p>
            
            <p><strong>E.</strong> The first type, the 224, was to prove unsuccessful and it was eventually rejected by the Royal Air
            Force due to unsatisfactory performance; however, private sponsorship enabled research,
            development and modifications which led to the creation of the Type 300 which would eventually
            become the Spitfire. Soon after the first flight of the Spitfire prototype (trial version) and prior to
            completion of all stages of its official trials, convinced by its potential, the British Royal Air Force
            ordered 310 models. With its smooth lines, load-bearing metal shell, and heavy eight-machine gun
            armament, the Spitfire was considered revolutionary. In 1938, the aircraft was first put into official
            service; however, Mitchell, who died from cancer in 1937 at the age of 42, was not to witness this
            or the extensive impact and longevity of use the aircraft would have. In total 20,351 spitfires of
            different versions were produced making it the most produced British aircraft of the Second
            World War.</p>
            
            <p><strong>F.</strong> After Mitchell's death, his former Chief Draughtsman Joe Smith took over the position of
            Technical Director and led the subsequent development of the Spitfire which would keep it at the
            forefront of aircraft technology while many other designs quickly became obsolete; 24 models of
            spitfire were designed along with many sub-variants containing different engine types and
            weapons configurations. The Spitfire was the only British fighter aircraft to be in continuous
            production before, during and after the Second World War. During the Battle of Britain, a major
            air campaign fought in the skies over the United Kingdom in 1940, the Hurricane, another aircraft
            used by the Royal Airforce, shouldered the burden of Britain's defence; however, the Spitfire units
            had a lower attrition rate and a higher victory-to-loss ratio than those flying Hurricanes because
            of the Spitfire's higher performance.</p>
            """,
            "passage3": """
            <h3>Passage 3: Nature's Most Violent Wind</h3>
            
            <p><strong>A.</strong> Tornadoes are one of the most destructive forces in nature, destroying countless lives
            and homes throughout history. A tornado is a violent, dangerous, rotating column of air
            that is in contact with both the surface of the earth and the base of a cumulonimbus
            cloud (also known as a thundercloud). The most violent tornadoes come from
            supercells, large severe thunderstorms. These tornadoes can cause fatalities and
            devastate neighbourhoods in seconds.</p>
            
            <p><strong>B.</strong> Most tornadoes take on the appearance of a narrow funnel, of approximately 100
            metres wide, which extends down from the rotating base of a thundercloud towards the
            earth. When a tornado touches the ground it kicks up dirt, debris and items that it
            has displaced to form a dirty, dark cloud around the funnel, making it more visible.
            The average tornado is a few dozen metres across, has winds of about 110 mph
            (approximately 180 kph), travels a few kilometres before dissipating, and causes
            minor but significant damage. Some tornadoes can be over 1.5 km wide and pack
            wind speeds in excess of 300 mph (480 kph) and stay on the ground for over 100 km.
            Tornadoes, while usually brief, can cause extensive damage to buildings due to the
            extreme nature of circular wind velocity.</p>
            
            <p><strong>C.</strong> Tornadoes have been observed on every continent except Antarctica. The United
            States has the most tornadoes of any country, with an average of over 1,200 per
            year. Tornadoes also frequently affect the Southern provinces of Canada, northern
            Mexico, Britain, Bangladesh, and parts of Argentina, southern Brazil, and South
            Africa. However, they can occur almost anywhere under suitable conditions. The
            most tornado-prone region of the world is the Midwestern United States and the
            Canadian prairies, known as Tornado Alley, where many tornadoes occur each year.
            There are no natural barriers such as mountains to slow down storms that begin to
            rotate.</p>
            
            <p><strong>D.</strong> For many years researchers believed that tornadoes formed primarily during the
            afternoon in the Midwestern United States. When tornadoes were reported in the
            morning, however, researchers knew that more information was needed about the
            frequency, location and time of tornado occurrences. In fact, today, tornadoes are
            known to occur at all times of day, and to have been documented at different times in
            different areas. For example, in the southern states of the United States, such as
            Arkansas, tornadoes tend to occur from 6 to 11 pm, while in the Midwestern United
            States, such as in Dakota, they tend to occur from 4 to 9 pm. Many Texas tornadoes
            occur between midnight and 1 am. Tornadoes also exhibit various strengths. F0 or EF0
            tornadoes are considered weak or 'gale' force. These have wind speeds of 65-85
            mph. F5 or EF5 tornadoes are considered the strongest with wind speeds of more
            than 200 mph.</p>
            
            <p><strong>E.</strong> The formation of a tornado is most likely when a storm system is being pumped by
            air from very different pressure and temperature levels. Tornadoes can be especially
            dangerous when they approach populated areas. Some of these deadly twisters have
            caused billions of dollars in property damage and claimed dozens, hundreds, and
            even thousands of lives. For example, the Tri-state Tornado of March 18, 1925,
            killed 695 people as it raced along at 60-73 mph (97-117 kph), cutting a 219-mile
            (352-km) path of destruction across Illinois, Indiana, and Missouri and causing
            between $1.4 and 1.9 billion worth of damage (if it happened in modern times). The
            deadliest tornado in history, the Bangladesh disaster of April 26, 1989, killed about
            1,300 people.</p>
            
            <p><strong>F.</strong> Researchers are now studying the evolution of supercell storms in more detail to
            better understand the dynamics of tornado formation. Using a technique called
            "storm chasing", researchers follow a developing tornado to collect data on
            wind speed and direction, temperature, pressure, and moisture around the tornado
            by releasing measuring devices into the tornados themselves. Doppler radar has also
            been used to remotely study the internal air flow patterns of supercell storms, the
            parent storms of tornadoes. Along with sophisticated computer modelling
            techniques, these data help meteorologists understand atmospheric processes and
            lead to more accurate severe weather forecasts. Doppler radar allows storms and
            precipitation to be seen from a remote distance and helps forecasters warn of
            impending serious thunderstorms or tornadoes. Authorities keep alert for storms
            that will most likely produce a major tornado and maintain a warning system that can
            give people up to 30 minutes in some cases to take shelter in special basements
            called 'storm cellars' or other places constructed to withstand high winds. This
            system has saved hundreds of lives.</p>
            
            <p><strong>G.</strong> Tornado researchers have determined that there is a strong correlation between
            urban versus rural casualties. People who live in urban areas tend to receive earlier
            warnings of coming tornadoes because of television and radio warnings, but also
            because tornado sirens in areas of dense population help to warn people to take
            shelter. In rural areas, there are not enough people to justify the cost of tornado
            sirens, which is typically from $15K up to $25K, to warn people about the dangers.
            Another problem is housing. In urban areas, the housing may be of higher quality.
            For example, in a mobile or manufactured home, the structure is obviously not built
            to the same standard as typical houses, and deaths from tornadoes are 15 to 20
            times more frequent in mobile homes than permanent structures. About half of all
            deaths in tornadoes occur in these settings. Mobile homes do not have enough wall
            strength to provide protection from a violent tornado, and 50% of major tornadoes
            directly hitting these homes will cause casualties.</p>
            """,
            "questions": [
                # PASSAGE 1 - QUESTIONS 1-11
                {
                    "text": "Opportunities to fund expenses through casual work increase the volume of visitors to a particular destination.",
                    "type": "matching",
                    "options": ["Simon Hartwell", "Brian Johnson", "Thomas Cooper", "Rebecca Thompson"],
                    "section": "passage1"
                },
                {
                    "text": "Attitude to the tourism industry of the local people has had a positive impact on visitor numbers.",
                    "type": "matching",
                    "options": ["Simon Hartwell", "Brian Johnson", "Thomas Cooper", "Rebecca Thompson"],
                    "section": "passage1"
                },
                {
                    "text": "Diverse attractions mean a destination is able to appeal to a wider range of people.",
                    "type": "matching",
                    "options": ["Simon Hartwell", "Brian Johnson", "Thomas Cooper", "Rebecca Thompson"],
                    "section": "passage1"
                },
                {
                    "text": "Motivations for different approaches to travel by different generations.",
                    "type": "matching",
                    "options": ["Simon Hartwell", "Brian Johnson", "Thomas Cooper", "Rebecca Thompson"],
                    "section": "passage1"
                },
                {
                    "text": "Interaction with others is generally more difficult when travelling alone than in normal life situations.",
                    "type": "true_false_not_given",
                    "section": "passage1"
                },
                {
                    "text": "Travelling by plane to other domestic destinations in Australia is cheaper than other forms of transport.",
                    "type": "true_false_not_given",
                    "section": "passage1"
                },
                {
                    "text": "Train travel in Vietnam can be too time-consuming for short visits.",
                    "type": "true_false_not_given",
                    "section": "passage1"
                },
                {
                    "text": "Experienced backpackers rarely travel to destinations such as Australia.",
                    "type": "true_false_not_given",
                    "section": "passage1"
                },
                {
                    "text": "Vietnam - tourism industry growing as is its _______.",
                    "type": "fill_blank",
                    "section": "passage1"
                },
                {
                    "text": "Thailand - certain _______ are advisable - e.g. wash fruit.",
                    "type": "fill_blank",
                    "section": "passage1"
                },
                {
                    "text": "Australia - Great Barrier Reef can be described as a _______.",
                    "type": "fill_blank",
                    "section": "passage1"
                },
                
                # PASSAGE 2 - QUESTIONS 12-22
                {
                    "text": "What age was Mitchell when he joined Supermarine Aviation?",
                    "type": "fill_blank",
                    "section": "passage2"
                },
                {
                    "text": "What was significant about the performance of the Supermarine S.B. on September 29th?",
                    "type": "fill_blank",
                    "section": "passage2"
                },
                {
                    "text": "How many models of Spitfire were designed after Mitchell's death?",
                    "type": "fill_blank",
                    "section": "passage2"
                },
                {
                    "text": "Mitchell was awarded a CBE for his contributions to sea-plane manufacturing.",
                    "type": "true_false_not_given",
                    "section": "passage2"
                },
                {
                    "text": "The Type 224 aircraft was rejected by the Royal Air Force.",
                    "type": "true_false_not_given",
                    "section": "passage2"
                },
                {
                    "text": "Mitchell lived to see the Spitfire put into official service.",
                    "type": "true_false_not_given",
                    "section": "passage2"
                },
                {
                    "text": "The Hurricane was considered more reliable than the Spitfire during the Battle of Britain.",
                    "type": "true_false_not_given",
                    "section": "passage2"
                },
                {
                    "text": "The Spitfire was the only British fighter plane in continuous production throughout World War II.",
                    "type": "true_false_not_given",
                    "section": "passage2"
                },
                {
                    "text": "The total number of Spitfires produced during the Second World War was:",
                    "type": "fill_blank",
                    "section": "passage2"
                },
                {
                    "text": "What is the passage primarily about?",
                    "type": "multiple_choice",
                    "options": [
                        "The development of the Spitfire aircraft and its designer",
                        "The history of British aviation during World War II",
                        "The competition between Spitfire and Hurricane aircraft",
                        "The technical specifications of fighter planes"
                    ],
                    "section": "passage2"
                },
                {
                    "text": "Mitchell's aviation career began at which company?",
                    "type": "multiple_choice",
                    "options": [
                        "Vickers Limited",
                        "Supermarine Aviation",
                        "Sir W G Armstrong Whitworth & Company",
                        "A locomotives engineering company"
                    ],
                    "section": "passage2"
                },
                
                # PASSAGE 3 - QUESTIONS 23-40
                {
                    "text": "What is the MAIN purpose of the first paragraph?",
                    "type": "multiple_choice",
                    "options": [
                        "To describe what a tornado is",
                        "To explain how tornadoes form",
                        "To compare tornadoes to other weather phenomena",
                        "To discuss the dangers of living in tornado areas"
                    ],
                    "section": "passage3"
                },
                {
                    "text": "According to the passage, what makes a tornado more visible when it touches the ground?",
                    "type": "multiple_choice",
                    "options": [
                        "The wider funnel that develops",
                        "The debris cloud that forms around it",
                        "The color change in the thundercloud",
                        "The lightning that occurs within it"
                    ],
                    "section": "passage3"
                },
                {
                    "text": "What is the average width of a tornado?",
                    "type": "multiple_choice",
                    "options": [
                        "A few dozen meters",
                        "About 100 meters",
                        "Over 1.5 kilometers",
                        "Not specified in the passage"
                    ],
                    "section": "passage3"
                },
                {
                    "text": "The passage states that Tornado Alley has frequent tornadoes because:",
                    "type": "multiple_choice",
                    "options": [
                        "It has more thunderstorms than other regions",
                        "The climate is especially hot and humid",
                        "There are no mountain barriers to stop rotating storms",
                        "It is more densely populated than other areas"
                    ],
                    "section": "passage3"
                },
                {
                    "text": "According to the passage, when do most tornadoes occur in the Midwestern United States?",
                    "type": "fill_blank",
                    "section": "passage3"
                },
                {
                    "text": "The Tri-state Tornado of 1925 killed how many people?",
                    "type": "fill_blank",
                    "section": "passage3"
                },
                {
                    "text": "The deadliest tornado in history occurred in which country?",
                    "type": "fill_blank",
                    "section": "passage3"
                },
                {
                    "text": "What technique do researchers use to collect data directly from a tornado?",
                    "type": "multiple_choice",
                    "options": [
                        "Doppler radar scanning",
                        "Computer modeling",
                        "Storm chasing",
                        "Satellite imaging"
                    ],
                    "section": "passage3"
                },
                {
                    "text": "Which of the following contributes to higher tornado casualties in rural areas?",
                    "type": "multiple_choice",
                    "options": [
                        "Lower quality housing",
                        "Longer warning times",
                        "More frequent tornadoes",
                        "Higher population density"
                    ],
                    "section": "passage3"
                },
                {
                    "text": "The majority of tornado casualties occur in what type of housing?",
                    "type": "fill_blank",
                    "section": "passage3"
                },
                {
                    "text": "Early warning systems can sometimes give people up to 30 minutes to take shelter.",
                    "type": "true_false_not_given",
                    "section": "passage3"
                },
                {
                    "text": "Most tornadoes in the United States occur in the morning.",
                    "type": "true_false_not_given",
                    "section": "passage3"
                },
                {
                    "text": "Tornadoes have been observed on all seven continents.",
                    "type": "true_false_not_given",
                    "section": "passage3"
                },
                {
                    "text": "The cost of tornado sirens is approximately $15,000-$25,000.",
                    "type": "true_false_not_given",
                    "section": "passage3"
                },
                {
                    "text": "About half of all tornado deaths occur in mobile homes.",
                    "type": "true_false_not_given",
                    "section": "passage3"
                },
                {
                    "text": "Most tornadoes have wind speeds of approximately 300 mph.",
                    "type": "true_false_not_given",
                    "section": "passage3"
                },
                {
                    "text": "Doppler radar helps forecasters predict serious storms.",
                    "type": "true_false_not_given",
                    "section": "passage3"
                },
                {
                    "text": "People in rural areas tend to receive earlier tornado warnings than those in urban areas.",
                    "type": "true_false_not_given",
                    "section": "passage3"
                }
            ],
            "answers": {
                # Passage 1 Answers
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
                "q11": "marine paradise",
                
                # Passage 2 Answers
                "q12": "22",
                "q13": "It was the first aircraft to exceed 400 mph",
                "q14": "24",
                "q15": "False",
                "q16": "True",
                "q17": "False",
                "q18": "False",
                "q19": "True",
                "q20": "20,351",
                "q21": "The development of the Spitfire aircraft and its designer",
                "q22": "A locomotives engineering company",
                
                # Passage 3 Answers
                "q23": "To describe what a tornado is",
                "q24": "The debris cloud that forms around it",
                "q25": "A few dozen meters",
                "q26": "There are no mountain barriers to stop rotating storms",
                "q27": "4 to 9 pm",
                "q28": "695",
                "q29": "Bangladesh",
                "q30": "Storm chasing",
                "q31": "Lower quality housing",
                "q32": "mobile homes",
                "q33": "True",
                "q34": "False",
                "q35": "False",
                "q36": "True",
                "q37": "True",
                "q38": "False",
                "q39": "True",
                "q40": "False"
            }
        }
        
        # Combine all passages into one HTML for the reading section
        combined_content = {
            "passage": f"""
            <div class="reading-passages">
                {reading_content['passage1']}
                <hr class="passage-divider my-5">
                {reading_content['passage2']}
                <hr class="passage-divider my-5">
                {reading_content['passage3']}
            </div>
            """,
            "questions": reading_content['questions'],
            "answers": reading_content['answers']
        }
        
        # Create the full mock test
        mock_test = Exercise()
        mock_test.title = 'IELTS Reading Full Mock Test 1'
        mock_test.description = 'Complete IELTS Academic Reading mock test with 3 passages and 40 questions. Time: 60 minutes.'
        mock_test.section_id = reading_section.id
        mock_test.difficulty_id = intermediate_difficulty.id
        mock_test.content = json.dumps(combined_content)
        mock_test.duration = 60  # 60 minutes for a full reading test
        mock_test.points = 150
        mock_test.is_mock_test = True
        
        db.session.add(mock_test)
        db.session.commit()
        print("Created full IELTS Reading mock test with 3 passages")

if __name__ == '__main__':
    create_complete_mock_test()
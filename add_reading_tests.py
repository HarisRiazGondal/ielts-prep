import json
from app import app, db
from models import Section, Difficulty, Exercise
from datetime import datetime

def add_reading_tests():
    """Add multiple reading tests from the IELTS PDF materials"""
    with app.app_context():
        # Get the reading section and intermediate difficulty
        reading_section = Section.query.filter_by(name='Reading').first()
        intermediate_difficulty = Difficulty.query.filter_by(name='Intermediate').first()
        
        if not reading_section or not intermediate_difficulty:
            print("ERROR: Required section or difficulty not found")
            return
        
        # Reading test 1: Aviation Wonder (already have test 1: The World is Our Oyster)
        create_aviation_test(reading_section, intermediate_difficulty)
        
        # Reading test 2: Bringing Up Children Bilingually
        create_bilingual_test(reading_section, intermediate_difficulty)
        
        print("Added multiple reading tests successfully!")

def create_aviation_test(reading_section, difficulty):
    """Create Aviation Wonder reading test"""
    
    # Check if we already have the exercise
    existing_exercise = Exercise.query.filter_by(title='An Aviation Wonder and its Creator').first()
    if existing_exercise:
        print("Aviation Wonder test already exists. Skipping.")
        return
    
    # Prepare content for the reading exercise
    reading_content = {
        "passage": """
        <h3>An Aviation Wonder and its Creator</h3>
        
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
        "questions": [
            {
                "text": "What is the passage primarily about?",
                "type": "multiple_choice",
                "options": [
                    "The development of the Spitfire aircraft and its designer",
                    "The history of British aviation during World War II",
                    "The competition between Spitfire and Hurricane aircraft",
                    "The technical specifications of fighter planes"
                ]
            },
            {
                "text": "Mitchell's aviation career began at which company?",
                "type": "multiple_choice",
                "options": [
                    "Vickers Limited",
                    "Supermarine Aviation",
                    "Sir W G Armstrong Whitworth & Company",
                    "A locomotives engineering company"
                ]
            },
            {
                "text": "What age was Mitchell when he joined Supermarine Aviation?",
                "type": "fill_blank"
            },
            {
                "text": "What was significant about the performance of the Supermarine S.B. on September 29th?",
                "type": "fill_blank"
            },
            {
                "text": "How many models of Spitfire were designed after Mitchell's death?",
                "type": "fill_blank"
            },
            {
                "text": "Mitchell was awarded a CBE for his contributions to sea-plane manufacturing.",
                "type": "true_false_not_given"
            },
            {
                "text": "The Type 224 aircraft was rejected by the Royal Air Force.",
                "type": "true_false_not_given"
            },
            {
                "text": "Mitchell lived to see the Spitfire put into official service.",
                "type": "true_false_not_given"
            },
            {
                "text": "The Hurricane was considered more reliable than the Spitfire during the Battle of Britain.",
                "type": "true_false_not_given"
            },
            {
                "text": "The Spitfire was the only British fighter plane in continuous production throughout World War II.",
                "type": "true_false_not_given"
            },
            {
                "text": "The total number of Spitfires produced during the Second World War was:",
                "type": "fill_blank"
            }
        ],
        "answers": {
            "q1": "The development of the Spitfire aircraft and its designer",
            "q2": "A locomotives engineering company",
            "q3": "22",
            "q4": "It was the first aircraft to exceed 400 mph",
            "q5": "24",
            "q6": "False",
            "q7": "True",
            "q8": "False",
            "q9": "False",
            "q10": "True",
            "q11": "20,351"
        }
    }
    
    # Create the exercise
    aviation_exercise = Exercise()
    aviation_exercise.title = 'An Aviation Wonder and its Creator'
    aviation_exercise.description = 'IELTS Reading practice about the Spitfire aircraft and its designer R.J. Mitchell.'
    aviation_exercise.section_id = reading_section.id
    aviation_exercise.difficulty_id = difficulty.id
    aviation_exercise.content = json.dumps(reading_content)
    aviation_exercise.duration = 20  # 20 minutes
    aviation_exercise.points = 50
    aviation_exercise.is_mock_test = True
    
    db.session.add(aviation_exercise)
    db.session.commit()
    print("Created reading exercise 'An Aviation Wonder and its Creator'")

def create_bilingual_test(reading_section, difficulty):
    """Create Bilingual Children reading test"""
    
    # Check if we already have the exercise
    existing_exercise = Exercise.query.filter_by(title='Bringing Up Children Bilingually').first()
    if existing_exercise:
        print("Bilingual Children test already exists. Skipping.")
        return
    
    # Prepare content for the reading exercise
    reading_content = {
        "passage": """
        <h3>Bringing Up Children Bilingually</h3>
        
        <p>Both my husband and I are bilingual, and we are determined to bring up our two-year-old daughter to speak both our languages in order to give her access to both our cultures.</p>
        
        <p>There are three major views on bilingual child-rearing. The first is that it is too early to expose children to more than one language at such an early age—that it's enough if they simply hear songs, rhymes, games and stories in a foreign language. But researchers suggest that linguistic awareness—i.e., the ability to think about language—emerges earlier in bilinguals than in monolinguals, which can only work in the child's favour.</p>
        
        <p>The second approach is for parents to speak to each other in the language of the broader community but to speak to the children in both languages from birth. For example, in a family where the mother speaks Portuguese and the father Greek, living in America, the parents communicate with each other in English but the mother speaks Portuguese to the daughter, while the father speaks Greek. In each case, they don't mix languages. Most researchers advocate maximum time spent with each language. But they emphasise the need for consistency, pointing out that in this approach an occasional weekend trip to visit extended family is far less important than daily conversation. They recommend that a special effort should be made to create situations (music lessons, a children's group, or a babysitter who speaks the language) which consistently expose the child to the parents' languages.</p>
        
        <p>The third approach is for the parents to speak to each other in one of their mother tongues, and speak to the child in that same language. The child is then obliged to communicate with the other parent in that parent's language. My husband and I have opted for a modified version of this approach: we speak to each other in English, because we met and socialised in that language. But our household language is also Greek, which my husband and I speak to our daughter.</p>
        
        <p>Both her father and I speak to her in Greek, unless we are in a situation involving English speakers. As we live in Greece, she naturally gets more exposure to Greek, but we bought her English books and CDs; we downloaded English children's stories, cartoons and nursery rhymes, and we have made it a habit to use them with her for about half an hour every evening. When she was a few months old, I would carry her in a baby sling and put on the headphones and choose among classical music, English and Greek music. Needless to say, she could not express a preference at that time. As we were in a country where she was sure to be exposed to Greek, we made an effort to give English a head start.</p>
        
        <p>Some of the stories we downloaded we read together—we both read to her, or we read them while she gradually fell asleep. When it comes to entertainment, she dances to anything, be it Greek or English (or even Italian, though we're not planning to teach her that language). We use a variety of didactic computer games, and she loves them all, even though she doesn't understand them for now. She's at the vocabulary-acquisition stage, but she's not yet absorbing very much grammar, although we try to expose her to a broad range of syntactical patterns.</p>
        
        <p>If she does say something to us in English we never correct her Greek or reply to her in Greek. Needless to say, we haven't tried to correct her English either, since we know she's just building her vocabulary in both languages, and she often mixes languages in the same sentence. But I try to take whatever word she used in one language, and use it in the other, but in context.</p>
        
        <p>The problem with mixed language sentences occurred early on. For instance, when she was about 15 months old she called a lemon a "kitron" (the Geek) and then said she liked "lemoni juice" (using the English word for 'juice' and the Greek for 'lemon'). So without commenting on it, I'd reply, saying "you like lemon juice", heavily emphasising the word 'lemon'. And then I'd point to a lemon and say, "this is a lemon" (in English) "and in Greek it's called a kitron". She soon sorted it out—by the time she was around 18 months old, the frequency of mixed sentences had fallen dramatically, although she did sometimes use the word order or give the intonation of one language while using the vocabulary of the other.</p>
        
        <p>To anyone interested in bringing up bilingual children, the key is patience. Don't expect immediate results. And I'd advise anyone who speaks more than one language to use them all with infants, since doing so gives them an advantage, not only in this increasingly globalised world, but also in their grasp of their own mother tongue.</p>
        """,
        "questions": [
            {
                "text": "The writer says that she and her husband are bringing up their daughter bilingually to",
                "type": "multiple_choice",
                "options": [
                    "enable her to interact with both parents equally",
                    "help her learn to speak both languages fluently",
                    "ensure she becomes familiar with their two cultures",
                    "make sure she has a wide vocabulary in both languages"
                ]
            },
            {
                "text": "What is the writer's attitude towards the first view of bilingual child-rearing described?",
                "type": "multiple_choice",
                "options": [
                    "She thinks it is a conservative approach",
                    "She believes it has some advantages",
                    "She thinks it is impractical in her situation",
                    "She disagrees with what it advocates"
                ]
            },
            {
                "text": "What does the writer say about the approach to bilingual child-rearing that she and her husband have chosen?",
                "type": "multiple_choice",
                "options": [
                    "It provides a good balance of the two languages",
                    "It is the one used by most bilingual families",
                    "It is a slightly adapted form of the third approach",
                    "It is the most suitable one for her circumstances"
                ]
            },
            {
                "text": "The writer mentions that when her daughter was very small,",
                "type": "multiple_choice",
                "options": [
                    "she was unable to distinguish between languages",
                    "she was able to show which music she preferred to listen to",
                    "a particular effort was made to ensure she heard English frequently",
                    "she learned to understand simple phrases in both languages"
                ]
            },
            {
                "text": "The writer says that at present her daughter",
                "type": "multiple_choice",
                "options": [
                    "is mainly learning new words rather than grammatical rules",
                    "is deliberately taught how various grammatical structures work",
                    "uses a variety of complex sentence structures",
                    "is careful about the choice of language she uses"
                ]
            },
            {
                "text": "The writer says that when her daughter uses English in a Greek context",
                "type": "multiple_choice",
                "options": [
                    "she does not indicate that she has noticed this",
                    "she corrects her daughter's use of language",
                    "she encourages her to continue speaking English",
                    "she repeats the sentence in Greek only"
                ]
            },
            {
                "text": "According to the writer, what was noticeable about her daughter's speech at 15 months?",
                "type": "multiple_choice",
                "options": [
                    "She sometimes confused the names of food items",
                    "She used elements of both languages in the same sentence",
                    "She applied Greek grammar to English words",
                    "She made vocabulary mistakes in both languages"
                ]
            }
        ],
        "answers": {
            "q1": "ensure she becomes familiar with their two cultures",
            "q2": "She disagrees with what it advocates",
            "q3": "It is a slightly adapted form of the third approach",
            "q4": "a particular effort was made to ensure she heard English frequently",
            "q5": "is mainly learning new words rather than grammatical rules",
            "q6": "she does not indicate that she has noticed this",
            "q7": "She used elements of both languages in the same sentence"
        }
    }
    
    # Create the exercise
    bilingual_exercise = Exercise()
    bilingual_exercise.title = 'Bringing Up Children Bilingually'
    bilingual_exercise.description = 'IELTS Reading practice about raising children to speak multiple languages.'
    bilingual_exercise.section_id = reading_section.id
    bilingual_exercise.difficulty_id = difficulty.id
    bilingual_exercise.content = json.dumps(reading_content)
    bilingual_exercise.duration = 20  # 20 minutes
    bilingual_exercise.points = 50
    bilingual_exercise.is_mock_test = True
    
    db.session.add(bilingual_exercise)
    db.session.commit()
    print("Created reading exercise 'Bringing Up Children Bilingually'")

if __name__ == '__main__':
    add_reading_tests()
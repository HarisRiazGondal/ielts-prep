import json
from app import app, db
from models import Exercise, Section, Difficulty
from datetime import datetime

def create_mock_reading_test():
    """Create a complete IELTS reading mock test with 3 passages"""
    with app.app_context():
        # Get the reading section and a difficulty level
        reading_section = Section.query.filter_by(name='Reading').first()
        advanced_difficulty = Difficulty.query.filter_by(name='Advanced').first()
        
        if not reading_section or not advanced_difficulty:
            print("Error: Section or Difficulty not found")
            return
        
        # Prepare the content for the mock test
        reading_content = {
            "passages": {
                "passage1": """
                <h3>The Science of Sleep</h3>
                
                <p>We spend about a third of our lives asleep, but most people have no idea what happens during this seemingly dormant state. Scientists are now beginning to understand that sleep is far from a passive process; rather, it's a dynamic state essential for a range of vital functions.</p>
                
                <p>Sleep can be broadly divided into two types: rapid eye movement (REM) and non-rapid eye movement (NREM). NREM sleep is further divided into three stages, N1 through N3, with N3 being the deepest sleep. Each stage serves different functions in physical and mental restoration. During a typical night, the brain cycles through these stages several times, with each cycle lasting approximately 90 minutes.</p>
                
                <p>NREM sleep, particularly the deep N3 stage, is when the body performs most of its physical repair and maintenance. Blood pressure drops, breathing becomes more regular, and blood supply to muscles increases, delivering extra oxygen and nutrients. Growth hormone levels peak during this phase, stimulating tissue growth and repair. This is why deep sleep is particularly important for children and adolescents, as well as for athletes recovering from physical exertion.</p>
                
                <p>REM sleep, on the other hand, is when most dreaming occurs. The brain becomes highly active—almost as active as when awake—while the body enters a state of temporary paralysis, preventing us from acting out our dreams. REM sleep is crucial for cognitive functions, including memory consolidation, learning, and creativity. Studies have shown that people deprived of REM sleep have difficulty remembering what they learned before falling asleep.</p>
                
                <p>Dr. Matthew Walker, a neuroscientist at the University of California, Berkeley, describes sleep as "the single most effective thing we can do to reset our brain and body health each day." His research has demonstrated that even a single night of inadequate sleep can impair the brain's ability to regulate emotions, leading to increased reactivity to negative stimuli and decreased ability to process positive experiences.</p>
                
                <p>Sleep also plays a critical role in immune function. During sleep, the immune system releases proteins called cytokines, which increase in production when you have an infection or inflammation. Sleep deprivation decreases the production of these protective cytokines, as well as infection-fighting antibodies and cells. This explains why people who don't get enough sleep are more likely to get sick after exposure to viruses such as the common cold.</p>
                
                <p>Perhaps most surprisingly, recent research has discovered that sleep is essential for brain waste clearance. During sleep, the space between brain cells increases, allowing toxic byproducts that accumulate during waking hours to be flushed away. Dr. Maiken Nedergaard, who led research into this system at the University of Rochester Medical Center, likens it to "a dishwasher that cleans the brain while we sleep." The implications of this finding are significant for understanding neurodegenerative conditions like Alzheimer's disease, which are characterized by the accumulation of toxic proteins in the brain.</p>
                
                <p>Despite the clear importance of sleep, modern society often treats it as a luxury rather than a necessity. The Centers for Disease Control and Prevention in the United States has declared insufficient sleep a public health epidemic, with an estimated one-third of adults regularly getting less than the recommended seven hours of sleep per night.</p>
                
                <p>The consequences of chronic sleep deprivation go beyond feeling tired. Studies have linked insufficient sleep to a range of health problems, including obesity, type 2 diabetes, cardiovascular disease, and compromised immune function. The mental health impact is equally severe, with sleep disturbances strongly associated with conditions such as depression and anxiety.</p>
                
                <p>The evidence is clear: sleep is not a passive state of unconsciousness but an active process essential for maintaining optimal physical and mental health. As our understanding of sleep continues to evolve, so too should our appreciation of its fundamental role in our overall well-being. Perhaps it's time we started giving our sleep the attention it deserves.</p>
                """,
                
                "passage2": """
                <h3>Urban Agriculture: The Future of Food Production?</h3>
                
                <p>As the global population continues to grow and urbanize, traditional agricultural systems face mounting challenges. Urban agriculture—the practice of cultivating, processing, and distributing food in or around urban areas—is emerging as a promising solution to enhance food security, improve nutrition, and create more sustainable cities.</p>
                
                <p>Urban agriculture takes many forms, from community gardens and rooftop farms to sophisticated vertical farming systems and hydroponic installations. What unifies these diverse approaches is their location within city environments and their aim to produce food for local consumption.</p>
                
                <p>The benefits of urban farming extend far beyond mere food production. By shortening the distance food travels from farm to table, urban agriculture reduces transportation emissions, decreases the need for packaging and refrigeration, and often results in fresher produce with a smaller carbon footprint. A study by the University of Michigan found that urban farms could reduce greenhouse gas emissions by up to 17 times compared to conventional farming systems when transportation and storage factors are considered.</p>
                
                <p>Urban farms also address food deserts—areas where access to affordable, healthy food is restricted or nonexistent. In Detroit, Michigan, once considered America's largest food desert, urban farming initiatives have transformed vacant lots into productive gardens, providing fresh produce in neighborhoods where grocery stores are scarce. Eastern Market, one of the city's most successful projects, now supports over 80 urban farms and gardens, supplying fresh food to local residents and restaurants.</p>
                
                <p>The social benefits of urban agriculture are equally significant. Community gardens often serve as gathering places that strengthen neighborhood bonds and promote community engagement. Research from Flinders University in Australia found that participants in community gardening programs reported improved mental health, reduced stress, and a greater sense of belonging. For immigrant communities, urban gardens can provide space to grow culturally significant foods that may be unavailable or expensive in local markets.</p>
                
                <p>Economically, urban agriculture creates jobs and entrepreneurial opportunities. In New York City, the Brooklyn Grange—the world's largest rooftop soil farms—employs full-time farmers and hosts an apprenticeship program while generating revenue through produce sales, events, and educational workshops. The economic viability of such operations demonstrates that urban agriculture can be more than just a community project; it can be a sustainable business model.</p>
                
                <p>Technological innovation is rapidly expanding the potential of urban food production. Vertical farming, which grows crops in stacked layers with controlled environment agriculture (CEA) technology, can produce yields up to 350 times greater than conventional farming, using 95% less water and no pesticides. Singapore's Sky Greens vertical farm produces one ton of vegetables every other day on just 3.65 hectares of land—productivity that would be impossible with traditional methods in such a space-constrained environment.</p>
                
                <p>Indoor farming technologies such as hydroponics (growing plants in nutrient-rich water rather than soil), aquaponics (combining fish farming with hydroponics), and aeroponics (growing plants in an air or mist environment) allow year-round production regardless of external weather conditions. AeroFarms in Newark, New Jersey, uses aeroponics to grow over 550 varieties of plants in a former steel mill, producing two million pounds of leafy greens annually while using 95% less water than field farming.</p>
                
                <p>Despite these promising developments, urban agriculture faces significant challenges. Land in cities is expensive and often contaminated from previous industrial use, requiring remediation before food production can begin. Zoning regulations frequently restrict agricultural activities in urban areas, though many cities are now updating policies to accommodate food production. The start-up costs for high-tech urban farming systems can be prohibitive, and some critics question whether the energy requirements for indoor farming are justified by the benefits.</p>
                
                <p>However, as climate change threatens traditional agricultural systems and urban populations continue to grow, the case for developing robust urban food production becomes increasingly compelling. By integrating agriculture into urban planning and design, cities can become not just consumers of food but producers, creating more resilient and sustainable food systems for the future.</p>
                """,
                
                "passage3": """
                <h3>The Enigma of the Voynich Manuscript</h3>
                
                <p>Hidden away in Yale University's Beinecke Rare Book & Manuscript Library lies one of history's most perplexing literary mysteries—the Voynich Manuscript. Named after Wilfrid Voynich, the Polish book dealer who acquired it in 1912, this illustrated codex defies understanding despite a century of intense study by linguists, cryptographers, and historians.</p>
                
                <p>The manuscript consists of approximately 240 pages of vellum, containing text written in an unknown script accompanied by elaborate illustrations of unidentifiable plants, astronomical diagrams, and scenes featuring human figures. Carbon dating has established that the vellum dates to the early 15th century (between 1404 and 1438), though this only confirms when the material was produced, not necessarily when the text was written.</p>
                
                <p>The illustrations provide the basis for dividing the manuscript into six sections: botanical, astronomical, biological, cosmological, pharmaceutical, and recipes. The botanical section contains drawings of over 100 plant species, none of which can be definitively identified as known plants. The astronomical pages feature circular diagrams, some with suns, moons, and stars, suggestive of astronomical or astrological content. Perhaps most bizarrely, the biological section contains images of small naked women bathing in green or brown liquid, sometimes connected by elaborate pipe systems.</p>
                
                <p>What makes the Voynich Manuscript particularly fascinating is its text. Written from left to right in an unknown script dubbed "Voynichese," the text shows patterns consistent with natural language, including word frequency distribution and regular morphological structure. However, it matches no known language, ancient or modern. The script consists of between 25 and 30 distinct characters, far fewer than most language systems, and appears to follow specific orthographic rules, such as certain characters appearing only at the beginning of words and others only at the end.</p>
                
                <p>Numerous theories have attempted to explain the manuscript's origins and content. One suggestion is that it contains a constructed language or a previously unknown natural language. Others propose it might be encoded text in a known language disguised through complex ciphers. Some scholars have even suggested it could be an elaborate hoax, though the complexity and internal consistency of the text argue against this.</p>
                
                <p>William Friedman, one of the 20th century's foremost cryptographers who helped break Japanese codes during World War II, spent decades studying the manuscript but was unable to decipher it. In 1969, the renowned cryptologist John Tiltman concluded that the text was either an unknown language or an unbreakable cipher. Modern computational linguistics approaches have fared no better at cracking the code.</p>
                
                <p>Historical detective work has established some facts about the manuscript's provenance. The earliest confirmed owner was Georg Baresch, a 17th-century alchemist from Prague, who sent a letter about it to the Jesuit scholar Athanasius Kircher in 1639. After Baresch's death, the manuscript passed to his friend Jan Marek Marci, who sent it to Kircher in 1666. The manuscript's trail then goes cold until Voynich purchased it from the Jesuit College at Villa Mondragone near Rome in 1912.</p>
                
                <p>In 2011, researchers analyzing the binding and covers determined they were added to the manuscript in the early 17th century, likely in Prague. A letter from Emperor Rudolf II of Bohemia, dated to the late 16th century and discovered inside the manuscript, suggested he had purchased it for 600 ducats, believing it to be the work of the 13th-century English monk Roger Bacon.</p>
                
                <p>Recent breakthrough claims have generated excitement but ultimately fallen short. In 2017, Nicholas Gibbs, a television writer and medievalist, proposed that the manuscript was a medical treatise based on antique sources. In 2018, Dr. Gerard Cheshire of the University of Bristol announced he had decoded the text as a proto-Romance language, claiming it was written by a Dominican nun as a reference for Maria of Castile, Queen of Aragon. Both theories were quickly dismissed by Voynich researchers due to methodological flaws.</p>
                
                <p>The Voynich Manuscript remains one of history's most enduring enigmas. Its resistance to decipherment despite modern computational methods suggests either a remarkably sophisticated encryption system or possibly a constructed language created for purposes we can only speculate about. Whatever its origins and purpose, it continues to captivate researchers and enthusiasts, a reminder that even in our age of information, some mysteries remain persistently beyond our grasp.</p>
                """
            },
            "questions": {
                "passage1": [
                    {
                        "number": 1,
                        "text": "According to the text, REM sleep is characterized by:",
                        "type": "multiple_choice",
                        "options": [
                            "Physical repair and tissue growth",
                            "Regular breathing and decreased blood pressure",
                            "High brain activity and temporary body paralysis",
                            "Brain waste clearance and detoxification"
                        ]
                    },
                    {
                        "number": 2,
                        "text": "Growth hormone levels peak during:",
                        "type": "multiple_choice",
                        "options": [
                            "REM sleep",
                            "N3 stage of NREM sleep",
                            "N1 stage of NREM sleep",
                            "The transition between sleep cycles"
                        ]
                    },
                    {
                        "number": 3,
                        "text": "The text compares the brain's waste clearance system during sleep to:",
                        "type": "fill_blank"
                    },
                    {
                        "number": 4,
                        "text": "Sleep is essential for memory consolidation.",
                        "type": "true_false_not_given"
                    },
                    {
                        "number": 5,
                        "text": "Deep sleep is more important for adults than for children.",
                        "type": "true_false_not_given"
                    },
                    {
                        "number": 6,
                        "text": "NREM sleep consists of four distinct stages.",
                        "type": "true_false_not_given"
                    },
                    {
                        "number": 7,
                        "text": "Dr. Matthew Walker describes sleep as...",
                        "type": "fill_blank"
                    },
                    {
                        "number": 8,
                        "text": "The Centers for Disease Control and Prevention considers insufficient sleep to be:",
                        "type": "multiple_choice",
                        "options": [
                            "A minor health concern",
                            "A public health epidemic",
                            "A natural part of modern life",
                            "Less important than diet and exercise"
                        ]
                    },
                    {
                        "number": 9,
                        "text": "During sleep, the space between brain cells decreases to prevent toxin buildup.",
                        "type": "true_false_not_given"
                    },
                    {
                        "number": 10,
                        "text": "The text suggests that sleep deprivation may be linked to neurodegenerative diseases like Alzheimer's.",
                        "type": "true_false_not_given"
                    },
                    {
                        "number": 11,
                        "text": "The recommended amount of sleep for adults is approximately:",
                        "type": "multiple_choice",
                        "options": [
                            "5 hours",
                            "6 hours",
                            "7 hours",
                            "9 hours"
                        ]
                    },
                    {
                        "number": 12,
                        "text": "According to the passage, cytokines are:",
                        "type": "multiple_choice",
                        "options": [
                            "Proteins released by the immune system",
                            "Toxins that build up during waking hours",
                            "Hormones that regulate sleep cycles",
                            "Brain cells that are activated during REM sleep"
                        ]
                    },
                    {
                        "number": 13,
                        "text": "Each sleep cycle lasts approximately ______ minutes.",
                        "type": "fill_blank"
                    }
                ],
                "passage2": [
                    {
                        "number": 14,
                        "text": "Urban agriculture can help address the problem of:",
                        "type": "multiple_choice",
                        "options": [
                            "Rural unemployment",
                            "Food deserts",
                            "Agricultural subsidies",
                            "International trade barriers"
                        ]
                    },
                    {
                        "number": 15,
                        "text": "According to the University of Michigan study, urban farms could reduce greenhouse gas emissions by up to:",
                        "type": "multiple_choice",
                        "options": [
                            "5 times",
                            "10 times",
                            "17 times",
                            "25 times"
                        ]
                    },
                    {
                        "number": 16,
                        "text": "The text mentions Eastern Market as an example of a successful urban farming project in:",
                        "type": "fill_blank"
                    },
                    {
                        "number": 17,
                        "text": "The Brooklyn Grange is described as:",
                        "type": "multiple_choice",
                        "options": [
                            "A community garden program",
                            "A vertical farming operation",
                            "The world's largest rooftop soil farm",
                            "A government-funded agricultural initiative"
                        ]
                    },
                    {
                        "number": 18,
                        "text": "Research from Flinders University found that community gardening improves participants' physical fitness.",
                        "type": "true_false_not_given"
                    },
                    {
                        "number": 19,
                        "text": "Urban agriculture can provide immigrants with access to culturally significant foods.",
                        "type": "true_false_not_given"
                    },
                    {
                        "number": 20,
                        "text": "According to the text, vertical farming can produce yields up to ______ times greater than conventional farming.",
                        "type": "fill_blank"
                    },
                    {
                        "number": 21,
                        "text": "Singapore's Sky Greens vertical farm produces one ton of vegetables:",
                        "type": "multiple_choice",
                        "options": [
                            "Daily",
                            "Every other day",
                            "Weekly",
                            "Monthly"
                        ]
                    },
                    {
                        "number": 22,
                        "text": "AeroFarms uses which farming technology?",
                        "type": "multiple_choice",
                        "options": [
                            "Hydroponics",
                            "Aquaponics",
                            "Aeroponics",
                            "Traditional soil farming"
                        ]
                    },
                    {
                        "number": 23,
                        "text": "The text states that all urban land requires remediation before food production can begin.",
                        "type": "true_false_not_given"
                    },
                    {
                        "number": 24,
                        "text": "The main challenge to urban agriculture mentioned in the passage is:",
                        "type": "multiple_choice",
                        "options": [
                            "Lack of consumer interest",
                            "High cost of urban land",
                            "Competition from traditional farms",
                            "Limited crop variety"
                        ]
                    },
                    {
                        "number": 25,
                        "text": "Urban agriculture can make cities both consumers and ______ of food.",
                        "type": "fill_blank"
                    },
                    {
                        "number": 26,
                        "text": "The text suggests that many cities are changing their zoning regulations to facilitate urban agriculture.",
                        "type": "true_false_not_given"
                    },
                    {
                        "number": 27,
                        "text": "According to the passage, which farming method uses fish as part of its system?",
                        "type": "fill_blank"
                    }
                ],
                "passage3": [
                    {
                        "number": 28,
                        "text": "The Voynich Manuscript is currently housed in:",
                        "type": "multiple_choice",
                        "options": [
                            "The British Library",
                            "Yale University's Beinecke Library",
                            "The Vatican Library",
                            "The Library of Congress"
                        ]
                    },
                    {
                        "number": 29,
                        "text": "Carbon dating has established that the Voynich Manuscript's vellum dates to between:",
                        "type": "multiple_choice",
                        "options": [
                            "1200 and 1250",
                            "1300 and 1350",
                            "1404 and 1438",
                            "1500 and 1550"
                        ]
                    },
                    {
                        "number": 30,
                        "text": "The manuscript is divided into six sections based on its:",
                        "type": "fill_blank"
                    },
                    {
                        "number": 31,
                        "text": "The text states that drawings in the biological section show women:",
                        "type": "multiple_choice",
                        "options": [
                            "Gathering herbs",
                            "Reading books",
                            "Bathing in colored liquid",
                            "Performing rituals"
                        ]
                    },
                    {
                        "number": 32,
                        "text": "The Voynich script contains between 25 and 30 distinct characters.",
                        "type": "true_false_not_given"
                    },
                    {
                        "number": 33,
                        "text": "William Friedman successfully deciphered parts of the manuscript.",
                        "type": "true_false_not_given"
                    },
                    {
                        "number": 34,
                        "text": "The earliest confirmed owner of the manuscript was:",
                        "type": "multiple_choice",
                        "options": [
                            "Roger Bacon",
                            "Athanasius Kircher",
                            "Georg Baresch",
                            "Emperor Rudolf II"
                        ]
                    },
                    {
                        "number": 35,
                        "text": "Emperor Rudolf II believed the manuscript was the work of:",
                        "type": "fill_blank"
                    },
                    {
                        "number": 36,
                        "text": "The manuscript's binding and covers were added in the early ______ century.",
                        "type": "fill_blank"
                    },
                    {
                        "number": 37,
                        "text": "Nicholas Gibbs proposed that the manuscript was:",
                        "type": "multiple_choice",
                        "options": [
                            "An alchemical treatise",
                            "A medical reference",
                            "A religious text",
                            "An astronomical guide"
                        ]
                    },
                    {
                        "number": 38,
                        "text": "Dr. Gerard Cheshire claimed the manuscript was written in a proto-Romance language by a Dominican nun.",
                        "type": "true_false_not_given"
                    },
                    {
                        "number": 39,
                        "text": "The Voynichese script is written from right to left.",
                        "type": "true_false_not_given"
                    },
                    {
                        "number": 40,
                        "text": "In what year did Wilfrid Voynich acquire the manuscript?",
                        "type": "fill_blank"
                    }
                ]
            },
            "answers": {
                "q1": "High brain activity and temporary body paralysis",
                "q2": "N3 stage of NREM sleep",
                "q3": "a dishwasher",
                "q4": "True",
                "q5": "False",
                "q6": "False",
                "q7": "the single most effective thing we can do to reset our brain and body health each day",
                "q8": "A public health epidemic",
                "q9": "False",
                "q10": "True",
                "q11": "7 hours",
                "q12": "Proteins released by the immune system",
                "q13": "90",
                "q14": "Food deserts",
                "q15": "17 times",
                "q16": "Detroit",
                "q17": "The world's largest rooftop soil farm",
                "q18": "Not Given",
                "q19": "True",
                "q20": "350",
                "q21": "Every other day",
                "q22": "Aeroponics",
                "q23": "False",
                "q24": "High cost of urban land",
                "q25": "producers",
                "q26": "True",
                "q27": "aquaponics",
                "q28": "Yale University's Beinecke Library",
                "q29": "1404 and 1438",
                "q30": "illustrations",
                "q31": "Bathing in colored liquid",
                "q32": "True",
                "q33": "False",
                "q34": "Georg Baresch",
                "q35": "Roger Bacon",
                "q36": "17th",
                "q37": "A medical reference",
                "q38": "True",
                "q39": "False",
                "q40": "1912"
            }
        }
        
        # Check if a similar test already exists
        existing_test = Exercise.query.filter_by(title='Complete IELTS Reading Mock Test').first()
        if existing_test:
            print("Advanced reading test already exists. Updating content...")
            existing_test.content = json.dumps(reading_content)
            existing_test.duration = 60  # 60 minutes
            db.session.commit()
            print(f"Updated existing test with ID {existing_test.id}")
            return existing_test.id
        else:
            # Create the new mock test
            advanced_reading_test = Exercise(
                title='Complete IELTS Reading Mock Test',
                description='A full IELTS Reading test with 3 passages and 40 questions to be completed in 60 minutes.',
                section_id=reading_section.id,
                difficulty_id=advanced_difficulty.id,
                content=json.dumps(reading_content),
                duration=60,  # 60 minutes
                points=100,
                is_mock_test=True
            )
            
            db.session.add(advanced_reading_test)
            db.session.commit()
            print(f"Created new advanced reading test with ID {advanced_reading_test.id}")
            return advanced_reading_test.id

if __name__ == '__main__':
    create_mock_reading_test()
    print("Mock test creation completed!") 
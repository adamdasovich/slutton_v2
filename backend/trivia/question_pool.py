"""
Large pool of trivia questions for daily rotation
"""

QUESTION_POOL = [
    # Lingerie History (20 questions)
    {
        "question_text": "What ancient civilization is credited with inventing lingerie?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Ancient Egypt", "B": "Ancient Rome", "C": "Ancient Greece", "D": "Ancient China"},
        "correct_answer": "A",
        "explanation": "Ancient Egyptians were the first to create decorative undergarments, often made from fine linen."
    },
    {
        "question_text": "In what year was Victoria's Secret founded?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "1965", "B": "1977", "C": "1982", "D": "1990"},
        "correct_answer": "B",
        "explanation": "Victoria's Secret was founded in 1977 by Roy Raymond in San Francisco."
    },
    {
        "question_text": "The modern bra was patented in which year?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "1889", "B": "1903", "C": "1914", "D": "1925"},
        "correct_answer": "C",
        "explanation": "Mary Phelps Jacob patented the first modern bra in 1914, made from two handkerchiefs and ribbon."
    },
    {
        "question_text": "The push-up bra was invented in which decade?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "1940s", "B": "1950s", "C": "1960s", "D": "1970s"},
        "correct_answer": "A",
        "explanation": "The push-up bra was invented in 1948 by Frederick Mellinger, founder of Frederick's of Hollywood."
    },
    {
        "question_text": "Who created the first underwire bra?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "Helene Weber", "B": "Mary Phelps Jacob", "C": "Herminie Cadolle", "D": "Frederick Mellinger"},
        "correct_answer": "A",
        "explanation": "Helene Weber designed the first underwire bra in the 1930s."
    },
    {
        "question_text": "When was the first thong bikini introduced?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "1950", "B": "1964", "C": "1974", "D": "1980"},
        "correct_answer": "C",
        "explanation": "The thong bikini was first introduced in 1974 by Brazilian designer Rudi Gernreich."
    },
    {
        "question_text": "What year did Agent Provocateur launch?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "1979", "B": "1984", "C": "1994", "D": "2001"},
        "correct_answer": "C",
        "explanation": "Agent Provocateur was founded in 1994 in London by Joseph Corré and Serena Rees."
    },
    {
        "question_text": "Who invented the sports bra?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Lisa Lindahl", "B": "Mary Phelps Jacob", "C": "Ida Rosenthal", "D": "Gabrielle Poisson"},
        "correct_answer": "A",
        "explanation": "Lisa Lindahl co-invented the sports bra (Jogbra) in 1977."
    },
    {
        "question_text": "What was the original name for a bra?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "Bust supporter", "B": "Breast bag", "C": "Chest warmer", "D": "Mammary supporter"},
        "correct_answer": "A",
        "explanation": "Early bras were called 'bust supporters' or 'bust improvers' in the early 1900s."
    },
    {
        "question_text": "When did La Perla open its first boutique?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "1948", "B": "1954", "C": "1963", "D": "1971"},
        "correct_answer": "B",
        "explanation": "Ada Masotti founded La Perla in Bologna, Italy in 1954."
    },

    # Materials & Fabrics (15 questions)
    {
        "question_text": "What is the most popular lingerie color worldwide?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Red", "B": "Black", "C": "White", "D": "Pink"},
        "correct_answer": "B",
        "explanation": "Black is the most popular lingerie color globally, known for its timeless elegance."
    },
    {
        "question_text": "The word 'lingerie' comes from which language?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Italian", "B": "Spanish", "C": "French", "D": "Latin"},
        "correct_answer": "C",
        "explanation": "Lingerie comes from the French word 'linge', meaning linen or washables."
    },
    {
        "question_text": "Which material is NOT commonly used in luxury lingerie?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Silk", "B": "Lace", "C": "Polyester", "D": "Satin"},
        "correct_answer": "C",
        "explanation": "Luxury lingerie typically uses natural materials like silk, lace, and satin rather than synthetic polyester."
    },
    {
        "question_text": "Which metal is most commonly used in bra underwires?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Aluminum", "B": "Steel", "C": "Copper", "D": "Titanium"},
        "correct_answer": "B",
        "explanation": "Steel is most commonly used for bra underwires due to its flexibility and durability."
    },
    {
        "question_text": "Which fabric is known as the 'queen of fabrics' in lingerie?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Cotton", "B": "Silk", "C": "Lace", "D": "Velvet"},
        "correct_answer": "B",
        "explanation": "Silk is called the 'queen of fabrics' for its luxurious feel and natural beauty."
    },
    {
        "question_text": "What is Chantilly lace named after?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "A designer", "B": "A French city", "C": "A royal family", "D": "A flower"},
        "correct_answer": "B",
        "explanation": "Chantilly lace is named after the town of Chantilly in France, where it originated."
    },
    {
        "question_text": "Which fabric is best for everyday comfort?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Polyester", "B": "Nylon", "C": "Cotton", "D": "Rayon"},
        "correct_answer": "C",
        "explanation": "Cotton is the most breathable and comfortable fabric for daily wear."
    },
    {
        "question_text": "What is modal fabric made from?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Cotton", "B": "Petroleum", "C": "Beech trees", "D": "Bamboo"},
        "correct_answer": "C",
        "explanation": "Modal is a semi-synthetic fabric made from beech tree pulp, known for its softness."
    },
    {
        "question_text": "Which lace is traditionally made with bobbin and pins?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "Alençon lace", "B": "Stretch lace", "C": "Chemical lace", "D": "Guipure lace"},
        "correct_answer": "A",
        "explanation": "Alençon lace is a needle lace made with bobbin and pins, originating from France."
    },
    {
        "question_text": "What percentage of spandex is typically in stretch lace?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "5-10%", "B": "15-20%", "C": "25-30%", "D": "35-40%"},
        "correct_answer": "A",
        "explanation": "Stretch lace typically contains 5-10% spandex for flexibility while maintaining structure."
    },

    # Styles & Terminology (20 questions)
    {
        "question_text": "What is a 'teddy' in lingerie terminology?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "A type of robe", "B": "A one-piece garment", "C": "A type of stocking", "D": "A bra style"},
        "correct_answer": "B",
        "explanation": "A teddy is a one-piece lingerie garment that combines a camisole and panty."
    },
    {
        "question_text": "What does 'décolletage' refer to?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "A type of fabric", "B": "The neckline/cleavage area", "C": "A lingerie brand", "D": "A fitting technique"},
        "correct_answer": "B",
        "explanation": "Décolletage refers to the low neckline of a garment that reveals the neck, shoulders, and cleavage."
    },
    {
        "question_text": "What is a 'babydoll' style?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "A tight bodysuit", "B": "A short, loose nightgown", "C": "A type of corset", "D": "A robe style"},
        "correct_answer": "B",
        "explanation": "A babydoll is a short, loose-fitting nightgown or negligee, typically with a hem above the knees."
    },
    {
        "question_text": "The term 'negligée' literally means what in French?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "Beautiful", "B": "Delicate", "C": "Neglected", "D": "Soft"},
        "correct_answer": "C",
        "explanation": "Negligée comes from the French verb 'négliger' meaning to neglect, referring to casual, informal attire."
    },
    {
        "question_text": "What is a 'balconette' bra?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Full coverage bra", "B": "Low-cut horizontal cup bra", "C": "Sports bra", "D": "Strapless bra"},
        "correct_answer": "B",
        "explanation": "A balconette bra has horizontal, low-cut cups that create a lifted 'balcony' effect."
    },
    {
        "question_text": "What does 'demi-cup' mean?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Full coverage", "B": "Half coverage", "C": "No coverage", "D": "Side coverage"},
        "correct_answer": "B",
        "explanation": "Demi-cup refers to a bra that covers about half to three-quarters of the breast."
    },
    {
        "question_text": "What is a 'bustier'?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "A type of panty", "B": "A form-fitting garment extending to hips", "C": "A robe", "D": "A stockings style"},
        "correct_answer": "B",
        "explanation": "A bustier is a form-fitting garment that extends from chest to hips or waist."
    },
    {
        "question_text": "What are 'garters' used for?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Holding up stockings", "B": "Adjusting bra straps", "C": "Tightening corsets", "D": "Decorative purposes only"},
        "correct_answer": "A",
        "explanation": "Garters are straps attached to a belt or garment that hold up stockings."
    },
    {
        "question_text": "What is a 'chemise'?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "A bra style", "B": "A loose-fitting slip dress", "C": "A panty style", "D": "A corset"},
        "correct_answer": "B",
        "explanation": "A chemise is a loose-fitting, slip-like dress typically made of silky fabric."
    },
    {
        "question_text": "What is a 'plunge bra' designed to do?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Maximize support", "B": "Create deep V neckline", "C": "Minimize appearance", "D": "Add padding"},
        "correct_answer": "B",
        "explanation": "A plunge bra has a deep V-shaped neckline for wearing with low-cut tops."
    },

    # Fit & Sizing (15 questions)
    {
        "question_text": "What percentage of women wear the wrong bra size?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "50%", "B": "60%", "C": "70%", "D": "80%"},
        "correct_answer": "D",
        "explanation": "Studies show that approximately 80% of women wear the wrong bra size."
    },
    {
        "question_text": "What is the average lifespan of a well-maintained bra?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "3-6 months", "B": "6-12 months", "C": "1-2 years", "D": "3-5 years"},
        "correct_answer": "B",
        "explanation": "A well-maintained bra typically lasts 6-12 months or about 180 wears before losing elasticity."
    },
    {
        "question_text": "How many bras should a woman own in rotation?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "2-3", "B": "4-5", "C": "6-8", "D": "10-12"},
        "correct_answer": "C",
        "explanation": "Experts recommend owning 6-8 bras in rotation to extend their lifespan."
    },
    {
        "question_text": "Where should most of a bra's support come from?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Shoulder straps", "B": "Band around torso", "C": "Underwire", "D": "Cups"},
        "correct_answer": "B",
        "explanation": "About 80% of a bra's support should come from the band, not the straps."
    },
    {
        "question_text": "How often should you replace your everyday bras?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Every 3 months", "B": "Every 6-12 months", "C": "Every 2 years", "D": "When they break"},
        "correct_answer": "B",
        "explanation": "Everyday bras should be replaced every 6-12 months as they lose elasticity."
    },
    {
        "question_text": "What happens if your band size is too large?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Too tight", "B": "Rides up your back", "C": "Straps fall down", "D": "Cups overflow"},
        "correct_answer": "B",
        "explanation": "If the band is too large, it rides up your back and provides inadequate support."
    },
    {
        "question_text": "On what setting should a new bra fit?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Tightest hook", "B": "Middle hook", "C": "Loosest hook", "D": "Any hook"},
        "correct_answer": "C",
        "explanation": "A new bra should fit on the loosest hook so you can tighten it as it stretches over time."
    },
    {
        "question_text": "What is 'sister sizing' in bra fitting?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "Buying matching sets", "B": "Swapping band and cup size", "C": "Sizing for twins", "D": "Comparing brands"},
        "correct_answer": "B",
        "explanation": "Sister sizing means going up in band size and down in cup size (or vice versa) for similar fit."
    },
    {
        "question_text": "How should bras ideally be washed?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Machine wash, tumble dry", "B": "Hand wash, air dry", "C": "Dry clean only", "D": "Machine wash, air dry"},
        "correct_answer": "B",
        "explanation": "Hand washing and air drying extends bra life and maintains shape and elasticity."
    },
    {
        "question_text": "What does the number in a bra size represent?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Cup size", "B": "Band size (underbust)", "C": "Weight", "D": "Bust size"},
        "correct_answer": "B",
        "explanation": "The number represents the band size, measured around the ribcage under the bust."
    },

    # Industry & Culture (20 questions)
    {
        "question_text": "Which country produces the most lingerie globally?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "France", "B": "USA", "C": "China", "D": "Italy"},
        "correct_answer": "C",
        "explanation": "China is the world's largest producer of lingerie, manufacturing over 70% of global supply."
    },
    {
        "question_text": "What is the global lingerie market worth approximately?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "$20 billion", "B": "$42 billion", "C": "$78 billion", "D": "$100 billion"},
        "correct_answer": "C",
        "explanation": "The global lingerie market is valued at approximately $78 billion as of 2023."
    },
    {
        "question_text": "Which city is known as the lingerie capital of France?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "Paris", "B": "Lyon", "C": "Marseille", "D": "Nice"},
        "correct_answer": "B",
        "explanation": "Lyon is known as the lingerie capital of France, with a rich textile history."
    },
    {
        "question_text": "What is the most expensive bra ever created worth?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "$1 million", "B": "$5 million", "C": "$15 million", "D": "$20 million"},
        "correct_answer": "C",
        "explanation": "Victoria's Secret's 'Heavenly Star Bra' (2001) was worth $15 million, featuring diamonds and gemstones."
    },
    {
        "question_text": "Which designer is famous for cone bras?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Jean Paul Gaultier", "B": "Christian Dior", "C": "Calvin Klein", "D": "Coco Chanel"},
        "correct_answer": "A",
        "explanation": "Jean Paul Gaultier designed the iconic cone bra worn by Madonna on her 1990 tour."
    },
    {
        "question_text": "When is National Lingerie Day in the US?",
        "question_type": "multiple_choice",
        "difficulty": "hard",
        "options": {"A": "April 10", "B": "June 15", "C": "August 5", "D": "October 20"},
        "correct_answer": "C",
        "explanation": "National Lingerie Day is celebrated on August 5th in the United States."
    },
    {
        "question_text": "What does 'athleisure lingerie' combine?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Athletic wear and lingerie", "B": "Leather and lace", "C": "Silk and cotton", "D": "Vintage and modern"},
        "correct_answer": "A",
        "explanation": "Athleisure lingerie combines athletic/sportswear elements with lingerie aesthetics."
    },
    {
        "question_text": "Which decade saw the 'bra burning' feminist movement?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "1940s", "B": "1960s", "C": "1980s", "D": "1990s"},
        "correct_answer": "B",
        "explanation": "The 1960s feminist movement included symbolic bra burning as protest against restrictive beauty standards."
    },
    {
        "question_text": "What is 'inclusive sizing' in lingerie?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "One size fits all", "B": "Wide range of sizes", "C": "Plus size only", "D": "Custom sizing"},
        "correct_answer": "B",
        "explanation": "Inclusive sizing means offering a wide range of sizes to accommodate diverse body types."
    },
    {
        "question_text": "Which brand pioneered the 'body positive' lingerie movement?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Victoria's Secret", "B": "Calvin Klein", "C": "Aerie", "D": "La Perla"},
        "correct_answer": "C",
        "explanation": "Aerie launched their #AerieREAL campaign in 2014, pioneering unretouched model photos."
    },

    # Fashion & Design (10 questions)
    {
        "question_text": "What is 'boudoir photography'?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Fashion photography", "B": "Intimate bedroom photography", "C": "Wedding photography", "D": "Product photography"},
        "correct_answer": "B",
        "explanation": "Boudoir photography is intimate, romantic photography typically featuring lingerie in bedroom settings."
    },
    {
        "question_text": "What color lingerie is traditionally worn at weddings?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Red", "B": "Black", "C": "White", "D": "Blue"},
        "correct_answer": "C",
        "explanation": "White or ivory lingerie is traditionally worn under wedding gowns."
    },
    {
        "question_text": "What is a 'bridal trousseau'?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Wedding dress", "B": "Collection of intimate apparel for bride", "C": "Flower arrangement", "D": "Wedding cake"},
        "correct_answer": "B",
        "explanation": "A trousseau is a bride's collection of clothing and lingerie for her wedding and honeymoon."
    },
    {
        "question_text": "Which color is considered most romantic for lingerie?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Black", "B": "White", "C": "Red", "D": "Pink"},
        "correct_answer": "C",
        "explanation": "Red is traditionally considered the most romantic and passionate lingerie color."
    },
    {
        "question_text": "What does 'vintage-inspired lingerie' typically feature?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Modern synthetics", "B": "High-waisted cuts and retro details", "C": "Athletic elements", "D": "Minimalist design"},
        "correct_answer": "B",
        "explanation": "Vintage-inspired lingerie features high-waisted cuts, garters, and retro styling from past eras."
    },
    {
        "question_text": "What is 'pin-up style' lingerie inspired by?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "1920s flappers", "B": "1940s-50s glamour models", "C": "1970s disco", "D": "1990s grunge"},
        "correct_answer": "B",
        "explanation": "Pin-up style is inspired by glamorous 1940s-50s models like Bettie Page."
    },
    {
        "question_text": "What is the purpose of a 'longline bra'?",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "options": {"A": "Extra shoulder coverage", "B": "Extended band to waist", "C": "Longer straps", "D": "Deeper cups"},
        "correct_answer": "B",
        "explanation": "A longline bra has an extended band that reaches down to or below the waist for extra support and smoothing."
    },
    {
        "question_text": "What is 'sheer lingerie'?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Completely opaque", "B": "See-through or translucent", "C": "Leather material", "D": "Metallic finish"},
        "correct_answer": "B",
        "explanation": "Sheer lingerie is made from see-through or translucent fabrics like mesh or fine lace."
    },
    {
        "question_text": "What are 'pasties' used for?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Nipple coverage", "B": "Hip padding", "C": "Waist cinching", "D": "Shoulder support"},
        "correct_answer": "A",
        "explanation": "Pasties are adhesive coverings used to cover nipples under sheer or backless clothing."
    },
    {
        "question_text": "What is a 'matching set' in lingerie?",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "options": {"A": "Two bras", "B": "Bra and panty in same style", "C": "Two panties", "D": "Bra and robe"},
        "correct_answer": "B",
        "explanation": "A matching set consists of a bra and panty made from the same fabric and design."
    },
]

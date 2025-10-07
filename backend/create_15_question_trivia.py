"""
Create sample trivia with 15 witty, sexy, sensual questions
"""
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slutton_backend.settings')
django.setup()

from trivia.models import DailyTrivia, TriviaQuestion

# Delete existing trivia for today
today = date.today()
DailyTrivia.objects.filter(date=today).delete()
print(f'Deleted existing trivia for {today}')

# Create new trivia
trivia = DailyTrivia.objects.create(
    date=today,
    theme="Seductive Secrets & Passionate History",
    description="Explore the witty, sensual, and intriguing world of adult knowledge with 15 captivating questions",
    is_active=True
)

questions_data = [
    # EASY QUESTIONS (10 points each)
    {
        'order': 1,
        'question_text': 'Which ancient civilization is credited with creating the Kama Sutra, the legendary guide to love and pleasure?',
        'question_type': 'multiple_choice',
        'difficulty': 'easy',
        'options': {
            'A': 'Ancient Egypt',
            'B': 'Ancient India',
            'C': 'Ancient Greece',
            'D': 'Ancient Rome'
        },
        'correct_answer': 'B',
        'explanation': 'The Kama Sutra was written in ancient India around 400 BCE by Vatsyayana. This Sanskrit text is far more than a manual on positions - it\'s a comprehensive guide to living a virtuous and pleasurable life, covering everything from courtship to the art of kissing.'
    },
    {
        'order': 2,
        'question_text': 'What flower, often associated with passion and romance, was said to be Aphrodite\'s favorite?',
        'question_type': 'multiple_choice',
        'difficulty': 'easy',
        'options': {
            'A': 'Rose',
            'B': 'Lily',
            'C': 'Orchid',
            'D': 'Tulip'
        },
        'correct_answer': 'A',
        'explanation': 'The rose has been the symbol of love since ancient times. According to Greek mythology, when Aphrodite emerged from sea foam, roses bloomed wherever she stepped. Red roses specifically symbolize passionate love, while white roses represent purity.'
    },
    {
        'order': 3,
        'question_text': 'True or False: Chocolate contains phenylethylamine, the same chemical the brain produces when falling in love.',
        'question_type': 'true_false',
        'difficulty': 'easy',
        'options': None,
        'correct_answer': 'True',
        'explanation': 'This is absolutely true! Phenylethylamine (PEA) is known as the "love chemical" because your brain releases it when you fall in love. Chocolate contains this compound, which is why it\'s often given as a romantic gift and why we crave it when we\'re feeling lonely.'
    },
    {
        'order': 4,
        'question_text': 'Which famous lover was known for documenting his numerous romantic conquests in detailed memoirs?',
        'question_type': 'multiple_choice',
        'difficulty': 'easy',
        'options': {
            'A': 'Don Juan',
            'B': 'Casanova',
            'C': 'Romeo',
            'D': 'Paris'
        },
        'correct_answer': 'B',
        'explanation': 'Giacomo Casanova (1725-1798) wrote a 12-volume autobiography detailing his adventures across Europe. His name has become synonymous with the art of seduction. Unlike the fictional Don Juan, Casanova was a real person who charmed his way through 18th-century high society.'
    },
    {
        'order': 5,
        'question_text': 'What is the scientific term for the study of kissing?',
        'question_type': 'multiple_choice',
        'difficulty': 'easy',
        'options': {
            'A': 'Osculation',
            'B': 'Philematology',
            'C': 'Labiology',
            'D': 'Smackerology'
        },
        'correct_answer': 'B',
        'explanation': 'Philematology is the scientific study of kissing. Research shows that kissing releases oxytocin (the bonding hormone), reduces stress, and can even boost your immune system. The average person spends about 20,160 minutes kissing in their lifetime!'
    },

    # MEDIUM QUESTIONS (15 points each)
    {
        'order': 6,
        'question_text': 'In Victorian England, lovers used the "language of flowers" to send secret messages. What did giving someone lavender signify?',
        'question_type': 'multiple_choice',
        'difficulty': 'medium',
        'options': {
            'A': 'Passionate love',
            'B': 'Distrust',
            'C': 'Devotion and virtue',
            'D': 'A secret affair'
        },
        'correct_answer': 'B',
        'explanation': 'Surprisingly, lavender meant distrust in the Victorian language of flowers! While today we associate lavender with relaxation and purity, Victorians used it to say "I don\'t trust you." Red roses meant love, yellow roses meant jealousy, and striped carnations meant "I cannot be with you."',
    },
    {
        'order': 7,
        'question_text': 'True or False: The ancient Romans held a festival called Lupercalia, which inspired modern Valentine\'s Day.',
        'question_type': 'true_false',
        'difficulty': 'medium',
        'options': None,
        'correct_answer': 'True',
        'explanation': 'Lupercalia was a wild fertility festival held every February 15th in ancient Rome. Men would sacrifice animals, then playfully whip women with the hides (believed to promote fertility). When Christianity spread, Pope Gelasius I replaced it with St. Valentine\'s Day, making it more... civilized.',
    },
    {
        'order': 8,
        'question_text': 'Which aphrodisiac food was once so prized that Montezuma reportedly consumed 50 cups of it daily before visiting his harem?',
        'question_type': 'multiple_choice',
        'difficulty': 'medium',
        'options': {
            'A': 'Wine',
            'B': 'Chocolate',
            'C': 'Oysters',
            'D': 'Honey'
        },
        'correct_answer': 'B',
        'explanation': 'Montezuma II, the Aztec emperor, was said to drink up to 50 cups of chocolate (xocolatl) daily from golden goblets before visiting his wives. The Aztecs believed chocolate gave them stamina and vigor. They weren\'t entirely wrong - chocolate contains compounds that boost mood and energy!',
    },
    {
        'order': 9,
        'question_text': 'What percentage of the human body is considered an erogenous zone, capable of sexual arousal when stimulated?',
        'question_type': 'multiple_choice',
        'difficulty': 'medium',
        'options': {
            'A': '25%',
            'B': '50%',
            'C': '75%',
            'D': '100%'
        },
        'correct_answer': 'D',
        'explanation': 'The entire body can be an erogenous zone! While certain areas (lips, neck, ears, etc.) are more sensitive due to higher concentrations of nerve endings, sexual arousal is deeply connected to the brain. Context, mood, and individual preference mean any part of the body can become sensual.',
    },
    {
        'order': 10,
        'question_text': 'True or False: The word "pornography" comes from the Greek words "porne" (prostitute) and "graphein" (to write).',
        'question_type': 'true_false',
        'difficulty': 'medium',
        'options': None,
        'correct_answer': 'True',
        'explanation': 'Absolutely correct! The term literally means "writing about prostitutes." It was first used in the 1800s to describe ancient Roman and Greek erotic art discovered in Pompeii. The word didn\'t become commonly used until the Victorian era when scholars needed a "respectable" term for such materials.',
    },

    # HARD QUESTIONS (20 points each)
    {
        'order': 11,
        'question_text': 'Which famous French courtesan inspired Alexandre Dumas fils\' novel "La Dame aux Camélias," later adapted into Verdi\'s opera "La Traviata"?',
        'question_type': 'multiple_choice',
        'difficulty': 'hard',
        'options': {
            'A': 'Madame de Pompadour',
            'B': 'Marie Duplessis',
            'C': 'La Belle Otero',
            'D': 'Émilienne d\'Alençon'
        },
        'correct_answer': 'B',
        'explanation': 'Marie Duplessis was a legendary Parisian courtesan who captivated high society in the 1840s. She died of tuberculosis at just 23, but not before inspiring Dumas (her former lover) to immortalize her as Marguerite Gautier. Her tragic life became the basis for one of opera\'s most beloved works.',
    },
    {
        'order': 12,
        'question_text': 'In Freudian psychology, what term describes the unconscious sexual desire a child feels toward the opposite-sex parent?',
        'question_type': 'multiple_choice',
        'difficulty': 'hard',
        'options': {
            'A': 'Electra Complex',
            'B': 'Oedipus Complex',
            'C': 'Both A and B',
            'D': 'Neither A nor B'
        },
        'correct_answer': 'C',
        'explanation': 'Both terms are correct! Freud\'s Oedipus Complex describes a boy\'s attachment to his mother, while Carl Jung later coined the Electra Complex for a girl\'s attachment to her father. While modern psychology largely dismisses these theories, they remain influential in understanding childhood development and adult relationships.',
    },
    {
        'order': 13,
        'question_text': 'True or False: The "G-spot" is named after gynecologist Ernst Gräfenberg, who first described it in 1950.',
        'question_type': 'true_false',
        'difficulty': 'hard',
        'options': None,
        'correct_answer': 'True',
        'explanation': 'Correct! German gynecologist Ernst Gräfenberg published research in 1950 about an erogenous zone on the anterior vaginal wall. The "Gräfenberg spot" (later shortened to G-spot) became widely known in the 1980s. However, its existence remains debated in medical circles, with some researchers suggesting it\'s part of the clitoral complex.',
    },
    {
        'order': 14,
        'question_text': 'Which 18th-century libertine novel, written by the Marquis de Sade, gave us the word "sadism"?',
        'question_type': 'multiple_choice',
        'difficulty': 'hard',
        'options': {
            'A': 'Justine',
            'B': 'The 120 Days of Sodom',
            'C': 'Philosophy in the Bedroom',
            'D': 'All of the above'
        },
        'correct_answer': 'D',
        'explanation': 'All three works contributed to the Marquis de Sade\'s infamous reputation! The term "sadism" (deriving pleasure from inflicting pain) comes directly from his name. De Sade spent 32 years in prisons and asylums for his writings and alleged crimes. His works explored the darkest corners of human desire and remain controversial today.',
    },
    {
        'order': 15,
        'question_text': 'What ancient contraceptive method involved women inserting crocodile dung mixed with honey into the vagina?',
        'question_type': 'multiple_choice',
        'difficulty': 'hard',
        'options': {
            'A': 'Ancient Egyptian method',
            'B': 'Ancient Chinese method',
            'C': 'Ancient Greek method',
            'D': 'Ancient Babylonian method'
        },
        'correct_answer': 'A',
        'explanation': 'Ancient Egyptians used this rather... pungent contraceptive around 1850 BCE! The acidic nature of crocodile dung supposedly killed sperm, while the sticky honey acted as a barrier. Other Egyptian methods included acacia leaves (which contain spermicidal lactic acid) and pessaries made from various animal dung. Thank goodness for modern medicine!',
    },
]

# Create questions
for q_data in questions_data:
    TriviaQuestion.objects.create(
        daily_trivia=trivia,
        **q_data
    )
    print(f"Created question {q_data['order']}: {q_data['question_text'][:60]}...")

print(f'\nCreated trivia game for {today}')
print(f'   Theme: {trivia.theme}')
print(f'   Questions: 15')
print(f'   Mix: 5 Easy (10pts), 5 Medium (15pts), 5 Hard (20pts)')
print(f'   Total possible score: 225 points')

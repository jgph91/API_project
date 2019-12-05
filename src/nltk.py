from nltk import download
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pymongo import MongoClient,ASCENDING
from src.mongo import connectCollection

# collections
db, messages = connectCollection('API', 'messages')


def get_text(id,field):
    '''Returns a string with the text of all the message 
    from the specified chat'''
    
    id = int(id)
    
    text_messages = messages.find({field: id})
    text = ''

    for e in text_messages:
        text += e['text']
    return text

def analyzer(text):
    '''Rates the specified text'''

    download('vader_lexicon')
    mood = SentimentIntensityAnalyzer().polarity_scores(text)

    return mood

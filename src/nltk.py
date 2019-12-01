from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pymongo import MongoClient,ASCENDING
from src.mongo import connectCollection

# collections
db, messages = connectCollection('API', 'messages')


def get_text(idChat):
    '''Returns a string with the text of all the message 
    from the specified chat'''
    
    idChat = int(idChat)
    text_messages = messages.find({'idChat': idChat}).sort('idMessage',ASCENDING)
    text = ''

    for e in text_messages:
        text += e['text']
    return text

def analyzer(text):
    '''Rates the specified text'''

    mood = SentimentIntensityAnalyzer().polarity_scores(text)

    return mood

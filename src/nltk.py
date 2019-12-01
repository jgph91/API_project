from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_text():
    '''Returns a string with the text of all the message 
    from the specified chat'''
    
    text_messages = messages.find({'idChat': idChat})
                            .sort('idMessage',ASCENDING))
    text = ''
    for e in text_messages:
        text += e['text']
    return text

def analyzer(text):
    '''Rates the specified text'''

    mood = SentimentIntensityAnalyzer().polarity_scores(text)

    return mood
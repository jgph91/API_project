from pymongo import MongoClient,ASCENDING
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from src.mongo import connectCollection
from src.nltk import analyzer,get_text


# collections
db, messages = connectCollection('API', 'messages')
db, users = connectCollection('API', 'users')

#functions
def get_users_mod():
    '''Get all the users and its ids'''

    return users.find({},{'_id': 0, 'idUser': 1,'userName': 1})

def get_messages_user(userName):
    '''Returns a string with the text of all the messages 
    from the specified user'''
    
    text_messages = messages.find({'userName': userName}).sort('idMessage',ASCENDING)
    text = ''

    for e in text_messages:
        text += e['text']
    return text

def similarities_matrix():
    '''Returns the similarities matrix'''

    #getting all users

    all_users = []
    get = list(get_users_mod())

    for i in range(len(get)):
        e = get[i]['userName']
        all_users.append(e)

    #getting all messages for each user

    user_messages = {}

    for e in all_users:
        
        userName = e
        text = get_messages_user(e)
        user_messages[userName] = text

    #rank for each user
    user_rank = {}

    for e in user_messages.keys():
        text = user_messages[e]
        rank = analyzer(text)
        user_rank[e] = rank

    #data frame containing the rate of each user
    df = pd.DataFrame(user_rank).T

    #similarities matrix
    return pd.DataFrame(1/(1 + squareform(pdist(df, 'euclidean'))),
                            index=df.index, columns=df.index)
    
def recommendations(userName,similarities):
    '''Return the 3 most similar users'''

    return similarities[userName].sort_values(ascending=False)[1:4]

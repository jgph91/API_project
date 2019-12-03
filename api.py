#!/usr/bin/python3

from pymongo import MongoClient,ASCENDING
from bottle import request, response, post, get, run, route
from bson.json_util import dumps
import requests
import os
import json
from src.mongo import connectCollection, stop_existence, stop_not_existence,get_name
from src.nltk import analyzer,get_text
from src.recommender import get_users_mod, get_messages_user, similarities_matrix,recommendations



# collections
db, chats = connectCollection('API', 'chats')
db, users = connectCollection('API', 'users')
db, messages = connectCollection('API', 'messages')

@route('/')
def main():
    return 'Welcome to my first API! Check my repo in:https://github.com/jgph91/API_project'

# users endpoints
@post('/users/create')
def user_creator():
    '''Create a user and save into DB'''

    #text entered via params
    dict(request.forms)
    userName = request.forms.get('userName')
    # user can't be already created
    stop_existence(userName,'userName', users) 
    
    #assigning a new id
    new_id = users.distinct("idUser")[-1] + 1
    db.users.insert_one({'idUser': new_id,
                        'userName': userName})

    return (f'Welcome {userName}!. Your id is {new_id}')

@get('/users')
def get_users():
    '''Get all the users and its ids'''

    return dumps(users.find({},
                            {'_id': 0, 'idUser': 1,
                            'userName': 1}))

@get('/users/<userName>')
def get_userid(userName):
    '''Get the user id for the user name specified'''

    # user must be already created
    stop_not_existence(userName, 'userName', users)

    return dumps(users.find({'userName': userName},
                            {'_id': 0, 'idUser': 1,
                            'userName': 1}))

@get('/users/<idUser>/sentiment')
def mood_analyzer_user(idUser):
    '''Analyze messages from an user using NLTK's sentiment.'''

    # user must be already created
    stop_not_existence(idUser,'idUser', users)
    
    text = get_text(idUser,'idUser')
    
    mood = analyzer(text)
    
    return mood

@get('/users/<userName>/recommend')
def user_recommender(userName):
    '''Return the 3 most similar users'''
    
    # user must exist in the collection 
    stop_not_existence(userName, 'userName', users)

    similarities = similarities_matrix()
    top3 = recommendations(userName,similarities)
    top3 = top3.to_json()
    return top3

# chat endpoints
@get('/chat/create')
def chat_creator():
    '''Create a conversation to load messages'''
    idChat = chats.distinct("idChat")[-1] + 1
    db.chats.insert_one({'idChat': idChat})

    return (f'Chat created, the id is {idChat}.')

@post('/messages/<idChat>/<idUser>/addmessage')
def add_message(idChat, idUser):
    '''Add a message to the conversation.'''

    # user must be already created
    stop_not_existence(idUser,'idUser', users)
    # chat must be already created
    stop_not_existence(idChat,'idChat', chats)

    dict(request.forms)
    #text entered via params
    datetime = request.forms.get('datetime')
    text = request.forms.get('text')

    #getting the user name from the users collection
    userName = get_name(idUser)
    
    new_id = messages.distinct("idMessage")[-1] + 1
    messages.insert_one({'idUser': int(idUser),'userName': userName,
                        'idMessage':new_id,'idChat':int(idChat),
                        'datetime':datetime,'text':text})
    
    return ('Your message has been inserted sucessfully!')

@get('/messages/chat/<idChat>')
def get_messages(idChat):
    '''Get all messages from the specified chat'''

    idChat = int(idChat)
    # chat must be already created
    stop_not_existence(idChat,'idChat', chats)

    return dumps(messages.find({'idChat': idChat},
                            {'idChat':1,'datetime':1,'_id':0,
                            'userName':1,'idMessage':1,'text':1})
                            .sort('idMessage',ASCENDING))

@get('/messages/user/<idUser>')
def get_messages(idUser):
    '''Get all messages from the specified chat'''

    idUser = int(idUser)
    # user must exist in the collection 
    stop_not_existence(idUser,'idUser', users)

    return dumps(messages.find({'idUser': idUser},
                            {'datetime':1,'_id':0,
                            'idChat':1,'userName':1,
                            'idMessage':1,'text':1})
                            .sort('idMessage',ASCENDING))

@get('/chat/<idChat>/sentiment')
def mood_analyzer(idChat):
    '''Analyze messages for a chat using NLTK's sentiment.'''

    text = get_text(idChat,'idChat')
    mood = analyzer(text)
    
    return mood

#run(host='localhost', port=8080, debug=True)

port = int(os.getenv("PORT", 8080))
print(f"Running server {port}....")
run(host="0.0.0.0", port=port, debug=True)


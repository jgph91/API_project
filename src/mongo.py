from pymongo import MongoClient
import getpass
import json
import os
import re

# Get Password
password = getpass.getpass("Insert your AtlasMongoDB root password: ")
connection = 'mongodb+srv://root:{}@cluster0-rad7h.mongodb.net/test?retryWrites=true&w=majority'.format(
    password)

# Connect to DB
client = MongoClient(connection)

def connectCollection(database, collection):
    db = client[database]
    coll = db[collection]
    return db, coll


# collections
db, chats = connectCollection('API', 'chats')
db, users = connectCollection('API', 'users')
db, messages = connectCollection('API', 'messages')


def stop_not_existence(new_element,field, collection):
    '''check if the element is in the collection'''

    
    if re.search(r'^id',field):#id fields are stored as integers
        new_element = int(new_element)
    check = list(collection.find({field: new_element}))

    if check == []:
        raise Exception(f'{new_element} doesn\'t exist!')


def stop_existence(new_element,field,collection):
    '''check if the element is not in the collection'''

    

    if re.search(r'^id',field):#id fields are stored as integers
        new_element = int(new_element)
    check = list(collection.find({field: new_element}))
    if check != []:
        raise Exception(f'{new_element} already exists!')

def get_name(idUser):
    '''Gives back the user name introducing it's id'''

    name_id = list(users.find({'idUser': idUser}))
    userName = name_id[0]['userName']
    return userName
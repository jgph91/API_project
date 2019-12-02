# API_project

This API has the aim to analyze chats and recommend users that have similar 'sentiment' value.  

## Commands  

### user endpoints  

- Create a new user: @post(/users/create)  
- Get all user and its ids: @get(/users)  
- Get the id of your user: @get(/users/<userName>)  
- Get the sentiment values of your user: @get(/users/<idUser>/sentiment)    
- Returns the 3 most similar users to you: @get(/users/<userName>/recommend)

### chats endpoints  

- Start a chat to insert messages: @get(/chat/create)  
- Add a message to chat: @post(/messages/<idChat>/<idUser>/addmessage)
- Get all the messages from a chat: @get(/messages/chat/<idChat>)
- Get all the messages from an user: @get(/messages/user/<idUser>)
- Get the sentiment values from a chat @get(/chat/<idChat>/sentiment)  


## Files included  

api.py -> main file including the api code  
Dockerfile -> file for creating the container in docker  
.src/mongo.py -> file including the database functions  
.src/nltk.py -> file including the nltk functions to perform the sentiment analysis  
.src/recommender.py -> file including the recommender functions  
requeriments.txt -> md file containing all the modules used in this program  
./input/chats.json -> initial chats  

MongoDB Atlas -> database using 3 collections: users,chats and messages











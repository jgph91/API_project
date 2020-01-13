# Chat sentiment API

This API has the aim to analyze chats and recommend users that have similar 'sentiment' value.  
It's also deployed in heroku https://chat-sentiment-jgph91.herokuapp.com/   

The database is in Atlas MongoDB (cloud) and it contains 3 collections: users, chats and messages. The chats are analyzed using NLTK and the recommend system was developed using a similarities matrix which relates each user using its euclidean distances. 

## Commands  

### user endpoints  

- Create a new user inserting its nickname `/users/create` *enter userName via params  
- Get all user and its ids `/users`  
- Get the id of the specified user `/users/<userName>`
- Get the sentiment values of the specified user id `/users/<idUser>/sentiment`    
- Returns the 3 most similar users to the specified user `/users/<userName>/recommend`

### chats endpoints  

- Start a chat to insert new messages `/chat/create`  
- Add a message to a chat `/messages/<idChat>/<idUser>/addmessage` *enter the message via params
- Get all the messages from a chat `/messages/chat/<idChat>`
- Get all the messages from an user `/messages/user/<idUser>`
- Get the sentiment values from a chat `/chat/<idChat>/sentiment`  


## Files included  

- `api.py` -> main file including the api code  
- `Dockerfile` -> file for creating the container in docker  
- `src/mongo.py` -> file including the database functions  
- `src/nltk.py` -> file including the nltk functions to perform the sentiment analysis  
- `src/recommender.py` -> file including the recommender functions  
- `requeriments.txt` -> md file containing all the modules used in this program  
- `input/chats.json` -> initial chats  

## Contact info

If you have any doubt please don't heisitate to contact me:

- email : jgph91@gmail.com
- linkedin:  <a href="https://www.linkedin.com/in/javier-gomez-del-pulgar/?locale=en_US">Javier Gómez del Pulgar</a>












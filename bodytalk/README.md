# description cehck

An app that lets users, after logging in with Google+, add colorful english words to a collection. 
Users can add items and edit items they have created. 

# setup

The database, if empty, can be initialized with many filler words by executing ` python lotsofwords.py ` .

# use

start the application by executing ` python application.py ` while within the root directory. By default, the application will be served at ` 0.0.0.0:5000 ` .


A dump of the current state of the database, formatted in json, is available at ` /fetch ` , or ` /fetch/(wordname) `


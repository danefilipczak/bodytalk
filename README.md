An app that lets users, after logging in with Google+, add colorful english words to a collection. 
After signing in via Google+, users can add items and edit items they have created. 

# setup

start the application by executing ` python application.py ` while within the root directory. By default, the application will be served at ` 0.0.0.0:5000 ` .
The database, if empty, can be populated with many filler words by executing ` python lotsofwords.py ` .

A dump of the current state of the database, formatted in json, is available at /fetch, or /fetch/(wordname)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User, Base, Entry

engine = create_engine('sqlite:///simpleenglish.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Menu for UrbanBurger
newWord = Entry(word="dour", category = "adjective", definition = "relentlessly severe, stern, or gloomy in manner or appearance.")
session.add(newWord)
session.commit()

newWord = Entry(word="ululate", category = "verb", 
	definition = "howl or wail as an expression of strong emotion, typically grief.",
	example = "the fair hounds ululate the arrival of their master's casket")
session.add(newWord)
session.commit()




newWord = Entry(word="pithily", category = "adverb", 
	definition = "succinct, pointed, meaty, concise.",
	example = "he pithily rejoiced before the urgent matters.")
session.add(newWord)
session.commit()






print "added some words!"
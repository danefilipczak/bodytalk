from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import sys

from models import User, Base, Entry

if sys.argv[1] == 'dev':
	dbpath = 'sqlite:///bodytalkdev3.db'
elif sys.argv[1] == 'dep':
	dbpath = ''

engine = create_engine(dbpath)
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


# d = session.query(Entry).all()
# session.delete(d)
# session.commit()


newWord = Entry(category = "seeing", 
	entry = "the sun kiss the mountain",
	creatorEmail = 'dane.email@gmail.com',
	time = datetime.now() - timedelta(30)
	)
session.add(newWord)
session.commit()

newWord = Entry(category = "smelling", 
	entry = "burning leaves",
	creatorEmail = 'dane.email@gmail.com',
	time = datetime.now() - timedelta(3)
	)
session.add(newWord)
session.commit()



newWord = Entry(category = "feeling", 
	entry = "my shirt touch my back",
	creatorEmail = 'animposter@gmail.com',
	time = datetime.now() - timedelta(1)
	)
session.add(newWord)
session.commit()






print("added some words!")
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from models import User, Base, Entry

engine = create_engine('sqlite:///bodytalkdev2.db')
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
	entry = "my shirt on my back",
	creatorEmail = 'dane.email@gmail.com',
	time = datetime.now() - timedelta(30)
	)
session.add(newWord)
session.commit()

newWord = Entry(category = "hearing", 
	entry = "my shirt on my back",
	creatorEmail = 'dane.email@gmail.com',
	time = datetime.now() - timedelta(3)
	)
session.add(newWord)
session.commit()



newWord = Entry(category = "feeling", 
	entry = "my shirt on my back",
	creatorEmail = 'animposter@gmail.com',
	time = datetime.now() - timedelta(1)
	)
session.add(newWord)
session.commit()






print("added some words!")
from sqlalchemy import Column,ForeignKey,Integer,String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
Base = declarative_base()


class User(Base):
	# not used
    __tablename__ = 'user'
    ID = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
		



class Entry(Base):
	__tablename__ = 'entry'
	id = Column(Integer, primary_key=True)
	# word = Column(String, nullable = False)
	category = Column(String)
	entry = Column(String)
	time = Column(DateTime)
	#picture = Column(String)
	# definition = Column(String)
	# example = Column(String)
	creatorEmail = Column(String)
	#user = relationship(User)
	#price = Column(String)
	@property
	def serialize(self):
		return {
			'id':self.id,
			'word':self.word,
			'category':self.category,
			'definition':self.definition
		}
	'''
	@property
	def serialize(self):
	    """Return object data in easily serializeable format"""
	    return {
	    'name' : self.name,
	    'picture' : self.picture,
	    'description' : self.description,
	    'price' : self.price
	        }
	'''


engine = create_engine('sqlite:///bodytalkdev1.db')
 

Base.metadata.create_all(engine)
    
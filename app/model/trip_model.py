from sqlalchemy import create_engine, Column, String, Float, Date, Integer, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

Base = declarative_base()

class Trip(Base):
    __tablename__ = 'trips'
    id = Column(Integer, Sequence('trip_id_seq'), primary_key=True, autoincrement=True)
    path = Column(String)
    speed = Column(Float)
    date = Column(Date)

# Create an SQLite database engine
engine = create_engine('sqlite:///trips.db')

# Create the 'trips' table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

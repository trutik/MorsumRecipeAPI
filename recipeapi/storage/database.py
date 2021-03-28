from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

def get_database_session():
    engine = create_engine(os.environ['DB_CONNECTION_STRING'])
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


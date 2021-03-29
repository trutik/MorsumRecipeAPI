from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

def get_database():
    engine = create_engine('mysql+mysqldb://root:@localhost:3306/my_schema?charset=utf8mb4')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, engine


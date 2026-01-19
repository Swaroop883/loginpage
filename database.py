from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)#converts the python commands into raw sql query which are understood by the sql database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()#retruns a class
def get_db():
    db = SessionLocal()
    try:
        yield db #allows the conversation with the databse to stay alive while your database work is happening
    finally:
        db.close()
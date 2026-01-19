from sqlalchemy import Column, Integer, String
from database import Base
#here the user class is inheriting from the base class , and gets access to the metadata
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
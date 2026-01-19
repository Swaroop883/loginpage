#before auth we define how data looks and this file ensures that user sends the correct datatype
#this also conerts the user data into a user obj; so the username becomes the user.username
from pydantic import BaseModel
class UserCreate(BaseModel):
    username: str
    password: str
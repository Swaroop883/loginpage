from passlib.context import CryptContext #for hashing
from jose import JWTError,jwt #for tokens
from datetime import datetime,timedelta
import os
from dotenv import load_dotenv
load_dotenv()
#for password hashing
pwd_contest=CryptContext(schemes=["bcrypt"],deprecated="auto")
#for the jwt token verification
Secret_key =os.getenv("SECRET_KEY")
algo = os.getenv("ALGORITHM")
exp_time=30
#creating the hash
def hash_pass(password:str):
    return pwd_contest.hash(password)
#verification
def verify_pass(plain_password,hashed_password):
    return pwd_contest.verify(plain_password,hashed_password)
#header is auto created , we here define the payload generate the jwt_token
def create_jwt_token(data:dict):
    payload = data.copy()
    expire=datetime.utcnow()+timedelta(minutes=exp_time)
    payload.update({"exp":expire})
    jwt_token = jwt.encode(payload,Secret_key,algorithm=algo)
    return jwt_token


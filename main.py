from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware # Required for HTML connection
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import models, database

#for creating the jwt token 
SECRET_KEY = "Swaroop@2006_Secret_Key" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#deprecated tells server to verify if in future a better algo for hashing is made
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows any origin (your local HTML file)
    allow_credentials=True,
    allow_methods=["*"], # Allows POST, GET, etc.
    allow_headers=["*"], # Allows all headers
)

# Create the database tables in PostgreSQL automatically
models.Base.metadata.create_all(bind=database.engine)

# --- 3. HELPER FUNCTIONS ---

def get_password_hash(password):
    """Turns plain text into a secure scrambled hash."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Checks if the entered password matches the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """Generates the JWT token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- 4. THE ROUTES (Endpoints) ---

@app.get("/")
def read_root():
    """Home page route to avoid 'Not Found' errors."""
    return {"message": "Welcome to the Auth API. Go to /docs to test!"}

@app.post("/register")
def register_user(username: str, password: str, db: Session = Depends(database.get_db)):
    # Check if the user exists
    user_exists = db.query(models.User).filter(models.User.username == username).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Save user with hashed password
    new_user = models.User(username=username, hashed_password=get_password_hash(password))
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully!"}

@app.post("/login")
def login_for_access_token(username: str, password: str, db: Session = Depends(database.get_db)):
    # Find user
    user = db.query(models.User).filter(models.User.username == username).first()
    
    # Verify credentials
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Generate and return JWT
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
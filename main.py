from fastapi import FastAPI
from database import engine,Base
from fastapi.middleware.cors import CORSMiddleware
import models
import routes
#creating the database tables, it checks the User in the models .py and then the pgAdmin, if the user does not exust it creates it
models.Base.metadata.create_all(bind=engine)#bind is to tell the path to store the table
app=FastAPI()
#Allows frontend to talk tobackend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your specific domain
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routes.router)
#in the server if the request is other than the specified routes 
@app.get("/")
def other_route():
    return{"status":"the system is active"}
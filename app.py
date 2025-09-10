from fastapi import FastAPI
from dotenv import load_dotenv
import os
from routes.default import defaultrouter
from routes.signin import signinrouter
from fastapi.middleware.cors import CORSMiddleware
from routes.my_space import myspacerouter
from routes.signout import signoutrouter
from routes.delete_account import accountdeleterouter
from routes.boards import board_router
# from contextlib import asynccontextmanager
# from pymongo import AsyncMongoClient

load_dotenv()

# database=None

# @asynccontextmanager
# async def lifespan_manager():
#     global database
#     database=AsyncMongoClient(os.getenv('MONGO_DB'))[os.getenv('DB_NAME')]
#     yield
#     await database.client.aclose()

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv('APP_FRONT_END'),"http://localhost:5173"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(defaultrouter)
app.include_router(signinrouter,prefix="/signin")
app.include_router(myspacerouter,prefix="/myspace")
app.include_router(signoutrouter,prefix="/signout")
app.include_router(accountdeleterouter,prefix="/delete_account")
app.include_router(board_router,prefix="/boards")



import uvicorn
if(__name__=="__main__"):
    
    uvicorn.run("app:app",host='localhost',port=8000,log_level='info')
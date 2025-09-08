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

load_dotenv()
app=FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv('APP_FRONT_END')],  # frontend origin
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




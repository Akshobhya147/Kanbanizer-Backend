import jwt
from dotenv import load_dotenv
import os
import time
from fastapi.exceptions import HTTPException
from fastapi import Request

load_dotenv()

def create_token(user_id,email,time_delta=120):
    expiresAt=time.time()+time_delta # currently, our token is valid only for 120 seconds. Increase this.

    payload={
        "sub":user_id,
        "email":email,
        "expiresAt":expiresAt
    }

    return jwt.encode(payload,os.getenv('JWT_SECRET'),os.getenv('JWT_ALGORITHM'))

def verify_token(token:str):
    try:
        payload=jwt.decode(token,os.getenv('JWT_SECRET'),os.getenv('JWT_ALGORITHM'))
        if(payload):
            if(payload["expiresAt"]>=time.time()):
                return [True,payload]
            else:
                return [False,"Session expired."]
            
    except Exception as e:
        return [False,str(e)]

def extractJWT(request:Request):
    try:
        token=request.cookies['session_token']
        return token
    except Exception as e:
        raise e
from fastapi import Request,APIRouter
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
import os
from fastapi.responses import RedirectResponse,JSONResponse
from fastapi.exceptions import HTTPException
from jwt_handler import create_token
from mongodb_handler import check_account
import logging
from models import user_schema

load_dotenv()

logger=logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

signinrouter=APIRouter()

@signinrouter.post('/',tags=['signin'])
async def signin_process(
    # request:Request,
    user_details:user_schema
    ):
    try:
        account_exists=await check_account(user_details.userID,user_details.userEmail,user_details.userName,user_details.picture)
        if(account_exists):

            our_token=create_token(user_details.userID,user_details.userEmail,864000) # we are going to keep our token valid for 10 days 

            # response=RedirectResponse(url=os.getenv('APP_FRONT_END')+'/myspace',status_code=301) # 301 means moved permanently.
            response=JSONResponse({"status":"success","info":"Sign in successful"},200)
            response.set_cookie(
                key="session_token",
                value=our_token,
                httponly=True,
                secure=False if os.getenv('BUILD')=='dev' else True, # secure=True uses https
                samesite="lax" if os.getenv('BUILD')=='dev' else "none",
                path='/',
                max_age=864000,
            )

            response.headers["Cache-Control"]="no-store"

            return response
        
        else:
            logger.error("Account validation failed.")
            return "Account validation failed."

    
    except Exception as e:
        logger.error(f"Some error occured. Error:{str(e)}")
        return {"status":"error","info":str(e)}
    
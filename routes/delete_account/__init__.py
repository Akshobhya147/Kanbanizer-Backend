from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from mongodb_handler import delete_account
from jwt_handler import extractJWT,verify_token,create_token
import os
import logging

accountdeleterouter=APIRouter()

logger=logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

@accountdeleterouter.post("/",tags=["delete_account"])
async def account_delete(token=Depends(extractJWT)):
    try:
        verify_result=verify_token(token)
        if(verify_result[0]):
            res=await delete_account(verify_result[1]["sub"])
            response=JSONResponse(res,status_code=200)
            our_token=create_token("0","anon@email.com",-200) 
            response.set_cookie(
                key="session_token",
                value=our_token,
                httponly=True,
                secure=True,
                samesite="none",
                path='/',
                max_age=864000,
            )

            response.headers["Cache-Control"]="no-store"
            return response
        else:
            return {"status":"error","info":"Some issue, either with JWT authentication or cookie."}
    except Exception as e:
        logger.error(f"Some error occured. Error:{str(e)}")
        return {"status":"error","info":"Some error occured. Error:"+str(e)}

from fastapi import APIRouter,Depends
from jwt_handler import verify_token,extractJWT
from fastapi.exceptions import HTTPException
from mongodb_handler import get_user_info
import logging

logger=logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

myspacerouter=APIRouter()

@myspacerouter.get('/',tags=['myspace']) # for loading details of user from database
async def extract_user_info(token=Depends(extractJWT)):
    try:
        verify_result:list=verify_token(token)
        if(verify_result):
                status=verify_result[0]
                user_creds:dict=verify_result[1]
                if(status):
                    user_info=await get_user_info(user_creds["sub"])
                    return {"status":"success","info":user_info} # user details from database
                else:
                    logger.error(f"Some error occured. Error:{verify_result[1]}")
        return {"status":"error","info":"Invalid token."}
            
    except Exception as e:
        logger.error(f"Some error occured. Error:{str(e)}")
        return {"status":"error","info":str(e)}



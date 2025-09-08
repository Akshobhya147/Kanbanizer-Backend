from fastapi import APIRouter,Depends
from jwt_handler import verify_token,extractJWT
from models import board_schema
from mongodb_handler import get_boards,upsert_boards

board_router=APIRouter()

@board_router.get("/get_boards",tags=["boards","get boards"])
async def get_boards_fn(token=Depends(extractJWT)):
    verify_result=verify_token(token)
    if(verify_result[0]):
        user_creds=None
        if(verify_result[0]):
            user_creds=verify_result[1]
            userID=user_creds["sub"]
            return await get_boards(userID)
    return {"status":"error","info":"Some issue, either with JWT authentication or cookie."}

@board_router.post("/upsert_boards",tags=["boards","get boards"])
async def upsert_boards_fn(boards:list[board_schema],token=Depends(extractJWT)):
    verify_result=verify_token(token)
    if(verify_result[0]):
        user_creds=None
        if(verify_result[0]):
            user_creds=verify_result[1]
            userID=user_creds["sub"]
            # print("boards:\n\n\n\n",boards)
            return await upsert_boards(userID,boards)
    return {"status":"error","info":"Some issue, either with JWT authentication or cookie."}  
    

        

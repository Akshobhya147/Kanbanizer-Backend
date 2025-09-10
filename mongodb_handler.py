import logging.config
from pymongo import AsyncMongoClient
import os
from dotenv import load_dotenv
from models import user_schema,item_schema,board_schema
from fastapi.exceptions import HTTPException
import logging
from pymongo.collection import ObjectId
from board_generate import get_sample_board
import time

load_dotenv()

logger=logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

def get_database(dbname):
    database=AsyncMongoClient(os.getenv('MONGO_DB'))[dbname]
    return database

database=get_database(os.getenv('DB_NAME'))

async def check_account(userID:str,userEmail:str,userName:str,picture:str):
    users_collection=None
    if("users" not in await database.list_collection_names()):
        users_collection=await database.create_collection("users")
        logger.info("Created collection users")
    else:
        users_collection=database["users"]
   
    user=await users_collection.find_one({"userID":userID}) 
   
    if(user):
        return True
    else:
        return await create_account(userID,userEmail,userName,picture)
    

async def create_account(userID:str,userEmail:str,userName:str,picture:str):
    try:
        users_collection=database["users"]
        await users_collection.insert_one({"userID":userID,"userEmail":userEmail,"userName":userName,"picture":picture})
        await database.create_collection(userID) # creates an empty collection for the user.
        await upsert_board(userID=userID,board=get_sample_board(uid=userID,ct=int(time.time()*1000))) # creates a sample board for the user.
        logger.info(f"Account created successfully for {userEmail}.")
        return True
    except Exception as e:
        logger.error(f"Some error occured in account creation: {str(e)}")
        return False

async def get_user_info(userID:str):
    try:
        users_collection=database["users"]
        user_info=await users_collection.find_one({"userID":userID})
        user=user_schema(userID=user_info["userID"],userEmail=user_info["userEmail"],userName=user_info["userName"],picture=user_info["picture"])
        return user
    except Exception as e:
        raise e

async def delete_account(userID:str):
    try:
        users_collection=database["users"]
        await users_collection.delete_one({"userID":userID})
        await database.drop_collection(userID)
        return {"status":"success","info":"User account deleted successfully."}
    except Exception as e:
        logger.error(f"Some error occured. Error:{str(e)}")
        return {"status":"error","info":"Error deleting the user."+str(e)}

async def get_boards(userID:str):
    try:
        user_board_collection=database[userID]
        boards=user_board_collection.find()
        boards=await boards.to_list()

        board_list:list[board_schema]=[]

        for board in boards:
            board_id=str(board["_id"])
            board_name=board["board_name"]
            board_creation_date=board["board_creation_date"]

            item_list:list[item_schema]=[]

            for item in board["items"]:
                item_list.append(item_schema(id=item["id"],
                            name=item["name"],
                            description=item["description"],
                            type=item["type"],
                            order=item["order"],
                            createdAt=item["createdAt"],
                            deleted=item["deleted"],
                            deletePermanently=item["deletePermanently"],
                            board_id=item["board_id"]
                            ))
            board_list.append(board_schema(board_id=board_id,board_name=board_name,board_creation_date=board_creation_date,items=item_list))
        
        return {"status":"success","info":"Boards fetched successfully.","boards":board_list}
    except Exception as e:
        logger.error(f"Some error occured. Error:{str(e)}")
        return {"status":"error","info":"Error fetching boards:"+str(e),"boards":None}
            

async def upsert_board(userID:str,board:board_schema):
    try:
        update_list:list[item_schema]=[]
        removal_list:list[item_schema]=[]
        for item in board.items:
            if(item.deletePermanently):
                removal_list.append(item)
            else:
                update_list.append(item.model_dump())
        
        user_board_collection=database[userID]
        await user_board_collection.update_one({"_id":ObjectId(board.board_id)},{"$set":{"board_name":board.board_name,"board_creation_date":board.board_creation_date,"items":update_list}},upsert=True)
    except Exception as e:
        raise e

async def upsert_boards(userID:str,boards:list[board_schema]):
    try:
        # deleting boards in the database which are not in the received boards
        board_hash={boards[i].board_id:i for i in range(len(boards)) }
        
        res=await get_boards(userID)
        boards_db:list[board_schema]=res.get("boards")
        
        if(boards_db):
            user_board_collection=database[userID]
            for i in range(len(boards_db)):
                bd=boards_db[i]
                if(bd.board_id not in board_hash.keys()):
                    await user_board_collection.delete_one({'_id':ObjectId(bd.board_id)})

        # upserting boards   
        for board in boards:
            await upsert_board(userID,board)
        
        res=await get_boards(userID)
        if(res.get("boards","")==""):
            return {"status":"error","info":"Error upserting:"+res.get("info")}
        return {"status":"success","info":"Boards upserted successfully.","boards":res.get("boards")}
    except Exception as e:
        logger.error(f"Some error occured. Error:{str(e)}")
        return {"status":"error","info":"Error upserting:"+str(e),"boards":None}
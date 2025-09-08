from models import board_schema,item_schema
import json
from bson import ObjectId

def get_sample_board(uid:str,ct:float):
    """Get a sample board for a new user."""
    board=json.load(open('sample_board.json'))
    board=board_schema.model_validate(board)
    bid=ObjectId()

    board.board_id=str(bid)
    board.board_creation_date=ct
    n=0
    for item in board.items:
        item.id=uid+str(ct-n)
        item.createdAt=ct
        item.board_id=str(bid)
        n-=1

    return board


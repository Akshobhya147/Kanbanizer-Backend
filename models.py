from pydantic import BaseModel,Field
from typing import Any

class user_schema(BaseModel):
    userID:str=Field()
    userEmail:str=Field()
    userName:str=Field()
    picture:str=Field()
    class Config:
        schema={
            "user":{
                "userID":"some_id",
                "userEmail":"some_email",
                "userName":"some_name",
                "picture":"some_link"

            }
        }

class item_schema(BaseModel):
    id:str=Field()
    name:str=Field()
    description:str=Field(default="")
    type:str=Field()
    order: int=Field()
    createdAt: int
    deleted: bool
    deletePermanently: bool
    board_id: str

class board_schema(BaseModel):
    board_id: str
    board_name: str=Field()
    board_creation_date: int
    items: list[item_schema]

from fastapi import APIRouter

defaultrouter=APIRouter()

@defaultrouter.get('/',tags=['default_route'])
async def default_route():
    return "sup"
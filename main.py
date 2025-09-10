import uvicorn
from app import app
import logging
import os
from dotenv import load_dotenv

load_dotenv()

if(__name__=="__main__"):
    
    uvicorn.run("app:app",host=os.getenv('HOST'),port=int(os.getenv('PORT')),log_level='info')
    logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")
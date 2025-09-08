import uvicorn
from app import app
import logging

if(__name__=="__main__"):
    
    uvicorn.run("app:app",host='localhost',port=8000,log_level='info')
    logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")
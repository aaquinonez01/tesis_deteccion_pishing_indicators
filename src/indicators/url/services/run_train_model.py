import logging
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.getenv("PYTHONPATH"))
from src.indicators.url.trainning.url_trainning import UrlModelTrainer
from src.indicators.url.utils.constants import URL_PROCESS_DATASET_PATH, MODEL_PATH

url_trainer = UrlModelTrainer(URL_PROCESS_DATASET_PATH, MODEL_PATH)


#Testear modelo de URL

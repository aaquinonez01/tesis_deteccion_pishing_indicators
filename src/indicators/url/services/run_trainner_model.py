import logging
import sys
import os
from dotenv import load_dotenv

from src.indicators.url.trainning.url_trainning import UrlModelTrainer
from src.indicators.url.utils.constants import URL_PROCESS_DATASET_PATH, MODEL_PATH

url_trainer = UrlModelTrainer(URL_PROCESS_DATASET_PATH, MODEL_PATH)

try:
    print(URL_PROCESS_DATASET_PATH)
    url_trainer.load_dataset()
    url_trainer.train_model()
    url_trainer.evaluate_model()
    url_trainer.save_model()
    print("URL model trained successfully")
except Exception as e:
    logging.error("Error training URL model: %s", str(e))
    print("Error training URL model")
    
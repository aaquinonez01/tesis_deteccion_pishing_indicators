import os
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = os.getenv("BODY_DATASET_PATH")
BODY_PROCESS_DATASET_PATH = os.getenv("BODY_PROCESS_DATASET_PATH")
MODEL_PATH = os.getenv("BODY_MODEL_PATH")
VECTORIZER_PATH = os.getenv("BODY_VECTORIZER_PATH")
SELECTER_PATH = os.getenv("BODY_SELECTER_PATH")

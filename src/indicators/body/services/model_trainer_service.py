import logging
import os
from indicators.body.helpers.dowload_url import KaggleDatasetDownloader
from indicators.body.features.preprocessing import process_emails
from indicators.body.trainning.body_trainning import BodyModelTrainer
from indicators.body.utils.constants import BODY_PROCESS_DATASET_PATH, MODEL_PATH, VECTORIZER_PATH, SELECTER_PATH, CSV_PATH

class BodyModelTrainerService:
    def __init__(self):
        self.body_trainer = BodyModelTrainer(BODY_PROCESS_DATASET_PATH, MODEL_PATH, VECTORIZER_PATH, SELECTER_PATH)

    def download_and_preprocess(self, kaggle_dataset, download_path):
        try:
            # Descargar el dataset desde Kaggle
            downloader = KaggleDatasetDownloader(kaggle_dataset, download_path)
            downloader.download_dataset()

            # Preprocesar el dataset descargado
            csv_filename = os.path.join(download_path, 'dataset.csv')  # Cambia 'dataset.csv' según sea necesario
            process_emails(CSV_PATH, BODY_PROCESS_DATASET_PATH, VECTORIZER_PATH, SELECTER_PATH, max_workers=12)
        except Exception as e:
            logging.error(f"Error downloading or preprocessing dataset: {e}")
            raise

    def train_model(self):
        try:
            self.body_trainer.load_dataset()
            self.body_trainer.load_vectorizer_and_selector()
            self.body_trainer.split_dataset()
            self.body_trainer.train_model()
            self.body_trainer.evaluate_model()
            self.body_trainer.save_model()
            return "Body model trained successfully"
        except Exception as e:
            logging.error("Error training Body model: %s", str(e))
            raise
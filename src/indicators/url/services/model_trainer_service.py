import logging
from indicators.url.trainning.url_trainning import UrlModelTrainer
from indicators.url.utils.constants import URL_PROCESS_DATASET_PATH, MODEL_PATH, CSV_PATH
from indicators.url.features.preprocessing import UrlPreprocessor
from indicators.url.helpers.dowload_url import KaggleDatasetDownloader
class UrlModelTrainerService:
    def __init__(self):
        self.url_trainer = UrlModelTrainer(URL_PROCESS_DATASET_PATH, MODEL_PATH)
    def download_and_preprocess(self, kaggle_dataset, download_path):
        try:
            # Descargar el dataset desde Kaggle
            
            downloader = KaggleDatasetDownloader(kaggle_dataset, download_path)
            downloader.download_dataset()

            # Preprocesar el dataset descargado
            preprocessor = UrlPreprocessor(CSV_PATH, batch_size=200)  # Cambia 'dataset.csv' según sea necesario
            preprocessor.load_dataset()
            preprocessor.preprocess()
            preprocessor.save_processed_data(URL_PROCESS_DATASET_PATH)
        except Exception as e:
            logging.error(f"Error downloading or preprocessing dataset: {e}")
            raise

    def train_model(self):
        try:
            self.url_trainer.load_dataset()
            self.url_trainer.train_model()
            self.url_trainer.evaluate_model()
            self.url_trainer.save_model()
            return "URL model trained successfully"
        except Exception as e:
            logging.error("Error training URL model: %s", str(e))
            raise

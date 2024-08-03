import joblib
import pandas as pd
from indicators.url.features.extraction import UrlExtraction
from indicators.url.utils.constants import (
    MODEL_PATH,
    URL_PROCESS_DATASET_PATH,
    URL_FEATURE_COLUMNS,
)


class UrlPredictionService:
    def __init__(self):
        self.model = None
        self.processed_dataset_path = URL_PROCESS_DATASET_PATH
        self.load_model()

    def load_model(self):
        try:
            self.model = joblib.load(MODEL_PATH)
        except FileNotFoundError:
            print("Model file not found. Please train the model first.")
        except Exception as e:
            print(f"An error occurred while loading the model: {e}")

    def predict(self, url):
        url_instance = UrlExtraction(url)
        url_instance.getFeatures()
        prediction = self.model.predict([url_instance.features])[0]
        prediction_data = None
        if prediction == 1:
            prediction_data = 0
        else:
            prediction_data = 1
            
        print("prueba: " + str(prediction))
        return prediction_data
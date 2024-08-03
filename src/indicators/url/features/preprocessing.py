import pandas as pd
import sys
import os
from dotenv import load_dotenv
import concurrent.futures
from indicators.url.features.extraction import UrlExtraction
from indicators.url.utils.constants import (
    URL_FEATURE_COLUMNS,
    CSV_PATH,
    URL_PROCESS_DATASET_PATH,
)

# Cargar variables del archivo .env
load_dotenv()

# Agregar el directorio raíz al PYTHONPATH
sys.path.append(os.getenv("PYTHONPATH"))

class UrlPreprocessor:
    def __init__(self, csv_path, batch_size=5000):
        self.csv_path = csv_path
        self.batch_size = batch_size
        self.website_list = []
        self.list_doubt = []

    def load_dataset(self):
        try:
            self.dataset = pd.read_csv(self.csv_path)
            print("Lectura de archivo CSV exitosa")
        except pd.errors.ParserError as e:
            print(f"Error al leer el archivo CSV: {e}")
            self.dataset = pd.DataFrame()

    def process_url(self, index, row):
        try:
            label = 1 if row["result"] == 0 else -1
            aux = UrlExtraction(row["url"], label)
            aux.getFeatures()
            if aux.doubt == 0:
                return aux.features, None, index
            else:
                return None, row, index
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            return None, row, index

    def preprocess(self, max_workers=30):  # Aumenta el número de trabajadores
        print("Procesando URLs...")
        self.website_list = []
        self.list_doubt = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(self.process_url, index, row): (index, row) for index, row in self.dataset.iterrows()}
            for future in concurrent.futures.as_completed(future_to_url):
                features, doubt, index = future.result()
                print(f"Processed batch number: {index + 1}")
                if features is not None:
                    self.website_list.append(features)
                if doubt is not None:
                    self.list_doubt.append(doubt)
        print("Procesamiento de URLs finalizado")

    def save_processed_data(self, output_path):
        dt_finish = pd.DataFrame(self.website_list, columns=URL_FEATURE_COLUMNS)
        dt_finish.to_csv(output_path, index_label="Ord.")
        print(f"Datos preprocesados guardados en {output_path}")
        print("Lista de URL que dieron problemas:")
        print(self.list_doubt)

# Ejemplo de uso
if __name__ == "__main__":
    preprocessor = UrlPreprocessor(CSV_PATH, batch_size=200)
    preprocessor.load_dataset()
    preprocessor.preprocess(max_workers=50)  # Aumenta el número de trabajadores
    preprocessor.save_processed_data(URL_PROCESS_DATASET_PATH)

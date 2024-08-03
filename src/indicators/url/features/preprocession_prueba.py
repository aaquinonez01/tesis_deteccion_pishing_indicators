import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
import sys
import os
from dotenv import load_dotenv
import gc

# Cargar variables del archivo .env
load_dotenv()

# Agregar el directorio raíz al PYTHONPATH
sys.path.append(os.getenv("PYTHONPATH"))
from src.indicators.url.features.extraction import UrlExtraction
from src.indicators.url.utils.constants import (
    URL_FEATURE_COLUMNS,
    CSV_PATH,
    URL_PROCESS_DATASET_PATH,
)

class UrlPreprocessor:
    def __init__(self, csv_path, batch_size=200):  # Reduce el tamaño del lote
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

    def process_url(self, row):
        label = 1 if row["result"] == 0 else -1
        aux = UrlExtraction(row["url"], label)
        aux.getFeatures()
        if aux.doubt == 0:
            return aux.features, None
        else:
            return None, row

    def preprocess_batch(self, batch, batch_number):
        website_list = []
        list_doubt = []
        with ProcessPoolExecutor(max_workers=6) as executor:
            futures = {executor.submit(self.process_url, row): row for _, row in batch.iterrows()}

            for future in as_completed(futures):
                result, doubt = future.result()
                if result:
                    website_list.append(result)
                if doubt is not None:
                    list_doubt.append(doubt)

                # Print progress
                print(f"Batch {batch_number}: Processed {len(website_list) + len(list_doubt)} URLs")

        # Clear memory
        del batch
        gc.collect()
        
        return website_list, list_doubt

    def preprocess(self):
        print("Procesando URLs...")
        num_batches = len(self.dataset) // self.batch_size + 1
        total_processed = 0

        with ProcessPoolExecutor(max_workers=2) as executor:
            futures = {executor.submit(self.preprocess_batch, self.dataset.iloc[i * self.batch_size:(i + 1) * self.batch_size], i + 1): i for i in range(num_batches)}

            for future in as_completed(futures):
                website_list, list_doubt = future.result()
                self.website_list.extend(website_list)
                self.list_doubt.extend(list_doubt)
                total_processed += len(website_list) + len(list_doubt)

                # Print progress for cada batch
                print(f"Total processed: {total_processed}/{len(self.dataset)}")

        print("Procesamiento de URLs finalizado")

    def save_processed_data(self, output_path):
        dt_finish = pd.DataFrame(self.website_list, columns=URL_FEATURE_COLUMNS)
        dt_finish.to_csv(output_path, index_label="Ord.")
        print(f"Datos preprocesados guardados en {output_path}")
        print("Lista de URL que dieron problemas:")
        print(self.list_doubt)

# Ejemplo de uso
if __name__ == "__main__":
    preprocessor = UrlPreprocessor(CSV_PATH, batch_size=100)  # Reduce el tamaño del lote
    preprocessor.load_dataset()
    preprocessor.preprocess()
    preprocessor.save_processed_data(URL_PROCESS_DATASET_PATH)

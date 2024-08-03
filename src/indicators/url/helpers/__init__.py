import os
import kaggle
import zipfile
import logging

class KaggleDatasetDownloader:
    def __init__(self, dataset, download_path):
        self.dataset = dataset
        self.download_path = download_path

        # Asegúrate de que la carpeta de descarga existe
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def download_dataset(self):
        try:
            # Descargar el dataset
            kaggle.api.dataset_download_files(self.dataset, path=self.download_path, unzip=False)
            logging.info(f"Dataset {self.dataset} descargado en {self.download_path}")

            # Descomprimir el archivo descargado
            zip_path = os.path.join(self.download_path, f"{self.dataset.split('/')[-1]}.zip")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.download_path)
            logging.info(f"Dataset {self.dataset} descomprimido en {self.download_path}")

            # Eliminar el archivo zip
            os.remove(zip_path)
            logging.info(f"Archivo zip {zip_path} eliminado")
        except Exception as e:
            logging.error(f"Error descargando el dataset: {e}")
            raise

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Reemplaza 'your-username/dataset-name' con tu dataset privado de Kaggle
    downloader = KaggleDatasetDownloader('your-username/dataset-name', 'path/to/download')
    downloader.download_dataset()

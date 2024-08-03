import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
import sys
import os
from dotenv import load_dotenv
import numpy as np
import joblib

load_dotenv()
sys.path.append(os.getenv("PYTHONPATH"))

from indicators.body.features.text_preprocessing import TextProcessor
from indicators.body.utils.constants import CSV_PATH, BODY_PROCESS_DATASET_PATH, VECTORIZER_PATH, SELECTER_PATH
from indicators.body.features.extraction import BodyExtractionFeature

RESULT_MAP = {"Phishing Email": 1, "Safe Email": 0}

def process_email(row):
    try:
        tp = TextProcessor()
        body_email = row["body_email"]
        result_text = row["result"]
        result = RESULT_MAP.get(result_text, -1)
        tokens = tp.preprocess_text(body_email)
        print(f"Cuerpo con el índice {row['ord']} completado")
        return {"tokens": " ".join(tokens), "result": result}
    except Exception as e:
        print(f"Error procesando fila {row['ord']}: {e}")
        return None

def process_partition(partition):
    processed_data = []
    for _, row in partition.iterrows():
        result = process_email(row)
        if result is not None:
            processed_data.append(result)
    return pd.DataFrame(processed_data)

def process_emails(input_csv, output_csv, vectorizer_path, selector_path, max_workers=8):
    df = pd.read_csv(input_csv)
    
    num_partitions = max_workers * 2
    partitions = np.array_split(df, num_partitions)
    
    processed_data = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_partition, partition) for partition in partitions]

        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                processed_data.append(result)

    processed_df = pd.concat(processed_data)

    tfidf_transformer = BodyExtractionFeature(num_features=5000)
    tfidf_df, vectorizer, selector = tfidf_transformer.fit_transform(processed_df["tokens"], processed_df["result"])

    tfidf_df["result"] = processed_df["result"].values

    tfidf_df.to_csv(output_csv, index=False)
    
    # Guardar el vectorizador y el selector
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(selector, selector_path)
    print(f"Vectorizador guardado en {vectorizer_path}")
    print(f"Selector guardado en {selector_path}")

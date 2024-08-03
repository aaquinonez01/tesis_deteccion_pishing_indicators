import joblib
import pandas as pd
from indicators.body.features.text_preprocessing import TextProcessor
from indicators.body.utils.constants import MODEL_PATH, BODY_PROCESS_DATASET_PATH, VECTORIZER_PATH, SELECTER_PATH

class BodyPredictionService:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.selector = None
        self.processed_dataset_path = BODY_PROCESS_DATASET_PATH
        self.load_model_and_vectorizer_selector()

    def load_model_and_vectorizer_selector(self):
        try:
            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            self.selector = joblib.load(SELECTER_PATH)
        except FileNotFoundError:
            print("Model, vectorizer or selector file not found. Please train the model first.")
        except Exception as e:
            print(f"An error occurred while loading the model, vectorizer or selector: {e}")

    def predict(self, email_body):
        tp = TextProcessor()
        tokens = tp.preprocess_text(email_body)
        
        # Transformar tokens en características numéricas usando el vectorizador ajustado
        X = self.vectorizer.transform([" ".join(tokens)])
        
        # Seleccionar las mismas características que se usaron durante el entrenamiento
        X_new = self.selector.transform(X)
        
        features = X_new.toarray()[0]
        
        # Realizar la predicción
        prediction = self.model.predict([features])[0]
        
        return prediction
    
# if __name__ == "__main__":
#     prediction_service = BodyPredictionService()
#     email_body ="URL: http://www.newsisfree.com/click/-5,8304313,1717/ Date: 2002-09-27T08:51:29+01:00[IMG: http://www.newsisfree.com/Images/fark/cbc.ca.gif ([CBC])] "
#     prediction = prediction_service.predict(email_body)
#     print(f"Prediction: {prediction}")
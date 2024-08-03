import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

class BodyModelTrainer:
    def __init__(self, preprocessed_csv_path, model_path, vectorizer_path, selector_path):
        self.preprocessed_csv_path = preprocessed_csv_path
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.selector_path = selector_path

    def load_dataset(self):
        self.dataset = pd.read_csv(self.preprocessed_csv_path)
        self.X = self.dataset.drop("result", axis=1).values
        self.y = self.dataset["result"].values

        self.scaler = StandardScaler()
        self.X = self.scaler.fit_transform(self.X)
        print("Dataset cargado y características escaladas.")

    def load_vectorizer_and_selector(self):
        self.vectorizer = joblib.load(self.vectorizer_path)
        self.selector = joblib.load(self.selector_path)
        print(f"Vectorizador y selector cargados desde {self.vectorizer_path} y {self.selector_path}")

    def split_dataset(self, test_size=0.2, random_state=42):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state)
        print(f"Conjunto de datos dividido: {test_size * 100}% para prueba y {(1 - test_size) * 100}% para entrenamiento.")

    def train_model(self):
        self.model = RandomForestClassifier(n_jobs=-1)
        self.model.fit(self.X_train, self.y_train)
        print("Modelo entrenado.")

    def evaluate_model(self):
        self.y_pred = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, self.y_pred)
        
        report = classification_report(self.y_test, self.y_pred)
        print(f"Accuracy: {accuracy}")
        print("Precision: " + report.split("\n")[2])
        print("Recall: " + report.split("\n")[3])
        print("F1 Score: " + report.split("\n")[4])

    def save_model(self):
        joblib.dump(self.model, self.model_path)
        print(f"Modelo guardado en {self.model_path}")
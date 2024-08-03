import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, recall_score, precision_score
import joblib

class UrlModelTrainer:
    def __init__(self, preprocessed_csv_path, model_path):
        self.preprocessed_csv_path = preprocessed_csv_path
        self.model_path = model_path

    def load_dataset(self):
        self.dataset = pd.read_csv(self.preprocessed_csv_path)

        self.dataset = self.dataset.iloc[:, 1:]

        self.X = self.dataset.drop("result", axis=1).values
        self.y = self.dataset["result"].values

        self.scaler = StandardScaler()
        self.X = self.scaler.fit_transform(self.X)

        # Dividir el dataset en conjuntos de entrenamiento y prueba
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )

    def train_model(self):
        self.model = RandomForestClassifier(n_jobs=-1)
        self.model.fit(self.X_train, self.y_train)

    def evaluate_model(self):
        y_pred = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        recall = recall_score(self.y_test, y_pred, average='binary', pos_label=1)
        precision = precision_score(self.y_test, y_pred, average='binary', pos_label=1)

        print(f"Accuracy: {accuracy}")
        print(f"Recall: {recall}")
        print(f"Precision: {precision}")

    def save_model(self):
        joblib.dump(self.model, self.model_path)
        print(f"Modelo guardado en {self.model_path}")
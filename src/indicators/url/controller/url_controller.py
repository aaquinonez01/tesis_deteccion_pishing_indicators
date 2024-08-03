from flask import Blueprint, jsonify
from threading import Thread
from indicators.url.services.model_trainer_service import UrlModelTrainerService

class UrlController:
    def __init__(self):
        self.blueprint = Blueprint("url_controller", __name__)
        self.blueprint.add_url_rule("/train", "train", self.train, methods=["GET"])

    def train(self):
        try:
            Thread(target=self.train_url_model).start()
            return jsonify({"message": "Model training started in the background"}), 202
        except Exception as e:
            return jsonify({"message": str(e)}), 500

    def train_url_model(self):
        model_trainer = UrlModelTrainerService()
        model_trainer.train_model()

from flask import Blueprint, jsonify
from threading import Thread
from indicators.body.services.model_trainer_service import BodyModelTrainerService

class BodyController:
    def __init__(self):
        self.blueprint = Blueprint("body_controller", __name__)
        self.blueprint.add_url_rule("/train", "train", self.train, methods=["GET"])

    def train(self):
        try:
            Thread(target=self.train_body_model).start()
            return jsonify({"message": "Model training started in the background"}), 202
        except Exception as e:
            return jsonify({"message": str(e)}), 500

    def train_body_model(self):
        model_trainer = BodyModelTrainerService()
        model_trainer.train_model()

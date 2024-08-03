from flask import Blueprint, jsonify, request
import logging
from services.phishing_detection_service import PhishingDetectionService
logging.basicConfig(level=logging.DEBUG)
import re
class Controller:
    def __init__(self):
        self.blueprint = Blueprint("controller", __name__)
        self.phishing_detection_service = PhishingDetectionService()
        self.blueprint.add_url_rule("/predict", "predict", self.predict, methods=["POST"])
        
    def predict(self):
        try:
            datos = request.get_json()
            if not datos:
                logging.error("No se recibieron datos JSON")
                return jsonify({"error": "Invalid input, expected JSON"}), 415

            #logging.info(f"Datos recibidos: {datos}")

            # Procesar los datos recibidos
            data = {
                "ip": datos.get("sender_ip", ""),
                "urls": self.extract_urls(datos.get("body", "")),
                "domain": datos.get("sender_domain", ""),
                "body": datos.get("body", ""),
                "subject": datos.get("subject", ""),
                "sender_email": datos.get("sender_email", ""),
                "recipient_email": datos.get("recipient_email", "")
            }
            urls = self.extract_urls(data["body"])
            data["urls"] = urls
            print(data)

            #@logging.info(f"Datos procesados: {data}")

            result = self.phishing_detection_service.detect_phishing(data)
            logging.info(f"Resultado: {result}")
            return jsonify({"result": result})
        except Exception as e:
            logging.error(f"Error en predict: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    def extract_urls(self, body):
    # Patrón para detectar URLs
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        return url_pattern.findall(body)

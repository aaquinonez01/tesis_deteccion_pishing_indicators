from indicators.url.services.prediction_service import UrlPredictionService

from indicators.ip.services.prediction_service import IpPredictionService

from indicators.domain.services.prediction_service import DomainPredictionService
from indicators.body.services.prediction_service import BodyPredictionService
from utils.priority import priority_predict
#importar el json


class PhishingDetectionService:
    def __init__(self):
        self.url_prediction_service = UrlPredictionService()
        self.ip_prediction_service = IpPredictionService()
        self.domain_prediction_service = DomainPredictionService()
        self.body_prediction_service = BodyPredictionService()

    def detect_phishing(self, data):
        ordered_predictors = sorted(priority_predict.items(), key=lambda item: item[1])

        for predictor, _ in ordered_predictors:
            if predictor == "IP" and "ip" in data:
                ip_result = self.ip_prediction_service.predict(data["ip"])
                if ip_result == 1:
                    #return {"message": "Phishing detected", "predictor": "IP", "prediction": ip_result}
                    print("Phishing detected")
                    return 1

            if predictor == "URL" and "urls" in data:
                for url in data["urls"]:
                    url_result = self.url_prediction_service.predict(url)
                    if url_result == 1:
                        print("Phishing detected")
                        return 1

            if predictor == "Domain" and "domain" in data:
                domain_result = self.domain_prediction_service.predict(data["domain"])
                if domain_result == 1:
                    print("Phishing detected")
                    return 1

            if predictor == "Body" and "body" in data:
                body_result = self.body_prediction_service.predict(data["body"])
                if body_result == 1:
                    print("Phishing detected")
                    return 1
        print("Phishing not detected")
        return 0

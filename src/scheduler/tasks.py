def train_url_model():
    from indicators.url.services.model_trainer_service import UrlModelTrainerService
    model_trainer = UrlModelTrainerService()
    model_trainer.download_and_preprocess('alexanderquionez01/pishing-url-dataset', 'C:\\Users\\PC\\Documents\\tesis\\data\\url\\raw')
    model_trainer.train_model()

def train_body_model():
    from indicators.body.services.model_trainer_service import BodyModelTrainerService
    model_trainer = BodyModelTrainerService()
    model_trainer.train_model()

from threading import Thread
from .tasks import train_url_model, train_body_model

def configure_scheduler(scheduler):
    @scheduler.task('interval', id='train_url_model', hours=24*15)  # Cambia el intervalo según sea necesario
    def scheduled_train_url_model():
        Thread(target=train_url_model).start()

    @scheduler.task('interval', id='train_body_model', hours=24*30)  # Cambia el intervalo según sea necesario
    def scheduled_train_body_model():
        Thread(target=train_body_model).start()
import sys
import os
from dotenv import load_dotenv
from flask import Flask
from flask_apscheduler import APScheduler
from controller.controller import Controller
from indicators.url.controller.url_controller import UrlController
from indicators.body.controller.body_controller import BodyController
from scheduler.scheduler import configure_scheduler

# Cargar variables del archivo .env
load_dotenv()

# Agregar el directorio raíz al PYTHONPATH
sys.path.append(os.getenv("PYTHONPATH"))

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Registrar rutas
app.register_blueprint(Controller().blueprint, url_prefix="/api/v1")
app.register_blueprint(UrlController().blueprint, url_prefix="/api/v1/url")
app.register_blueprint(BodyController().blueprint, url_prefix="/api/v1/body")

scheduler = APScheduler()
scheduler.init_app(app)
configure_scheduler(scheduler)
scheduler.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
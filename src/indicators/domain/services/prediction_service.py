import pandas as pd
from indicators.domain.features.check_report import DomainChecker
from indicators.domain.utils.constants import DOMAIN_DATASET_PATH

import logging


class DomainPredictionService:
    def __init__(self):
        self.processed_dataset_path = DOMAIN_DATASET_PATH

    def predict(self, domain):
        try:
            domain_checker = DomainChecker(DOMAIN_DATASET_PATH)
            domain_info = domain_checker.is_domain_in_list(domain)
            return 1 if domain_info == 1 else 0
        except Exception as e:
            logging.error("Error predicting Domain: %s", str(e))
        return 1

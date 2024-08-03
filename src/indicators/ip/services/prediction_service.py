import pandas as pd
from indicators.ip.features.check_report import IPChecker
from indicators.ip.utils.constants import IP_DATASET_PATH

import logging


class IpPredictionService:
    def __init__(self):
        self.processed_dataset_path = IP_DATASET_PATH

    def predict(self, ip):
        try:
            ip_checker = IPChecker(IP_DATASET_PATH)
            ip_info = ip_checker.is_ip_in_list(ip)
            return 1 if ip_info == 1 else 0
        except Exception as e:
            logging.error("Error predicting IP: %s", str(e))
        return 1

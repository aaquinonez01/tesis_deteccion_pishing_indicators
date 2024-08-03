import csv


class IPChecker:
    def __init__(self, filename):
        """Inicializa la clase cargando las IPs desde el archivo CSV especificado."""
        self.ip_set = self.load_ips_from_csv(filename)

    def load_ips_from_csv(self, filename):
        """Carga las IPs desde un archivo CSV y las almacena en un conjunto."""
        ip_set = set()
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                ip_set.add(row["IP Address"])
        return ip_set

    def is_ip_in_list(self, ip):
        """Verifica si una IP está en el conjunto de IPs cargadas.
        Devuelve 1 si la IP está presente, -1 si no lo está."""
        return 1 if ip in self.ip_set else -1

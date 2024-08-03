import csv


class DomainChecker:
    def __init__(self, filename):
        """Inicializa la clase cargando las IPs desde el archivo CSV especificado."""
        self.domain_set = self.load_domains_from_csv(filename)

    def load_domains_from_csv(self, filename):
        """Carga los Dominios desde un archivo CSV y las almacena en un conjunto."""

        domain_set = set()
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                domain_set.add(row["domain"])
        return domain_set

    def is_domain_in_list(self, ip):
        """Verifica si un Dominio está en el conjunto de IPs cargadas.
        Devuelve 1 si el Dominio está presente, -1 si no lo está."""
        return 1 if ip in self.domain_set else -1

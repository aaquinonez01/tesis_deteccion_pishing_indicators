import re
import ipaddress
import urllib.parse as urp
import requests as rq
import whois as ws
from datetime import date
from datetime import datetime
from bs4 import BeautifulSoup
from googlesearch import search
import socket


class UrlExtraction:
    def __init__(self, url, result=None):
        self.url = url
        self.domain = None
        self.response = None
        self.whois = None
        self.soup = None
        self.features = []
        self.result = result
        self.doubt = 0

    def printWebsite(self):
        print("La url ingresada es {}".format(self.url))

    "Agregar http a las url que no tiene https al inicio de la url"

    def addHttp(self):
        if not re.match(r"^https?", self.url) or not re.match(r"^http?", self.url):
            self.url = "http://" + self.url
        return

    "Encontrar el dominio y reemplazo www"

    def findDomain(self):
        self.domain = urp.urlparse(self.url).netloc
        if re.match(r"^www.", self.domain):
            self.domain = self.domain.replace("www.", "")

    "Obtener el response"

    def getResponse(self):
        try:
            self.response = rq.get(self.url, timeout=5.0)
        except Exception as e:
            return

    "Obtener registro whois" ""

    def getWhois(self):
        try:
            self.whois = ws.whois(self.domain)
        except:
            return

    "Traer información con BeautifulSoap"

    def getSoup(self):
        try:
            self.soup = BeautifulSoup(self.response.text, "html.parser")
        except:
            return

    """#1. Tiene dirección ip"""

    def haveIp(self):
        try:
            ipaddress.ip_address(self.domain)
            return -1
        except:
            "Retorna Error cuando no encuentra una ip"
            return 1

    """#2. Longitud de la url"""

    def lengthUrl(self):
        if len(self.url) < 54:
            return 1
        elif len(self.url) < 75:
            return 0
        else:
            return -1

    """#3. Tiene el símbolo @ """

    def haveAtSymbol(self):
        if "@" in self.url:
            return -1
        else:
            return 1

    """#4. Estado SSL"""

    def sslState(self):
        if not self.url.startswith("https"):
            return -1
        else:
            return 1

    def convertDate(self, date):
        if isinstance(date, str):
            date = date[0:19]
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()
        return date

    """#5. Edad del Dominio"""

    def domainAge(self):
        if self.whois == None or not self.whois.creation_date:
            return -1
        else:
            try:
                creationDate = self.whois.creation_date[0]
                try:
                    creationDate = self.convertDate(creationDate)
                except:
                    creationDate = self.whois.creation_date[1]
                    creationDate = self.convertDate(creationDate)
            except:
                creationDate = self.whois.creation_date
                try:
                    creationDate = self.convertDate(creationDate)
                except:
                    self.whois.creation_date = None
                    creationDate = None
            try:
                if not creationDate == None:
                    if (date.today().year - creationDate.year) < 1:
                        if (date.today().month - creationDate.month) < 6:
                            return -1
                        else:
                            return 1
                    else:
                        return 1
                else:
                    return -1
            except:
                self.doubt = 1
                return

    """#6. Redirección de doble barra"""

    def redirectionSlashDouble(self):
        position = self.url.rfind("//")
        if position > 6:
            return -1
        else:
            return 1

    """#7. URL de anclaje"""

    def anchorUrl(self):
        "tag 'a'"
        if self.soup == None:
            return -1
        else:
            i = 0
            countOk = 0
            percentValueOk = 0.0
            for a in self.soup.find_all("a", href=True):
                if (
                    "#" in a["href"]
                    or "javascript" in a["href"].lower()
                    or "mailto" in a["href"].lower()
                    or not (self.url in a["href"] or self.domain in a["href"])
                ):
                    countOk = countOk + 1
                i += 1
            try:
                percentValueOk = (countOk * 100) / float(i)
            except:
                return 1
            if percentValueOk < 31.0:
                return 1
            elif percentValueOk < 67.0:
                return 0
            else:
                return -1

    """#8. Prefijo Sufijo"""

    def prefixSuffix(self):
        if "-" in self.domain:
            return -1
        else:
            return 1

    """#9. Enlaces en Etiquetas"""

    def linksInTags(self):
        "All tags"
        if self.soup == None:
            return -1
        else:
            i = 0
            countOk = 0
            percentValueOk = 0.0
            for link in self.soup.find_all("link", href=True):
                dots = [link.start(0) for link in re.finditer("\.", link["href"])]
                if (
                    self.url in link["href"]
                    or self.domain in link["href"]
                    or len(dots) == 1
                ):
                    countOk += 1
                i += 1
            for script in self.soup.find_all("script", src=True):
                dots = [x.start(0) for x in re.finditer("\.", script["src"])]
                if (
                    self.url in script["src"]
                    or self.domain in script["src"]
                    or len(dots) == 1
                ):
                    countOk += 1
                i += 1
            try:
                percentValueOk = (countOk * 100) / i
            except:
                return 1
            if percentValueOk < 17.0:
                return 1
            elif percentValueOk < 81.0:
                return 0
            else:
                return -1

    """#10. Deshabilitar clic derecho"""

    def clicRigth(self):
        ##Trata de "Usar onMouseOver para ocultar el enlace".
        ##Se busca el evento "event.button==2"
        if self.response == None:
            return -1
        else:
            if re.findall(r"event.button ?== ?2", self.response.text):
                return 1
            else:
                return -1

    """#11. Uso de la ventana emergente"""

    def windowsPopUp(self):
        if self.response == None:
            return -1
        else:
            if re.findall(r"alert\(", self.response.text):
                return 1
            else:
                return -1

    """#12. Favicon"""

    def favicon(self):
        if self.soup == None:
            return -1
        else:
            for head in self.soup.find_all("head"):
                for head.link in self.soup.find_all("link", href=True):
                    dots = [x.start() for x in re.finditer(r"\.", head.link["href"])]
                    if (
                        self.url in head.link["href"]
                        or len(dots) == 1
                        or self.domain in head.link["href"]
                    ):
                        return 1
                    else:
                        return -1
        return 1

    """#13. URL anormal"""

    def abnormalURL(self):
        if self.response == None:
            return -1
        else:
            if self.response.text == self.whois:
                return 1
            else:
                return -1

    """#14. IFrame"""

    def iframe(self):
        ##Si el iframe está vacío o no se encuentra respuesta es phishing
        if self.response == None:
            return -1
        else:
            if re.findall(r"[<iframe>|<frameBorder>]", self.response.text):
                return 1
            else:
                return -1

    """#15. Registro DNS"""

    def dnsRegister(self):
        if self.whois == None:
            return -1
        else:
            return 1

    "#16. Índice de google"

    def googleIndex(self):
        webSite = search(self.url, 5)
        if webSite:
            return 1
        else:
            return -1

    "#17. Puerto"

    def port(self):
        try:
            port = self.domain.split(":")[1]
            if port:
                return -1
            else:
                return -1
        except:
            return -1

    "#18. Request URL"

    def requestUrl(self):
        "object: img, audio, embed, i_frame"
        if self.soup == None:
            return -1
        else:
            i = 0
            countOk = 0
            percentValueOk = 0.0
            for img in self.soup.find_all("img", src=True):
                dots = [slash.start() for slash in re.finditer(r"\.", img["src"])]
                if self.domain in img["src"] or self.url in img["src"] or dots == 1:
                    countOk += 1
                i += 1
            for audio in self.soup.find_all("audio", src=True):
                dots = [slash.start() for slash in re.finditer(r"\.", audio["src"])]
                if self.domain in audio["src"] or self.url in audio["src"] or dots == 1:
                    countOk += 1
                i += 1
            for embed in self.soup.find_all("embed", src=True):
                dots = [slash.start() for slash in re.finditer(r"\.", embed["src"])]
                if self.domain in embed["src"] or self.url in embed["src"] or dots == 1:
                    countOk += 1
                i += 1
            for i_frame in self.soup.find_all("i_frame", src=True):
                dots = [slash.start() for slash in re.finditer(r"\.", i_frame["src"])]
                if (
                    self.domain in i_frame["src"]
                    or self.url in i_frame["src"]
                    or dots == 1
                ):
                    countOk += 1
                i += 1
            try:
                percentValueOk = (countOk * 100) / i
            except:
                return 1
            if percentValueOk < 22.0:
                return 1
            elif percentValueOk < 61.0:
                return 0
            else:
                return -1

    "#19. Controlador de formulario de servidor (SFH)"

    def sfh(self):
        if self.soup == None:
            return -1
        else:
            if len(self.soup.find_all("form", action=True)) == 0:

                return 1
            else:
                for form in self.soup.find_all("form", action=True):
                    if form["action"] == "" or form["action"] == "about:blank":
                        return -1
                    elif (
                        self.url not in form["action"]
                        and self.domain not in form["action"]
                    ):
                        return 0
                    else:
                        return 1

    "#20. Recuento de redirección del sitio web (website forwarding)"

    def websiteForwarding(self):
        ##sitios web de phishing  han sido redirigidos al menos 4 veces
        if self.response == None:
            return -1
        else:
            if len(self.response.history) <= 1:
                return -1
            elif len(self.response.history) <= 4:
                return 0
            else:
                return 1

    "#21. Personalización de la barra de estado (Mouse over)"

    def mouseOver(self):
        ##buscar en el código fuente de la página web el evento "onMouseOver", y comprobar si realiza algún cambio en la barra de estado
        if self.response == None:
            return -1
        else:
            if re.findall("<script>.+onmouseover.+</script>", self.response.text):
                return 1
            else:
                return -1

    "#22. Tráfico web"

    def webTraffic(self):
        "traer el doc detrás de la url"
        try:
            rank = self.soup.find("reach")["rank"]
            if int(rank) < 100000:
                return -1
            else:
                return 1
        except:
            return -1

    "#23. Servicio de acortamiento"

    def shorterService(self):
        listService = (
            r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|"
            r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|"
            r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|"
            r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|"
            r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|"
            r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|"
            r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|"
            r"tr\.im|link\.zip\.net"
        )
        if re.search(listService, self.url):
            return -1
        else:
            return 1

    "#24. Duración del registro del dominio"

    def domainRegisterAge(self):
        if (
            self.whois == None
            or not self.whois.expiration_date
            or not self.whois.creation_date
        ):
            return -1
        else:
            try:
                creationDate = self.whois.creation_date[0]
                if isinstance(creationDate, str):
                    creationDate = self.whois.creation_date[0:19]
                    creationDate = datetime.strptime(
                        creationDate, "%Y-%m-%d %H:%M:%S"
                    ).date()
            except:
                creationDate = self.whois.creation_date
            try:
                expirationDate = self.whois.expiration_date[0]
                if isinstance(creationDate, str):
                    expirationDate = self.whois.expiration_date[0:19]
                    expirationDate = datetime.strptime(
                        expirationDate, "%Y-%m-%d %H:%M:%S"
                    ).date()
            except:
                expirationDate = self.whois.expiration_date
            try:
                if (expirationDate.year - creationDate.year) <= 1:
                    return -1
                else:
                    return 1
            except:
                self.doubt = 1
                return

    "#25. Token HTTPS"

    def httpsToken(self):
        if "https" in self.domain:
            return -1
        else:
            return 1

    "#26. Envío de información al correo electrónico"

    def emailInformation(self):
        if self.response == None:
            return -1
        else:
            if re.findall(r"[mail\(\)|mailto:?]", self.response.text):
                return -1
            else:
                return 1

    "#27. Rango de página"

    def pageRank(self):
        try:
            rankResponse = rq.post(
                "https://www.checkpagerank.net/index.php",
                {"name": self.domain},
                timeout=5.0,
            )
            globalRank = re.findall(r"Global Rank: ([0-9]+)", rankResponse.text)[0]
            if int(globalRank) > 0 and int(globalRank) < 100000:
                return 1
            else:
                return 0
        except:
            return -1

    "#28. Informe estadístico"

    def staticalInform(self):
        urlMatch = re.search(
            "at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly",
            self.url,
        )
        try:
            ipAddress = socket.gethostbyname(self.domain)
            ipMatch = re.search(
                "146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|"
                "107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|"
                "118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|"
                "216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|"
                "34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|"
                "216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42",
                ipAddress,
            )
            if urlMatch:
                return -1
            elif ipMatch:
                return -1
            else:
                return 1
        except Exception as e:
            return 0

    "#29. Tiene un subdomino"

    def haveSubdomain(self):
        if len(re.findall("\.", self.url)) == 1:
            return 1
        elif len(re.findall("\.", self.url)) == 2:
            return 0
        else:
            return -1

    "#30. Enlaces que apuntan a la página"

    def linksToPage(self):
        if self.response == None:
            return -1
        else:
            numLinks = len(re.findall(r"<a href=", self.response.text))
            if int(numLinks) <= 2:
                return 1
            else:
                return -1

    "#31. verificar md5"

    def hasMD5(self):
        md5_pattern = re.compile(r"[a-fA-F\d]{32}")
        if md5_pattern.search(self.url):
            return 1
        else:
            return -1

    "#32. verificar SHA1"

    def hasSHA1(self):
        sha1_pattern = re.compile(r"[a-fA-F\d]{40}")
        if sha1_pattern.search(self.url):
            return 1
        else:
            return -1

    "#33. verificar Yara"

    def hasYara(self):
        yara_pattern = re.compile(r"rule\s+.+\s+\{[\s\S]*?\}")
        if yara_pattern.search(self.url):
            return 1
        else:
            return -1

    "#34. verificar SHA256"

    def hasSHA256(self):
        sha256_pattern = re.compile(r"[a-fA-F\d]{64}")
        if sha256_pattern.search(self.url):
            return 1
        else:
            return -1

    "#35. verificar Short"

    def hasShort(self):
        if "short" in self.url:
            return 1
        else:
            return -1

    "#36. verificar dataTime"

    def hasDateTime(self):
        datetime_pattern = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
        if datetime_pattern.search(self.url):
            return 1
        else:
            return -1

    "#37. verificar Domain"

    def hasDomain(self):
        domain_pattern = re.compile(r"^[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}$")
        if domain_pattern.search(self.url):
            return 1
        else:
            return -1

    "#38. verificar hostname"

    def hasHostname(self):
        hostname_pattern = re.compile(
            r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$"
        )
        if hostname_pattern.search(self.url):
            return 1
        else:
            return -1

    "#39. verificar IPDSt"

    def hasIPDst(self):
        ip_pattern = re.compile(r"^([0-9]{1,3}\.){3}[0-9]{1,3}$")
        if ip_pattern.search(self.url):
            return 1
        else:
            return -1

    "#40. verificar IPDSt"

    def hasIPSrc(self):
        ip_src_regex = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b(?:/\d{1,2})?\b")
        if ip_src_regex.search(self.url):
            return 1
        else:
            return -1

    "Reunir todas las características"

    def getFeatures(self):
        self.addHttp()
        self.findDomain()
        self.getResponse()
        self.getWhois()
        self.getSoup()
        self.features.append(self.haveIp())
        self.features.append(self.lengthUrl())
        self.features.append(self.haveAtSymbol())
        self.features.append(self.sslState())
        self.features.append(self.domainAge())
        if self.doubt == 0:
            self.features.append(self.redirectionSlashDouble())
            self.features.append(self.anchorUrl())
            self.features.append(self.prefixSuffix())
            self.features.append(self.linksInTags())
            self.features.append(self.clicRigth())
            self.features.append(self.windowsPopUp())
            self.features.append(self.favicon())
            self.features.append(self.abnormalURL())
            self.features.append(self.iframe())
            self.features.append(self.dnsRegister())
            self.features.append(self.googleIndex())
            self.features.append(self.port())
            self.features.append(self.requestUrl())
            self.features.append(self.sfh())
            self.features.append(self.websiteForwarding())
            self.features.append(self.mouseOver())
            self.features.append(self.webTraffic())
            self.features.append(self.shorterService())
            self.features.append(self.domainRegisterAge())
            if self.doubt == 0:
                self.features.append(self.httpsToken())
                self.features.append(self.emailInformation())
                self.features.append(self.pageRank())
                self.features.append(self.staticalInform())
                self.features.append(self.haveSubdomain())
                self.features.append(self.linksToPage())
                self.features.append(self.hasMD5())
                self.features.append(self.hasSHA1())
                self.features.append(self.hasYara())
                self.features.append(self.hasSHA256())
                self.features.append(self.hasShort())
                self.features.append(self.hasDateTime())
                self.features.append(self.hasDomain())
                self.features.append(self.hasHostname())
                self.features.append(self.hasIPDst())
                self.features.append(self.hasIPSrc())
        if not self.result == None:
            self.features.append(self.result)

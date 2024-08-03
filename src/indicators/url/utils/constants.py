import os
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = os.getenv("URL_DATASET_PATH")
URL_PROCESS_DATASET_PATH = os.getenv("PROCESSED_URL_DATASET_PATH")
MODEL_PATH = os.getenv("URL_MODEL_PATH")

URL_FEATURE_COLUMNS = [
    "haveIp",
    "lengthUrl",
    "haveAtSymbol",
    "sslState",
    "domainAge",
    "slashDouble",
    "anchorUrl",
    "prefixSuffix",
    "linksInTags",
    "clicRigth",
    "windowsPopUp",
    "favicon",
    "abnormalURL",
    "iframe",
    "dnsRegister",
    "googleIndex",
    "port",
    "requestUrl",
    "sfh",
    "websiteForwarding",
    "mouseOver",
    "webTraffic",
    "shorterService",
    "domainRegisterAge",
    "httpsToken",
    "emailInformation",
    "pageRank",
    "staticalInform",
    "haveSubdomain",
    "linksToPage",
    "hasMD5",
    "hasSHA1",
    "hasYara",
    "hasSHA256",
    "hasShort",
    "hasDateTime",
    "hasDomain",
    "hasHostname",
    "hasIPDst",
    "hasIPSrc",
    "result",
]

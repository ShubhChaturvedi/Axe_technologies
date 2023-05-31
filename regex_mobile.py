import re

MOBILE_REGEX = {
    "battery": r"(?:^\d+\s?mah\s?battery\s?$)|(?:^\d+\s?mah\s?$)|(?:^\d+\s?mah\s?battery)|(?:^\d+\s?mah)",
    "charger" : r"(?:^\d+\s?w\s?fast\s?charger\s?$)|(?:^\d+\s?w\s?charger\s?$)|(?:^\d+\s?w\s?fast\s?charge)|(?:^\d+\s?w\s?charge)|(?:^\d+\s?w\s?fast\s?charger)|(?:^\d+\s?w\s?charger)|(?:^\d+\s?w\s?fast\s?charge)|(?:^\d+\s?w\s?charge)",
    "display": r"(?:^\d+\s?fhd\+ display\s?$)|(?:^\d+mp[\s\w]+ display\s?$)|(?:^\d+\s?s+\s?amoled\+\d+hz\s?$)|(?:^\d+\s?fhd\+ display)|(?:^\d+mp[\s\w]+ display)|(?:^\d+\s?s+\s?amoled\+\d+hz)",
    "camera": r"(\d+MP[\s\w]+ camera|\d+MP[\s\w]+ triple camera|\d+mp[\s\w]+ dual camera)|(\d+MP[\s\w]+ camera|\d+MP[\s\w]+ triple camera|\d+mp[\s\w]+ dual camera\s)",
    "sim": r"(?:^\d+\s?singal\s?sim\s?$)|(?:^\d+\s?dual\s?sim\s?$)|(?:^\d+\s?singal\s?sim)|(?:^\d+\s?dual\s?sim)",
    "camera_type": r"(?:^\d+\s?rear vga camera)|(?:^\d+ mp camera)|(?:^\d+\s?rear vga camera\s?$)|(?:^\d+ mp camera\s?$)"
}




MEMORY_REGEX = {
    "sdram":{
        "tb": r"(?:^\d+\s?tb\s?sdram\s?$)",
        "gb": r"(?:^\d+\s?gb\s?sdram\s?$)",
        "mb": r"(?:^\d+\s?mb\s?sdram\s?$)"
    },
    "ram":{
        "tb": r"(?:^\d+\s?tb\s?ram\s?$)|(?:^\d+\s?tb\s?$)",
        "gb": r"(?:^\d+\s?gb\s?ram\s?$)|(?:^\d+\s?gb\s?$)",
        "mb": r"(?:^\d+\s?mb\s?ram\s?$)|(?:^\d+\s?mb\s?$)" 
    }
}

STORAGE_REGEX = {
    "tb": {
        "ssd": r"(?:^\d+\s?tb\s?ssd\s?$)|(?:\d+\s?tb\s?ssd\s?)",
        "hdd": r"(?:^\d+\s?tb\s?hdd\s?$)|(?:^\d+\s?tb\s?storage\s?$)|(?:\d+\s?tb\s?hdd\s?)|(?:\d+\s?tb\s?storage\s?)",
        "rom": r"(?:^\d+\s?tb\s?rom\s?$)|(?:\d+\s?tb\s?rom\s?)",
        "sdd": r"(?:^\d+\s?tb\s?sdd\s?$)|(?:\d+\s?tb\s?sdd\s?)",
        "emmc": r"(?:\d+\s?tb\s?emmc\s?storage\s?)|(?:\d+\s?tb\s?emmc\s?)",
        "generic": r"(?:^\d+\s?tb\s?$)"
    },
    "gb": {
        "ssd": r"(?:^\d+\s?gb\s?ssd\s?$)|(?:\d+\s?gb\s?ssd\s?)",
        "hdd": r"(?:^\d+\s?gb\s?hdd\s?$)|(?:^\d+\s?gb\s?storage\s?$)|(?:\d+\s?gb\s?hdd\s?)|(?:\d+\s?gb\s?storage\s?)",
        "rom": r"(?:^\d+\s?gb\s?rom\s?$)|(?:\d+\s?gb\s?rom\s?)",
        "sdd": r"(?:^\d+\s?gb\s?sdd\s?$)|(?:\d+\s?gb\s?sdd\s?)",
        "emmc": r"(?:\d+\s?gb\s?emmc\s?storage\s?)|(?:\d+\s?gb\s?emmc\s?)",
        "generic": r"(?:^\d+\s?gb\s?$)"
    },
    "mb": {
        "ssd": r"(?:^\d+\s?mb\s?ssd\s?$)|(?:\d+\s?mb\s?ssd\s?)",
        "hdd": r"(?:^\d+\s?mb\s?hdd\s?$)|(?:^\d+\s?mb\s?storage\s?$)|(?:\d+\s?mb\s?hdd\s?)|(?:\d+\s?mb\s?storage\s?)",
        "rom": r"(?:^\d+\s?mb\s?rom\s?$)|(?:\d+\s?mb\s?rom\s?)",
        "sdd": r"(?:^\d+\s?mb\s?sdd\s?$)|(?:\d+\s?mb\s?sdd\s?)",
        "emmc": r"(?:\d+\s?mb\s?emmc\s?storage\s?)|(?:\d+\s?mb\s?emmc\s?)",
        "generic": r"(?:^\d+\s?mb\s?$)"
    }
}

WEIGHT_REGEX = {
    "kg":[
        r"(?:^\d+\.?\d+\s?\-?\s?kilograms\s?$)|(?:^\d+\s?\-?\s?kilograms\s?$)|(?:^\d+\.?\d+\s?\-?\s?kilogram\s?$)|(?:^\d+\s?\-?\s?kilogram\s?$)|(?:^\d+\.?\d+\s?\-?\s?kgs\s?$)|(?:^\d+\s?\-?\s?kgs\s?$)|(?:^\d+\.?\d+\s?\-?\s?kg\s?$)|(?:^\d+\s?\-?\s?kg\s?$)",
        r"(?:\s{1}\d+\.?\d+\s?\-?\s?kilograms\s{1})|(?:\s{1}\d+\s?\-?\s?kilograms\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?kilogram\s{1})|(?:\s{1}\d+\s?\-?\s?kilogram\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?kgs\s{1})|(?:\s{1}\d+\s?\-?\s?kgs\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?kg\s{1})|(?:\s{1}\d+\s?\-?\s?kg\s{1})",    
    ],
    "gm":[
        r"(?:^\d+\.?\d+\s?\-?\s?grams\s?$)|(?:^\d+\s?\-?\s?grams\s?$)|(?:^\d+\.?\d+\s?\-?\s?gram\s?$)|(?:^\d+\s?\-?\s?gram\s?$)|(?:^\d+\.?\d+\s?\-?\s?gms\s?$)|(?:^\d+\s?\-?\s?gms\s?$)|(?:^\d+\.?\d+\s?\-?\s?gm\s?$)|(?:^\d+\s?\-?\s?gm\s?$)",
        r"(?:\s{1}\d+\.?\d+\s?\-?\s?grams\s{1})|(?:\s{1}\d+\s?\-?\s?grams\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?gram\s{1})|(?:\s{1}\d+\s?\-?\s?gram\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?gms\s{1})|(?:\s{1}\d+\s?\-?\s?gms\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?gm\s{1})|(?:\s{1}\d+\s?\-?\s?gm\s{1})",    
    ],
    "litre":[
        r"(?:^\d+\.?\d+\s?\-?\s?litres\s?$)|(?:^\d+\s?\-?\s?litres\s?$)|(?:^\d+\.?\d+\s?\-?\s?litre\s?$)|(?:^\d+\s?\-?\s?litre\s?$)|(?:^\d+\.?\d+\s?\-?\s?l\s?$)|(?:^\d+\s?\-?\s?l\s?$)",
        r"(?:\s{1}\d+\.?\d+\s?\-?\s?litres\s{1})|(?:\s{1}\d+\s?\-?\s?litres\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?litre\s{1})|(?:\s{1}\d+\s?\-?\s?litre\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?l\s{1})|(?:\s{1}\d+\s?\-?\s?l\s{1})",
    ],
    "millilitre":[
        r"(?:^\d+\.?\d+\s?\-?\s?millilitres\s?$)|(?:^\d+\s?\-?\s?millilitres\s?$)|(?:^\d+\.?\d+\s?\-?\s?millilitre\s?$)|(?:^\d+\s?\-?\s?millilitre\s?$)|(?:^\d+\.?\d+\s?\-?\s?ml\s?$)|(?:^\d+\s?\-?\s?ml\s?$)",
        r"(?:\s{1}\d+\.?\d+\s?\-?\s?millilitres\s{1})|(?:\s{1}\d+\s?\-?\s?millilitres\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?millilitre\s{1})|(?:\s{1}\d+\s?\-?\s?millilitre\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?ml\s{1})|(?:\s{1}\d+\s?\-?\s?ml\s{1})",
    ]
}


DIMENSION_REGEX = {
    "inch": [
        r"(?:^\d+\.?\d+\s?\-?\s?inches\s?$)|(?:^\d+\s?\-?\s?inches\s?$)|(?:^\d+\.?\d+\s?\-?\s?inch\s?$)|(?:^\d+\s?\-?\s?inch\s?$)|(?:^\d+\.?\d+\s?\-?\s?in\s?$)|(?:^\d+\s?\-?\s?in\s?$)|(?:^\d+\.?\d+\s?\-?\s?\"\s?$)|(?:^\d+\s?\-?\s?\"\s?$)",
        r"(?:\s{1}\d+\.?\d+\s?\-?\s?inches\s{1})|(?:\s{1}\d+\s?\-?\s?inches\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?inch\s{1})|(?:\s{1}\d+\s?\-?\s?inch\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?in\s{1})|(?:\s{1}\d+\s?\-?\s?in\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?\"\s{1})|(?:\s{1}\d+\s?\-?\s?\"\s{1})"
    ],
    "cm":[
        r"(?:^\d+\.?\d+\s?\-?\s?centimeters\s?$)|(?:^\d+\s?\-?\s?centimeters\s?$)|(?:^\d+\.?\d+\s?\-?\s?centimeter\s?$)|(?:^\d+\s?\-?\s?centimeter\s?$)|(?:^\d+\.?\d+\s?\-?\s?cms\s?$)|(?:^\d+\s?\-?\s?cms\s?$)|(?:^\d+\.?\d+\s?\-?\s?cm\s?$)|(?:^\d+\s?\-?\s?cm\s?$)",
        r"(?:\s{1}\d+\.?\d+\s?\-?\s?centimeters\s{1})|(?:\s{1}\d+\s?\-?\s?centimeters\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?centimeter\s{1})|(?:\s{1}\d+\s?\-?\s?centimeter\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?cms\s{1})|(?:\s{1}\d+\s?\-?\s?cms\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?cm\s{1})|(?:\s{1}\d+\s?\-?\s?cm\s{1})",
    ],
    "mm":[
        r"(?:^\d+\.?\d+\s?\-?\s?millimeters\s?$)|(?:^\d+\s?\-?\s?millimeters\s?$)|(?:^\d+\.?\d+\s?\-?\s?millimeter\s?$)|(?:^\d+\s?\-?\s?millimeter\s?$)|(?:^\d+\.?\d+\s?\-?\s?mm\s?$)|(?:^\d+\s?\-?\s?mm\s?$)",
        r"(?:\s{1}\d+\.?\d+\s?\-?\s?millimeters\s{1})|(?:\s{1}\d+\s?\-?\s?millimeters\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?millimeter\s{1})|(?:\s{1}\d+\s?\-?\s?millimeter\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?mm\s{1})|(?:\s{1}\d+\s?\-?\s?mm\s{1})",
    ],
    "meter":[
        r"(?:^\d+\.?\d+\s?\-?\s?meters\s?$)|(?:^\d+\s?\-?\s?meters\s?$)|(?:^\d+\.?\d+\s?\-?\s?mts\s?$)|(?:^\d+\s?\-?\s?mts\s?$)|(?:^\d+\.?\d+\s?\-?\s?m\s?$)|(?:^\d+\s?\-?\s?m\s?$)",
        r"(?:\s{1}\d+\.?\d+\s?\-?\s?meters\s{1})|(?:\s{1}\d+\s?\-?\s?meters\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?mts\s{1})|(?:\s{1}\d+\s?\-?\s?mts\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?m\s{1})|(?:\s{1}\d+\s?\-?\s?m\s{1})",
    ],
    "feet":[
        r"(?:^\d+\.?\d+\s?\-?\s?feets\s?$)|(?:^\d+\s?\-?\s?feets\s?$)|(?:^\d+\.?\d+\s?\-?\s?feet\s?$)|(?:^\d+\s?\-?\s?feet\s?$)|(?:^\d+\.?\d+\s?\-?\s?ft\s?$)|(?:^\d+\s?\-?\s?ft\s?$)|(?:^\d+\.?\d+\s?\-?\s?\'\s?$)|(?:^\d+\s?\-?\s?\'\s?$)",
        r"(?:\s{1}\d+\.?\d+\s?\-?\s?feets\s{1})|(?:\s{1}\d+\s?\-?\s?feets\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?feet\s{1})|(?:\s{1}\d+\s?\-?\s?feet\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?ft\s{1})|(?:\s{1}\d+\s?\-?\s?ft\s{1})|(?:\s{1}\d+\.?\d+\s?\-?\s?\'\s{1})|(?:\s{1}\d+\s?\-?\s?\'\s{1})"
    ],
}

MODEL_REGEX = [
    r"(\w+\d+\w+)((-){0,1})(\w+)((\/){0,1})((\w+)|(\d+)|(\w+))"
]

PROCESSOR_REGEX = {
    "intel": {
        "core":{
            "3": r"(\d{1,2}\w{2}\s+gen\s+intel\s+core\s+i3)|(intel\s+core\s+i3-\d+[a-z]\d\s+\d{1,2}\w{2}\s+gen)|(intel\s+core\s+i3\s+\d{1,2}\w{2}\s+gen)|(intel\s?core\s+i3\s?\-?\s?\d+\s?\w{2}\s{1})|(intel\s?i\s?3\s?\-\s?\d+\s?u\s{1})|(intel\s?core\s?i3\s{1})|(core\s?i\s?3\s?\d+?th\s?gen\s{1})|(core\s?i3+\s+processor\s{1})|(core\s+i\s?3+\s{1})",
            
            "5": r"(\d{1,2}\w{2}\s+gen\s+intel\s+core\s+i5)|(intel\s+core\s+i5-\d+[a-z]\d\s+\d{1,2}\w{2}\s+gen)|(intel\s+core\s+i5\s+\d{1,2}\w{2}\s+gen)|(intel\s?core\s+i5\s?\-?\s?\d+\s?\w{2}\s{1})|(intel\s?i\s?5\s?\-\s?\d+\s?u\s{1})|(intel\s?core\s?i5\s{1})|(core\s?i\s?5\s?\d+?th\s?gen\s{1})|(core\s?i5+\s+processor\s{1})|(core\s+i\s?5+\s{1})",
            
            "7": r"(\d{1,2}\w{2}\s+gen\s+intel\s+core\s+i7)|(intel\s+core\s+i7-\d+[a-z]\d\s+\d{1,2}\w{2}\s+gen)|(intel\s+core\s+i7\s+\d{1,2}\w{2}\s+gen)|(intel\s?core\s+i7\s?\-?\s?\d+\s?\w{2}\s{1})|(intel\s?i\s?7\s?\-\s?\d+\s?u\s{1})|(intel\s?core\s?i7\s{1})|(core\s?i\s?7\s?\d+?th\s?gen\s{1})|(core\s?i7+\s+processor\s{1})|(core\s+i\s?7+\s{1})",
            
            "9": r"(\d{1,2}\w{2}\s+gen\s+intel\s+core\s+i9)|(intel\s+core\s+i9-\d+[a-z]\d\s+\d{1,2}\w{2}\s+gen)|(intel\s+core\s+i9\s+\d{1,2}\w{2}\s+gen)|(intel\s?core\s+i9\s?\-?\s?\d+\s?\w{2}\s{1})|(intel\s?i\s?9\s?\-\s?\d+\s?u\s{1})|(intel\s?core\s?i9\s{1})|(core\s?i\s?9\s?\d+?th\s?gen\s{1})|(core\s?i9+\s+processor\s{1})|(core\s+i\s?9+\s{1})"
        }
    },
    "celeron":{
        "generic": r"(\d{1,2}\w{2}\s+gen\s+intel\s+celeron\s+n\d{4}\s+dual\s+core\s+processor\s?)|(intel\s+celeron\s+(?:nuc\s+-\s+nuc\d[a-z]*|n\d{4}\s+(?:processors|\d+\w{2}\s+gen))\s{1})|(intel\s+celeron\s+n\d+\s{1})|(intel\s+celeron\s+dual\s+core\s{1})|(celeron\s+dual\s+core\s+\d+?th\s+gen\s{1})|(celeron\s?quad\s?core\s{1})|(celeron\s+dual\s+core\s{1})"   
    },
    "ryzen":{
        "hexa": {
            "3": r"(ryzen\s?3\s+hexa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s{1})|(ryzen\s?3\s+hexa\s+core\s+\d+u\s{1})|(ryzen\s?3\s+hexa\s+core\s{1})",
            "5": r"(ryzen\s?5\s+hexa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s{1})|(ryzen\s?5\s+hexa\s+core\s+\d+u\s{1})|(ryzen\s?5\s+hexa\s+core\s{1})",
            "7": r"(ryzen\s?7\s+hexa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s{1})|(ryzen\s?7\s+hexa\s+core\s+\d+u\s{1})|(ryzen\s?7\s+hexa\s+core\s{1})",
            "9": r"(ryzen\s?9\s+hexa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s{1})|(ryzen\s?9\s+hexa\s+core\s+\d+u\s{1})|(ryzen\s?9\s+hexa\s+core\s{1})",
        },
        "octa":{
            "3": r"(ryzen\s?3\s+octa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s{1})|(ryzen\s?3\s+octa\s+core\s{1})",
            "5": r"(ryzen\s?5\s+octa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s{1})|(ryzen\s?5\s+octa\s+core\s{1})",
            "7": r"(ryzen\s?7\s+octa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s{1})|(ryzen\s?7\s+octa\s+core\s{1})",
            "9": r"(ryzen\s?9\s+octa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s{1})|(ryzen\s?9\s+octa\s+core\s{1})",
        },
        "quad":{
            "3": r"(ryzen\s?3\s+quad\s?core\s?\d+\w+\s?gen\s{1})",
            "5": r"(ryzen\s?5\s+quad\s?core\s?\d+\w+\s?gen\s{1})",
            "7": r"(ryzen\s?7\s+quad\s?core\s?\d+\w+\s?gen\s{1})",
            "9": r"(ryzen\s?9\s+quad\s?core\s?\d+\w+\s?gen\s{1})",
        },
        "dual":{
            "3": r"(ryzen\s?3\s+dual\s+core\s+\d+\s?u\s{1})|(ryzen\s?3\s+dual\s+core\s?amd\s?ryzen\s?3\s+\d+\s?u\s{1})",
            "5": r"(ryzen\s?3\s+dual\s+core\s+\d+\s?u\s{1})|(ryzen\s?5\s+dual\s+core\s?amd\s?ryzen\s?5\s+\d+\s?u\s{1})",
            "7": r"(ryzen\s?3\s+dual\s+core\s+\d+\s?u\s{1})|(ryzen\s?7\s+dual\s+core\s?amd\s?ryzen\s?7\s+\d+\s?u\s{1})",
            "9": r"(ryzen\s?3\s+dual\s+core\s+\d+\s?u\s{1})|(ryzen\s?9\s+dual\s+core\s?amd\s?ryzen\s?9\s+\d+\s?u\s{1})",
        },
        "hs":{
            "3": r"(\s+amd\s?ryzen\s?3\s?\d+hs\s{1})|(ryzen\s?3+\s+octa\s+core\s+\d+hs\s{1})",
            "5": r"(\s+amd\s?ryzen\s?5\s?\d+hs\s{1})|(ryzen\s?5+\s+octa\s+core\s+\d+hs\s{1})",
            "7": r"(\s+amd\s?ryzen\s?7\s?\d+hs\s{1})|(ryzen\s?7+\s+octa\s+core\s+\d+hs\s{1})",
            "9": r"(\s+amd\s?ryzen\s?9\s?\d+hs\s{1})|(ryzen\s?9+\s+octa\s+core\s+\d+hs\s{1})",
        },
        "hx":{
            "3": r"(\s?amd\s?ryzen\s?3\s?\d+hx\s{1})|(ryzen\s?3\s+octa\s+core\s+\d+hx\s{1})",
            "5": r"(\s?amd\s?ryzen\s?5\s?\d+hx\s{1})|(ryzen\s?5\s+octa\s+core\s+\d+hx\s{1})",
            "7": r"(\s?amd\s?ryzen\s?7\s?\d+hx\s{1})|(ryzen\s?7\s+octa\s+core\s+\d+hx\s{1})",
            "9": r"(\s?amd\s?ryzen\s?9\s?\d+hx\s{1})|(ryzen\s?9\s+octa\s+core\s+\d+hx\s{1})",
        }
    },
    "snapdragon":{
        "generic": r"(qualcomm\s?snapdragon\s?\d+\s?-\s?\d+\w+\s{1})|(qualcomm\s?snapdragon\s?\d+\w+\s{1})|(snapdragon\s+\d+\s?\w?\s+gen\s+\d+\s{1})|(snapdragon\s?\d+\w+\s+\d+\w+\s+processor\s{1})|(snapdragon\s?\d+\s?[345]g\s{1})|(snapdragon\s?\d+\s?)",
    },
    "helio":{
        "octa": r"(\d+\s?ghz\s?octa\s?-\s?core\s?helio\sg\d+\s?processor\s{1})|(\d+\s?ghz\s?octa\s?-\s?core\s?helio\sg\d+\s{1})|(\d+\s?ghz\s?octa\s?core\s?helio\s?g\d+\s{1})|(octa\s?-\s?core\s?helio\s?g\d+\s{1})",
        
        "generic": r"(helio\s?\w?\d+\s+processor\s{1})|(helio\s?\w?\d+\s{1})"
    },
    
    "dimensity":{
        "3": r"(dimensity\s?\d+\s?3g\s{1})|(dimensity\s?3\s{1})",
        "4": r"(dimensity\s?\d+\s?4g\s{1})|(dimensity\s?4\s{1})",
        "5": r"(dimensity\s?\d+\s?5g\s{1})|(dimensity\s?5\s{1})"
    }
}



FILTER_PROCESSOR_REGEX = {
    "gen": r"(\s\d+\s?th\s+gen\s?)|(?:^\d+\s?th\s+gen\s?)",
    "u_type": r"(-{0,1}\s?\d+\s?u\s?)",
    "nuc": r"(\snuc\d[a-z]*\s?)",
    "n": r"(\sn\d{4}\s?)|(\sn\d+\s?)",
    "h_type": r"(\s\d+hs\s{1})|(\s\d+hx\s{1})|(\sr\d+\s?\-?\d+\s?h\s{1})",
}


OS_REGEX = [
    r"(?:^windows\s?\d+\s?home\s?$)|(?:^chrome\s?os\s?$)|(?:^windows\s?\d+\s?$)|(?:^win\s?\d+\s?$)|(?:^chrome\s?\d+\s?$)"
]

GRAPHICS_REGEX = {
    
    "nvidia geforce": {
        "gtx":{
            "maxq" : r"(?:\d+gb\?nvidia\s?geforce\s?gtx\s?\d{4}\s?max\?q\s?gddr\d\s?)|(nvidia\s?geforce\s?gtx\s?\d{4}\s?max\?q\s?gddr\d\s?)|(nvidia\s?geforce\s?gtx\s?\d{4}\s?max\?q\s?\d+gb\s?gddr\d\s?)|(?:\d+gb\s?nvidia\s?geforce\s?gtx\s?\d{4}\s?max\?q\s?)|(nvidia\s?geforce\s?gtx\s?\d{4}\s?max\?q\s?\d+gb\s?)|(nvidia\s?geforce\s?gtx\s?\d{4}\s?max\s?q\s?)|(?:\d+gb\?nvidia\s?gtx\s?\d{4}\s?max\?q\s?gddr\d\s?)|(nvidia\s?gtx\s?\d{4}\s?max\?q\s?\d+gb\s?gddr\d\s?)|(nvidia\s?gtx\s?\d{4}\s?max\?q\s?gddr\d\s?)|(?:\d+gb\s?nvidia\s?gtx\s?\d{4}\s?max\?q\s?)|(nvidia\s?gtx\s?\d{4}\s?max\?q\s?\d+gb\s?)|(nvidia\s?gtx\s?\d{4}\s?max\s?q\s?)",
            
            "ti": r"(?:\d+gb\s?nvidia\s?geforce\s?gtx\s?\d{4}\s?ti\s?gddr\d\s?)|(nvidia\s?geforce\s?gtx\s?ti\s?\d{4}\s?ti\s?\d+gb\s?gddr\d\s?)|(?:\d+gb\s?nvidia\s?geforce\s?gtx\s?\d{4}\s?ti\s?)|(nvidia\s?geforce\s?gtx\s?ti\s?\d{4}\s?ti\s?\d+gb\s?)|(nvidia\s?geforce\s?gtx\s?\d{4}\s?ti\s?gddr\d\s?)|(nvidia\s?geforce\s?gtx\s?ti\s?\d{4}\s?ti\s?\d+gb\s?)|(?:\d+gb\s?nvidia\s?gtx\s?\d{4}\s?ti\s?gddr\d\s?)|(nvidia\s?gtx\s?ti\s?\d{4}\s?ti\s?\d+gb\s?gddr\d\s?)|(?:\d+gb\s?nvidia\s?gtx\s?\d{4}\s?ti\s?)|(nvidia\s?gtx\s?ti\s\d{4}\s?ti\s?\d+gb\s?)|(nvidia\s?gtx\s?\d{4}\s?ti\s?gddr\d\s?)|(nvidia\s?gtx\s?ti\s?\d{4}\s?ti\s?\d+gb\s?)|(nvidia\s?gtx\d{4}\s?ti\s?\d+gb\s?gddr\d\s?)",
            
            "generic": r"(?:\d+gb\s?nvidia\s?geforce\s?gtx\s?\d{4}\s?gddr\d\s?)|(nvidia\s?geforce\s?gtx\s?\d{4}\s?\d+gb\s?gddr\d\s?)|(?:\d+gb\s?nvidia\s?geforce\s?gtx\s?\d{4}\s?)|(nvidia\s?geforce\s?gtx\s?\d{4}\s?\d+gb\s?)|(?:\d+gb\s?nvidia\s?gtx\s?\d{4}\s?gddr\d\s?)|(nvidia\s?gtx\s?\d{4}\s?\d+gb\s?gddr\d\s?)|(?:\d+gb\s?nvidia\s?gtx\s?\d{4}\s?)|(nvidia\s?gtx\s?\d{4}\s?\d+gb\s?)|(gtx\s?\d{4}\s?)"  
        },

        "rtx": {
            "maxq": r"(?:\d+gb\?nvidia\s?geforce\s?rtx\s?\d{4}\s?max\?q\s?gddr\d\s?)|(nvidia\s?geforce\s?rtx\s?\d{4}\s?max\?q\s?gddr\d\s?)|(nvidia\s?geforce\s?rtx\s?\d{4}\s?max\?q\s?\d+gb\s?gddr\d\s?)|(?:\d+gb\s?nvidia\s?geforce\s?rtx\s?\d{4}\s?max\?q\s?)|(nvidia\s?geforce\s?rtx\s?\d{4}\s?max\?q\s?\d+gb\s?)|(nvidia\s?geforce\s?rtx\s?\d{4}\s?max\s?q\s?)|(?:\d+gb\?nvidia\s?rtx\s?\d{4}\s?max\?q\s?gddr\d\s?)|(nvidia\s?rtx\s?\d{4}\s?max\?q\s?\d+gb\s?gddr\d\s?)|(nvidia\s?rtx\s?\d{4}\s?max\?q\s?gddr\d\s?)|(?:\d+gb\s?nvidia\s?rtx\s?\d{4}\s?max\?q\s?)|(nvidia\s?rtx\s?\d{4}\s?max\?q\s?\d+gb\s?)|(nvidia\s?rtx\s?\d{4}\s?max\s?q\s?)",

            "ti": r"(?:\d+gb\s?nvidia\s?geforce\s?rtx\s?\d{4}\s?ti\s?gddr\d\s?)|(nvidia\s?geforce\s?rtx\s?ti\s?\d{4}\s?ti\s?\d+gb\s?gddr\d\s?)|(?:\d+gb\s?nvidia\s?geforce\s?rtx\s?\d{4}\s?ti\s?)|(nvidia\s?geforce\s?rtx\s?ti\s?\d{4}\s?ti\s?\d+gb\s?)|(nvidia\s?geforce\s?rtx\s?\d{4}\s?ti\s?gddr\d\s?)|(nvidia\s?geforce\s?rtx\s?ti\s?\d{4}\s?ti\s?\d+gb\s?)|(?:\d+gb\s?nvidia\s?rtx\s?\d{4}\s?ti\s?gddr\d\s?)|(nvidia\s?rtx\s?ti\s?\d{4}\s?ti\s?\d+gb\s?gddr\d\s?)|(?:\d+gb\s?nvidia\s?rtx\s?\d{4}\s?ti\s?)|(nvidia\s?rtx\s?ti\s\d{4}\s?ti\s?\d+gb\s?)|(nvidia\s?rtx\s?\d{4}\s?ti\s?gddr\d\s?)|(nvidia\s?rtx\s?ti\s?\d{4}\s?ti\s?\d+gb\s?)|(nvidia\s?rtx\d{4}\s?ti\s?\d+gb\s?gddr\d\s?)",

            "generic": r"(?:\d+gb\s?nvidia\s?geforce\s?rtx\s?\d{4}\s?gddr\d\s?)|(nvidia\s?geforce\s?rtx\s?\d{4}\s?\d+gb\s?gddr\d\s?)|(?:\d+gb\s?nvidia\s?geforce\s?rtx\s?\d{4}\s?)|(nvidia\s?geforce\s?rtx\s?\d{4}\s?\d+gb\s?)|(?:\d+gb\s?nvidia\s?rtx\s?\d{4}\s?gddr\d\s?)|(nvidia\s?rtx\s?\d{4}\s?\d+gb\s?gddr\d\s?)|(?:\d+gb\s?nvidia\s?rtx\s?\d{4}\s?)|(nvidia\s?rtx\s?\d{4}\s?\d+gb\s?)|(rtx\s?\d{4}\s?)"
        }
    },
    
    "intel":{
        "hd": r"(intel\s?hd\s?graphics\s?)",
        "uhd": r"(intel\s?uhd\s?graphics\s?)"
    },
    
    "generic": {
        "graphics": r"(?:\d+\s+tb\s+graphics\s?)|(?:\d+\s+gb\s+graphics\s?)|(?:\d+\s+mb\s+graphics\s?)"
    }
}

REPLACERS = r"(\,|\/|((\s)\-(\s))|((\s)\&(\s))|\+)"
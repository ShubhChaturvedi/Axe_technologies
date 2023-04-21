import pandas as pd
import re
import pymysql
import csv

PROCESSOR_REGEX = {
    "intel": {
        "core":{
            "3": r"(\d{1,2}\w{2}\s+gen\s+intel\s+core\s+i3\s?)|(intel\s+core\s+i3-\d+[a-z]\d\s+\d{1,2}\w{2}\s+gen\s?)|(intel\s+core\s+i3\s+\d{1,2}\w{2}\s+gen\s?)|(intel\s?core\s+i3\s?\-?\s?\d+\s?\w{2}\s?\d{1,2}\w{2}\s?gen\s?)|(intel\s?core\s+i3\s?\-?\s?\d+\s?\w{2}\s?)|(intel\s?i\s?3\s?\-\s?\d+\s?u\s?)|(intel\s?core\s?i3\s?)|(core\s?i\s?3\s?\d+?th\s?gen\s?)|(core\s?i3+\s+processor\s?)|(core\s+i\s?3+\s?)|(intel\s?i3\s?-\s?\w+\s?)|(intel\s?\d{1,2}th\s?gen\s?i3\s?)",
            
            "5": r"(\d{1,2}\w{2}\s+gen\s+intel\s+core\s+i5\s?)|(intel\s+core\s+i5-\d+[a-z]\d\s+\d{1,2}\w{2}\s+gen\s?)|(intel\s+core\s+i5\s+\d{1,2}\w{2}\s+gen\s?)|(intel\s?core\s+i5\s?\-?\s?\d+\s?\w{2}\s?\d{1,2}\w{2}\s?gen\s?)|(intel\s?core\s+i5\s?\-?\s?\d+\s?\w{2}\s?)|(intel\s?i\s?5\s?\-\s?\d+\s?u\s?)|(intel\s?core\s?i5\s?)|(core\s?i\s?5\s?\d+?th\s?gen\s?)|(core\s?i5+\s+processor\s?)|(core\s+i\s?5+\s?)|(intel\s?i5\s?-\s?\w+\s?)|(intel\s?\d{1,2}th\s?gen\s?i5\s?)|(\d{1}?th\s?gen\s?ci5\s?)",
            
            "7": r"(\d{1,2}\w{2}\s+gen\s+intel\s+core\s+i7\s?)|(intel\s+core\s+i7-\d+[a-z]\d\s+\d{1,2}\w{2}\s+gen\s?)|(intel\s+core\s+i7\s+\d{1,2}\w{2}\s+gen\s?)|(intel\s?core\s+i7\s?\-?\s?\d+\s?\w{2}\s?\d{1,2}\w{2}\s?gen\s?)|(intel\s?core\s+i7\s?\-?\s?\d+\s?\w{2}\s?)|(intel\s?i\s?7\s?\-\s?\d+\s?u\s?)|(intel\s?core\s?i7\s?)|(core\s?i\s?7\s?\d+?th\s?gen\s?)|(core\s?i7+\s+processor\s?)|(core\s+i\s?7+\s?)|(intel\s?i7\s?-\s?\w+\s?)|(intel\s?\d{1,2}th\s?gen\s?i7\s?)",
            
            "9": r"(\d{1,2}\w{2}\s+gen\s+intel\s+core\s+i9\s?)|(intel\s+core\s+i9-\d+[a-z]\d\s+\d{1,2}\w{2}\s+gen\s?)|(intel\s+core\s+i9\s+\d{1,2}\w{2}\s+gen\s?)|(intel\s?core\s+i9\s?\-?\s?\d+\s?\w{2}\s?\d{1,2}\w{2}\s?gen\s?)|(intel\s?core\s+i9\s?\-?\s?\d+\s?\w{2}\s?)|(intel\s?i\s?9\s?\-\s?\d+\s?u\s?)|(intel\s?core\s?i9\s?)|(core\s?i\s?9\s?\d+?th\s?gen\s?)|(core\s?i9+\s+processor\s?)|(core\s+i\s?9+\s?)|(intel\s?i9\s?-\s?\w+\s?)|(intel\s?\d{1,2}th\s?gen\s?i9\s?)"
        },
        "celeron":{
            "generic": r"(\d{1,2}\w{2}\s+gen\s+intel\s+celeron\s+n\d{4}\s+dual\s+core\s+processor\s?)|(intel\s+celeron\s+(?:nuc\s+-\s+nuc\d[a-z]*|n\d{4}\s+(?:processors|\d+\w{2}\s+gen))\s{1})|(intel\s+celeron\s+n\d+\s?)|(intel\s+celeron\s+dual\s+core\s?)|(celeron\s+dual\s+core\s+\d+?th\s+gen\s?)|(celeron\s?quad\s?core\s?)|(celeron\s+dual\s+core\s?)"   
        },
        "pentium":{
            "quad":r"(pentium\s?quad\s?core\s?\d{1,2}th\s?gen\s?)|(pentium\s?quad\s?core\s?)",
            "gold":r"(pentium\s?gold\s?)"
        },
        "atom":{
            "generic":r"(atom\s?quad\s?core\s?)"
        }
    },
    "amd": {
        "athlon":{
            "dual": r"(athlon\s?dual\s?core\s?\d+u\s?)|(athlon\s?dual\s?core\s?)",
            "generic": r"(amd\s?athlon\s?)"
        },
    },
    "ryzen":{
        "hexa": {
            "3": r"(ryzen\s?3\s+hexa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s?)|(ryzen\s?3\s+hexa\s+core\s+\d+u\s?)|(ryzen\s?3\s+hexa\s+core\s?)",
            "5": r"(ryzen\s?5\s+hexa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s?)|(ryzen\s?5\s+hexa\s+core\s+\d+u\s?)|(ryzen\s?5\s+hexa\s+core\s?)",
            "7": r"(ryzen\s?7\s+hexa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s?)|(ryzen\s?7\s+hexa\s+core\s+\d+u\s?)|(ryzen\s?7\s+hexa\s+core\s?)",
            "9": r"(ryzen\s?9\s+hexa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s?)|(ryzen\s?9\s+hexa\s+core\s+\d+u\s?)|(ryzen\s?9\s+hexa\s+core\s?)",
        },
        "octa":{
            "3": r"(ryzen\s?3\s+octa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s?)|(ryzen\s?3\s+octa\s+core\s?)",
            "5": r"(ryzen\s?5\s+octa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s?)|(ryzen\s?5\s+octa\s+core\s?)",
            "7": r"(ryzen\s?7\s+octa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s?)|(ryzen\s?7\s+octa\s+core\s?)",
            "9": r"(ryzen\s?9\s+octa\s+core\s+amd\s?r\d+\s?\-?\d+\s?h\s?)|(ryzen\s?9\s+octa\s+core\s?)",
        },
        "quad":{
            "3": r"(ryzen\s?3\s+quad\s?core\s?\d+\w+\s?gen\s?)|(ryzen\s?3\s?quad\s?core\s?)",
            "5": r"(ryzen\s?5\s+quad\s?core\s?\d+\w+\s?gen\s?)|(ryzen\s?5\s?quad\s?core\s?)",
            "7": r"(ryzen\s?7\s+quad\s?core\s?\d+\w+\s?gen\s?)|(ryzen\s?7\s?quad\s?core\s?)",
            "9": r"(ryzen\s?9\s+quad\s?core\s?\d+\w+\s?gen\s?)|(ryzen\s?9\s?quad\s?core\s?)",
        },
        "dual":{
            "3": r"(ryzen\s?3\s+dual\s+core\s+\d+\s?u\s?)|(ryzen\s?3\s+dual\s+core\s?amd\s?ryzen\s?3\s+\d+\s?u\s?)|(ryzen\s?3\s?dual\s?core\s?)",
            "5": r"(ryzen\s?3\s+dual\s+core\s+\d+\s?u\s?)|(ryzen\s?5\s+dual\s+core\s?amd\s?ryzen\s?5\s+\d+\s?u\s?)|(ryzen\s?5\s?dual\s?core\s?)",
            "7": r"(ryzen\s?3\s+dual\s+core\s+\d+\s?u\s?)|(ryzen\s?7\s+dual\s+core\s?amd\s?ryzen\s?7\s+\d+\s?u\s?)|(ryzen\s?7\s?dual\s?core\s?)",
            "9": r"(ryzen\s?3\s+dual\s+core\s+\d+\s?u\s?)|(ryzen\s?9\s+dual\s+core\s?amd\s?ryzen\s?9\s+\d+\s?u\s?)|(ryzen\s?9\s?dual\s?core\s?)",
        },
        "hs":{
            "3": r"(\s+amd\s?ryzen\s?3\s?\d+hs\s?)|(ryzen\s?3+\s+octa\s+core\s+\d+hs\s?)",
            "5": r"(\s+amd\s?ryzen\s?5\s?\d+hs\s?)|(ryzen\s?5+\s+octa\s+core\s+\d+hs\s?)",
            "7": r"(\s+amd\s?ryzen\s?7\s?\d+hs\s?)|(ryzen\s?7+\s+octa\s+core\s+\d+hs\s?)",
            "9": r"(\s+amd\s?ryzen\s?9\s?\d+hs\s?)|(ryzen\s?9+\s+octa\s+core\s+\d+hs\s?)",
        },
        "hx":{
            "3": r"(\s?amd\s?ryzen\s?3\s?\d+hx\s?)|(ryzen\s?3\s+octa\s+core\s+\d+hx\s?)",
            "5": r"(\s?amd\s?ryzen\s?5\s?\d+hx\s?)|(ryzen\s?5\s+octa\s+core\s+\d+hx\s?)",
            "7": r"(\s?amd\s?ryzen\s?7\s?\d+hx\s?)|(ryzen\s?7\s+octa\s+core\s+\d+hx\s?)",
            "9": r"(\s?amd\s?ryzen\s?9\s?\d+hx\s?)|(ryzen\s?9\s+octa\s+core\s+\d+hx\s?)",
        },
        "apu":{
            "generic":{
                "e": r"(apu\s?dual\s?core\s?e[1-9]\s?e[1-9]\s?-{1}\s?\d+\s?\d{1,2}th\s?gen\s?)|(apu\s?dual\s?core\s?e[1-9]\s?e[1-9]\s?\-{1}\s?\d+\s?\d{1,2}th\s?gen\s?)|(apu\s?dual\s?core\s?e[1-9]\s?e[1-9]\s?\-{1}\s?\d{1,2}th\s?gen\s?)|(apu\s?dual\s?core\s?e[1-9]\s?e[1-9]\-{1}\d+\s?)|(apu\s?dual\s?core\s?e[1-9]\s?e[1-9]\s?\s?\d+\s?\d{1,2}th\s?gen\s?)|(apu\s?dual\s?core\s?e[1-9]\s?\d+\s?\d{1,2}\s?th\s?gen\s?)|(apu\s?dual\s?core\s?e[1-9]\s?\d{1,2}th\s?gen\s?)|(apu\s?dual\s?core\s?e[1-9]\s?e[1-9]\d+\s?)",
                "a": r"(apu\s?dual\s?core\s?a[1-9]\s?a[1-9]\s?-{1}\s?\d+\s?\d{1,2}th\s?gen\s?)|(apu\s?dual\s?core\s?a[1-9]\s?a[1-9]\s?\-{1}\s?\d+\s?\d{1,2}th\s?gen\s?)|(apu\s?dual\s?core\s?a[1-9]\s?a[1-9]\s?\-{1}\s?\d{1,2}th\s?gen\s?)|(apu\s?dual\s?core\s?a[1-9]\s?a[1-9]\-{1}\d+\s?)|(apu\s?dual\s?core\s?a[1-9]\s?a[1-9]\s?\s?\d+\s?\d{1,2}th\s?gen\s?)|(apu\s?dual\s?core\s?a[1-9]\s?\d+\s?\d{1,2}\s?th\s?gen\s?)|(apu\s?dual\s?core\s?a[1-9]\s?\d{1,2}th\s?gen\s?)|(apu\s?dual\s?core\s?a[1-9]\s?a[1-9]\d+\s?)"
            }
        },
        "generic":{
            "3": r"(amd\s?\d+th\s?gen\s?ryzen\s?3\s?)|(amd\s?r3\s?\d+u\s?)|(amd\s?ryzen\s?3\s?-\s?\d+u\s?)",
            "5": r"(amd\s?\d+th\s?gen\s?ryzen\s?5\s?)|(amd\s?r5\s?\d+u\s?)|(amd\s?ryzen\s?5\s?-\s?\d+u\s?)",
            "7": r"(amd\s?\d+th\s?gen\s?ryzen\s?7\s?)|(amd\s?r7\s?\d+u\s?)|(amd\s?ryzen\s?7\s?-\s?\d+u\s?)",
            "9": r"(amd\s?\d+th\s?gen\s?ryzen\s?9\s?)|(amd\s?r9\s?\d+u\s?)|(amd\s?ryzen\s?9\s?-\s?\d+u\s?)",
            "generic": r"(amd\s?ryzen\s?)"
        }
    },
    "snapdragon":{
        "generic": r"(qualcomm\s?snapdragon\s?\d+\s?-\s?\d+\w+\s?)|(qualcomm\s?snapdragon\s?\d+\w+\s?)|(snapdragon\s+\d+\s?\w?\s+gen\s+\d+\s?)|(snapdragon\s?\d+\w+\s+\d+\w+\s+processor\s?)|(snapdragon\s?\d+\s?[345]g\s?)|(snapdragon\s?\d+\s?)",
    },
    "meidatek":{
        "helio":{
            "octa": r"(\d+\s?ghz\s?octa\s?-\s?core\s?helio\sg\d+\s?processor\s?)|(\d+\s?ghz\s?octa\s?-\s?core\s?helio\sg\d+\s?)|(\d+\s?ghz\s?octa\s?core\s?helio\s?g\d+\s?)|(octa\s?-\s?core\s?helio\s?g\d+\s?)",

            "generic": r"(helio\s?\w?\d+\s+processor\s?)|(helio\s?\w?\d+\s?)"
        },
        "dimensity":{
            "3": r"(dimensity\s?\d+\s?3g\s?)|(dimensity\s?3\s?)",
            "4": r"(dimensity\s?\d+\s?4g\s?)|(dimensity\s?4\s?)",
            "5": r"(dimensity\s?\d+\s?5g\s?)|(dimensity\s?5\s?)"
        },
        "kompanio": {
            "500":{
                "mt8183":r"(mediatek\s?mt8183\s?kompanio\s?500\s?)|(mediatek\s?mt8183\s?)",
                "generic": r"(mediatek\s?kompanio\s?500\s?)"
            },
            "520":{
                "generic": r"(mediatek\s?kompanio\s?520\s?)|(kompanio\s?520\s?)|(mediatek\s?520\s?)"
            },
            "528":{
                "generic": r"(mediatek\s?kompanio\s?528\s?)|(kompanio\s?528\s?)|(mediatek\s?528\s?)"
            },
            "820":{
                "mt8192":r"(mediatek\s?mt8192\s?kompanio\s?820\s?)|(mediatek\s?mt8192\s?)",
                "generic": r"(mediatek\s?kompanio\s?820\s?)"
            },
            "828":{
                "generic": r"(mediatek\s?kompanio\s?828\s?)|(kompanio\s?828\s?)|(mediatek\s?828\s?)"
            },
            "900t":{
                "mt8791":r"(mediatek\s?mt8791\s?kompanio\s?900t\s?)|(mediatek\s?mt8791\s?)",
                "generic": r"(mediatek\s?kompanio\s?900t\s?)"
            },
            "1200":{
                "mt8195":r"(mediatek\s?mt8195\s?kompanio\s?1200\s?)|(mediatek\s?mt8195\s?)",
                "generic": r"(mediatek\s?kompanio\s?1200\s?)"
            },
            "1380":{
                "mt8195t":r"(mediatek\s?mt8195t\s?kompanio\s?1380\s?)|(mediatek\s?mt8195t\s?)",
                "generic": r"(mediatek\s?kompanio\s?1380\s?)"
            },
            "1300t":{
                "mt8797":r"(mediatek\s?mt8797\s?kompanio\s?1300t\s?)|(mediatek\s?mt8797\s?)",
                "generic": r"(mediatek\s?kompanio\s?1300t\s?)"
            },
            "mt":{
                "mt8317":r"(mediatek\s?my8317\s?)|(mt8317\s?)",
                "mt8317t":r"(mediatek\s?mt8317t\s?)|(mt8317t\s?)",
                "mt8377":r"(mediatek\s?mt8377\s?)|(mt8377\s?)",
                "mt8312":r"(mediatek\s?mt8312\s?)|(mt8312\s?)",
                "mt8321":r"(mediatek\s?mt8321\s?)|(mt8321\s?)",
                "mt8382":r"(mediatek\s?mt8382\s?)|(mt8382\s?)",
                "mt8117":r"(mediatek\s?mt8117\s?)|(mt8117\s?)",
                "mt8121":r"(mediatek\s?mt8121\s?)|(mt8121\s?)",
                "mt8125":r"(mediatek\s?mt8125\s?)|(mt8125\s?)",
                "mt8389":r"(mediatek\s?mt8389\s?)|(mt8389\s?)",
                "mt8389t":r"(mediatek\s?mt8389t\s?)|(mt8389t\s?)",
                "mt8135":r"(mediatek\s?mt8135\s?)|(mt8135\s?)",
                "mt8135v":r"(mediatek\s?mt8135v\s?)|(mt8135v\s?)",
                "mt8127":r"(mediatek\s?mt8127\s?)|(mt8127\s?)",
                "mt8151":r"(mediatek\s?mt8151\s?)|(mt8151\s?)",
                "mt8392":r"(mediatek\s?mt8392\s?)|(mt8392\s?)",
                "mt8735":r"(mediatek\s?mt8735\s?)|(mt8735\s?)",
                "mt8732":r"(mediatek\s?mt8732\s?)|(mt8732\s?)",
                "mt8752":r"(mediatek\s?mt8752\s?)|(mt8752\s?)",
                "mt8161":r"(mediatek\s?mt8161\s?)|(mt8161\s?)",
                "mt8163v":r"(mediatek\s?mt8163v\s?)|(mt8163v\s?)",
                "mt8163b":r"(mediatek\s?mt8163b\s?)|(mt8163b\s?)",
                "mt8163v":r"(mediatek\s?mt8163v\s?)|(mt8163v\s?)",
                "mt8163a":r"(mediatek\s?mt8163a\s?)|(mt8163a\s?)",
                "mt8165":r"(mediatek\s?mt8165\s?)|(mt8165\s?)",
                "mt8166":r"(mediatek\s?mt8166\s?)|(mt8166\s?)",
                "mt8167A":r"(mediatek\s?mt8167A\s?)|(mt8167A\s?)",
                "mt8173":r"(mediatek\s?mt8173\s?)|(mt8173\s?)",
                "mt8176":r"(mediatek\s?mt8176\s?)|(mt8176\s?)",
                "mt8766":r"(mediatek\s?mt8766\s?)|(mt8766\s?)",
                "mt8768t":r"(mediatek\s?mt8768t\s?)|(mt8768t\s?)",
                "mt8693":r"(mediatek\s?mt8693\s?)|(mt8693\s?)",
                "mt5327":r"(mediatek\s?mt5327\s?)|(mt5327\s?)",
                "mt5329":r"(mediatek\s?mt5329\s?)|(mt5329\s?)",
                "mt5366":r"(mediatek\s?mt5366\s?)|(mt5366\s?)",
                "mt5389":r"(mediatek\s?mt5389\s?)|(mt5389\s?)",
                "mt5395":r"(mediatek\s?mt5395\s?)|(mt5395\s?)",
                "mt5396":r"(mediatek\s?mt5396\s?)|(mt5396\s?)",
                "mt5398":r"(mediatek\s?mt5398\s?)|(mt5398\s?)",
                "mt5505":r"(mediatek\s?mt5505\s?)|(mt5505\s?)",
                "mt5561":r"(mediatek\s?mt5561\s?)|(mt5561\s?)",
                "mt5580":r"(mediatek\s?mt5580\s?)|(mt5580\s?)",
                "mt5582":r"(mediatek\s?mt5582\s?)|(mt5582\s?)",
                "mt5592":r"(mediatek\s?mt5592\s?)|(mt5592\s?)",
                "mt5595":r"(mediatek\s?mt5595\s?)|(mt5595\s?)",
                "mt5596":r"(mediatek\s?mt5596\s?)|(mt5596\s?)",
                "mt5597":r"(mediatek\s?mt5597\s?)|(mt5597\s?)",
                "mt9638":r"(mediatek\s?mt9638\s?)|(mt9638\s?)",
                "mt9675":r"(mediatek\s?mt9675\s?)|(mt9675\s?)",
                "mt9632":r"(mediatek\s?mt9632\s?)|(mt9632\s?)",
                "mt9602":r"(mediatek\s?mt9602\s?)|(mt9602\s?)",
                "mt9685":r"(mediatek\s?mt9685\s?)|(mt9685\s?)",
                "mt9612":r"(mediatek\s?mt9612\s?)|(mt9612\s?)",
                "mt9686":r"(mediatek\s?mt9686\s?)|(mt9686\s?)",
                "mt9652":r"(mediatek\s?mt9652\s?)|(mt9652\s?)",
                "mt9613":r"(mediatek\s?mt9613\s?)|(mt9613\s?)",
                "mt9950":r"(mediatek\s?mt9950\s?)|(mt9950\s?)",
                "mt5895":r"(mediatek\s?mt5895\s?)|(mt5895\s?)",
                "mt9970a":r"(mediatek\s?mt9970a\s?)|(mt9970a\s?)"
            },
        }
    },
    "apple":{
        "m1":{
            "max":r"(apple\s?m1\s?max\s?)|(m1\s?max\s?)",
            "pro":r"(apple\s?m1\s?pro\s?)|(m1\s?pro\s?)",
            "generic":r"(apple\s?m1\s?)|(m1\s?)"
        },
        "m2":{
            "max":r"(apple\s?m2\s?max\s?)",
            "pro":r"(apple\s?m2\s?pro\s?)",
            "generic":r"(apple\s?m2\s?)|(m2\s?)"
        },
        "a_series":{
            "a4": r"(apple\?a4\?)",
            "a5":r"(apple\?a5\?)",
            "a5x":r"(apple\?a5x\?)",
            "a6":r"(apple\?a6\?)",
            "a7":r"(apple\?a7\?)",
            "a8":r"(apple\?a8\?)",
            "a8x":r"(apple\?a8x\?)",
            "a9":r"(apple\?a9\?)",
            "a9x":r"(apple\?a9x\?)",
            "a10_fusion":r"(apple\s?a10\?fusion\s?)",
            "a10x_fusion":r"(apple\s?a10x\?fusion\s?)",
            "a11_bionic":r"(apple\s?a11\?bionic\s?)",
            "a12_bionic":r"(apple\s?a12\?bionic\s?)",
            "a12x_bionic":r"(apple\s?a12x\?bionic\s?)",
            "a12z_bionic":r"(apple\s?a12z\?bionic\s?)",
            "a13_bionic":r"(apple\s?a13\?bionic\s?)",
            "a14_bionic":r"(apple\s?a14\?bionic\s?)",
            "a15_bionic":r"(apple\s?a15\?bionic\s?)",
            "a16_bionic":r"(apple\s?a16\?bionic\s?)",
        },
        "m_series":{
            "m7":r"(apple\s?m7\s?)",
            "m8":r"(apple\s?m8\s?)",
        },
        "s_series":{
            "s1":r"(apple\s?s1\s?)",
            "s1p":r"(apple\s?s1p\s?)",
            "s2":r"(apple\s?s2\s?)",
            "s3":r"(apple\s?s3\s?)",
            "s4":r"(apple\s?s4\s?)",
            "s5":r"(apple\s?s5\s?)",
            "s6":r"(apple\s?s6\s?)",
            "s7":r"(apple\s?s7\s?)",
            "s8":r"(apple\s?s8\s?)",
        },
        "w_series":{
            "w1":r"(apple\s?w1\s?)",
            "w2":r"(apple\s?w2\s?)",
            "w3":r"(apple\s?w3\s?)"
        },
        "u_series":{
            "u1":r"(apple\s?u1\s?)"
        }
        
    }
    
}


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



FILTER_PROCESSOR_REGEX = {
    "gen": r"(\s\d+\s?th\s+gen\s?)|(?:^\d+\s?th\s+gen\s?)",
    "u_type": r"(-{0,1}\s?\d+\s?u\s?)",
    "nuc": r"(\snuc\d[a-z]*\s?)",
    "n": r"(\sn\d{4}\s?)|(\sn\d+\s?)",
    "h_type": r"(\s\d+hs\s{1})|(\s\d+hx\s{1})|(\sr\d+\s?\-?\d+\s?h\s{1})",
}


#=================================================================
# CLASSIFIER FUNCTION -- PROCESSOR
#=================================================================
def processor_regex_mapper(product_name_group=""):

    for a,b in STORAGE_REGEX.items():
        for c,d in b.items():
            if isinstance(d, dict):
                for key,val in d.items():
                    
                    if isinstance(val, dict):
                        for key_1,val_1 in val.items():
                            matched = re.search(val_1, product_name_group.strip())
                            if matched:
                                return matched.group(0).strip()
                            
                    else:
                        matched = re.search(val, product_name_group.strip())
                        if matched:
                            return matched.group(0).strip()
            else:
                matched = re.search(d, product_name_group.strip())

                if matched:
                    return matched.group(0).strip()
    return False


connection = pymysql.connect(
    host='localhost',
    user='shubh-compare',
    password='Shubh1710',
    database='compare_app',
    cursorclass=pymysql.cursors.DictCursor
)


qsql = "select id, product_title, category_id, product_id from all_products where is_active=1 and category_id = 90"


# print(qsql)
with connection.cursor() as cursor:
    cursor.execute(qsql)
    record_set = cursor.fetchall()
    
    cpu_csv = []
    
    
    for row in record_set:
        
        xx = processor_regex_mapper(row["product_title"].lower())
        
        if xx:
            cpu_csv.append(xx)
            val = xx
            print(row["product_title"].lower(), True)
            # write to csv
            with open('storage-laptop-true.csv', mode='a', newline='') as file:
                # Create a writer object
                writer = csv.writer(file)
                writer.writerow([row["product_id"], row["product_title"]])
            # insert into datastore_classifier - processor
            # try:
            #     insert_qry = """insert into app_datastore_classifier ( product_id, processor, category_id) values (%s, %s, %s)"""
            #     val = (row["product_id"], xx, row["category_id"])

            #     cursor.execute(insert_qry, val)
            #     connection.commit()
            #     print(cursor._last_executed)
            # except Exception as msg:
            #     print(msg)

            print(xx)
            print()
            
        else:
            print()
            print(row["product_title"].lower(), False)
            # write to csv
            with open('storage-laptop-false.csv', mode='a', newline='') as file:
            # Create a writer object
                writer = csv.writer(file)
                writer.writerow([row["product_id"] ,row["product_title"]])
        
        
    print(cpu_csv)



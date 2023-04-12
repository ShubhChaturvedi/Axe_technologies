import pandas as pd
import re
import pymysql
import numpy as np
import os
import sys
import requests
import urllib.parse
import csv
import json

from collections import OrderedDict, defaultdict

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

# Connect to the database
#================================================================
def db_connect():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='shubh-compare',
            password='Shubh1710',
            database='compare_app',
            cursorclass=pymysql.cursors.DictCursor
        )
            
        return connection
    except Exception as e:
        print("Could not connect to database: {}".format(e))
        return None

# Dynamic imports path
#================================================================
helpers_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(helpers_dir)

import regexFile, stop_words, colors_list


#=================================================================
# Constants
#=================================================================

BRANDS_FILE = os.path.join(os.getcwd(), 'brands_list.csv')
# print("Bran")
# print()
# print(BRANDS_FILE)
BRANDS_JSON = os.path.join(os.getcwd(), 'brands_list.json')

REPLACERS = r"(\,|\/|((\s)\-(\s))|((\s)\&(\s))|\+)"

SUBSCRIPTION_KEY = "24586d64cce94c6baeee90dbed141c1b"
API_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"
SUBSCRIPTION_KEY = ""
API_ENDPOINT = "https://www.google.com/search"

REGISTERED_URLS = [
    "www.amazon.in",
    "www.flipkart.com",
    "www.vijaysales.com",
    "www.reliancedigital.in",
    "www.samsung.com"
]

#=================================================================
# Data Writers Class
#=================================================================

class DataWriter():
    
    def __init__(self):
        self.connection = db_connect()
    
    # Save data into app_datastore table for future reference
    #================================================================
    def create_dataset(self):
        pass

    

#=================================================================
# Bing Search API Class
#=================================================================

class BingSearchApi():
    
    # Initializing class
    #
    # product_name <string> <optional depending on condition called>
    # product_id <integer> <optional depending on condition called>
    # product_data <dictionary> <optional depending on condition called>
    # main_product <boolean> <if called on the product in db or on bing search product name>
    # compare_data <list> <used for storing comparision data>
    # search_results <list> <used to store search results>
    #================================================================
    
    def __init__(self):
        
        self.product_data = None
        self.product_id = None 
        self.product_model_no = None
        self.product_part_number = None
        self.product_brand = None
        self.main_product = True
        self.compare_data = []
        self.search_results = []
        self.length_serach_list = 0
        self.x=1
        
        self.brands_list = []
        
        # Container for storing bing search reasults
        self.product_list = [] 
        
        # create brands list
        
        if os.path.exists(BRANDS_JSON):
            self.brands_list = self.read_brands_json()
        else:
            self.read_brands_csv(create_json=True)
            self.brands_list = self.read_brands_json()
        
        
    #=================================================================
    # CREATE BRANDS FILE
    #=================================================================

    def create_brands_csv(self):
        
        connection = db_connect()
        
        df = None
        
        if connection:
            
            qry = "select brand_name from app_productbrands"

            with connection.cursor() as cursor:
                cursor.execute(qry)

                if cursor.rowcount > 0:
                    recordset = cursor.fetchall()
                    df = pd.DataFrame.from_records(recordset)
                else:
                    return False

            df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)

            df = df.applymap(lambda x: x.replace('"', '').replace('.','').replace('*', '').replace("?", "").strip() if isinstance(x, str) else x)
            df = df.replace(r'^\s*$', np.nan, regex=True)
            df = df.dropna()
            df = df.drop_duplicates(subset='brand_name')
            df = df.sort_values(by="brand_name")

            df.to_csv(BRANDS_FILE, index=False)

            return True
        
    #=================================================================
    # READ BRANDS FILE -- RETURN TUPLE
    #=================================================================

    def read_brands_csv(self, create_json=False):
        if os.path.exists(BRANDS_FILE):
            brand_dict = defaultdict()
            with open(BRANDS_FILE, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # exclude header
                
                for row in reader:
                    x = str(row[0].strip())

                    xx = re.split(r"[\s\(\)\/,.\|]",x)
                    
                    if xx[0] in brand_dict.keys():
                        brand_dict[xx[0]].append(x)
                    else:
                        if xx[0] not in ("buy",):
                            brand_dict.update({xx[0]:[]})
                            brand_dict[xx[0]].append(x)
            
            if create_json:
                with open(BRANDS_JSON, "w") as outfile:
                    json.dump(brand_dict, outfile)  
        else:
            self.create_brands_csv()      
    
        return brand_dict
    
    #=================================================================
    # CREATE BRANDS FILE -- RETURN JSON
    #=================================================================
    
    def read_brands_json(self):
        brands_list = {}
        with open(BRANDS_JSON, "r") as output:
            brands_list = json.load(output)
        return brands_list
        
    #================================================================
    # Get Product details only if main/master product
    #================================================================
    def fetch_product_details(self):
        qry = """
            select product_title, product_model_no, product_part_number, product_brand from all_products where product_id = {}
        """.format(self.product_id)
        
        record_set = []
        with self.db_connect.cursor() as cursor: 
            cursor.execute(qry)
            
            if cursor.rowcount > 0:
                record_set = cursor.fetchone()
                self.product_name = record_set["product_title"]
                self.product_model_no = record_set["product_model_no"]
                self.product_part_number = record_set["product_part_number"]
                self.product_brand = record_set["product_brand"]
                
                return True
        return False
    
    #=================================================================
    # Bing API Call -- Function 
    # returns search results from bing
    #=================================================================
    def call_bing_api(self, query=""):
        
        if query.strip()=="":
            return False
    
        # Construct a request
        #=================================================================
        mkt = 'en-US'
        params = { 'q': query, 'answerCount':2}
        headers = { 'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY }

        product_list = []
        
        try:
            response = requests.get(API_ENDPOINT, headers=headers, params=params)
            response.raise_for_status()

            results = response.json()
            
            for product in results["webPages"]["value"]:        
                o = urllib.parse.urlsplit(product["url"])

                if o.hostname in REGISTERED_URLS:
                    
                    product_list.append({
                        "url": product["url"],
                        "snippet": product["snippet"],
                        "name": product["name"]
                    })
            # print(product_list)
            # print()
            # print()
            return product_list
        
        except Exception as ex:
            return False    
    
    
    #=================================================================
    # CLASSIFIER FUNCTION -- MULTI 
    #=================================================================
    def regex_mapper(self, data_dict={}, product_name_group=[], data_dict_key="", pattern=[]):
        
        v = 0
        while v < len(product_name_group):
            for x in pattern:
                try:
                    matched = re.search(x, product_name_group[v].strip())
                except IndexError:
                    return data_dict, product_name_group
                
                if matched:
                    data_dict[data_dict_key].append(matched.group(0).strip())
                    product_name_group.remove(product_name_group[v])
                    v = 0
                    break
            else:
                v +=1 
                
        return data_dict, product_name_group
    
    #=================================================================
    # CLASSIFIER FUNCTION -- DIMENSIONS 
    #=================================================================
    def dimension_regex_mapper(self, data_dict={}, product_name_group=[], data_dict_key="", pattern=[]):
        
        v = 0
        pattern_keys = pattern.keys()
        
        while v < len(product_name_group):
            
            try:
                p_name = product_name_group[v].strip()
            except IndexError:
                return data_dict, product_name_group
            
            if "/" in p_name:
                splitter = p_name.split("/")
                product_name_group[v] = splitter[0]
                product_name_group += splitter[1:]
                
            for x in pattern_keys:
                for val in pattern[x]:
                    try:
                        matched = re.search(val, product_name_group[v].strip())
                    except IndexError:
                        return data_dict, product_name_group

                    if matched:
                        xx = matched.group(0).strip()
                        
                        found = matched.span()
                        df = re.search(r"(?:^\d+\.?\d+\s?)", xx)
                        
                        if df:
                            data_dict[data_dict_key].update({x:df.group(0).strip()})
                        
                        if found[0] > 0:
                            product_name_group[v] = product_name_group[v].replace(product_name_group[v][found[0]:found[1]-1], "")
                        else:
                            product_name_group.remove(product_name_group[v])
                        v = 0
                        break
            else:
                v +=1 
                
        return data_dict, product_name_group
    
    #=================================================================
    # CLASSIFIER FUNCTION -- STORAGE
    #=================================================================
    def storage_regex_mapper(self, data_dict={}, product_name_group=[], data_dict_key="", pattern=None):
        if not bool(data_dict[data_dict_key]):
            v = 0
            while v < len(product_name_group):
                found = False
                for u,t in pattern.items():
                    for x,y in t.items():
                        
                        try:
                            matched = re.search(y, product_name_group[v].strip())
                        except IndexError:
                            return data_dict, product_name_group
                
                        if matched:
                            product_name_group.remove(product_name_group[v])
                            v = 0
                            found = True
                            
                            xx = matched.group(0).strip()
                            data_dict[data_dict_key].append(xx)
                            ff = re.search(r"(?:\d+\s?)", xx)
                            if ff:
                                data_dict["storage_details"].update({
                                    "mem_type": x,
                                    "mem_grid": u,
                                    "value": ff.group(0)
                                })
                            break
                    if found:
                        break
                else:
                    v += 1
        return data_dict, product_name_group

    #=================================================================
    # CLASSIFIER FUNCTION -- MEMORY
    #=================================================================
    def memory_regex_mapper(self, data_dict={}, product_name_group=[], data_dict_key="", pattern=None):
        if not bool(data_dict[data_dict_key]):
            v = 0
            while v < len(product_name_group):
                found = False
                for u,t in pattern.items():
                    for x,y in t.items():
                        try:
                            matched = re.search(y, product_name_group[v].strip())
                        except IndexError:
                            return data_dict, product_name_group
                        
                        if matched:
                            product_name_group.remove(product_name_group[v])
                            v = 0
                            found = True
                            
                            data_dict[data_dict_key].append(matched.group(0).strip())
                            
                            xx = matched.group(0).strip()
                            ff = re.search(r"(?:\d+\s?)", xx)
                            if ff:
                                data_dict["memory_details"].update({
                                    "mem_type": u,
                                    "mem_grid": x,
                                    "value": ff.group(0)
                                })
                            break
                    
                    if found:
                        break
                else:
                    v += 1
        return data_dict, product_name_group
    
    #=================================================================
    # CLASSIFIER FUNCTION -- PROCESSOR
    #=================================================================
    def processor_regex_mapper(self, data_dict={}, product_name_group=[], data_dict_key=""):
        
        if bool(data_dict["processor"]) and data_dict_key=="processor":
            return data_dict, product_name_group
        
        v = 0
        while v < len(product_name_group):
            
            found = False
            
            for a,b in regexFile.PROCESSOR_REGEX.items():
                for c,d in b.items():
                    if isinstance(d, dict):
                        for key,val in d.items():
                            
                            try:
                                matched = re.search(val, product_name_group[v].strip())
                            except IndexError:
                                return data_dict, product_name_group
                            
                            if matched:
                                span_found = matched.span()
                                product_name_group[v] = product_name_group[v].replace(product_name_group[v][span_found[0]:span_found[1]], "")
                                
                                data_dict[data_dict_key].append(matched.group(0).strip())
                                data_dict["processor_details"].update(self.get_processor_details(matched.group(0), cpu_type=a, sub_type=c, family=key))
                                
                                v = 0
                                found = True
                                break
                        if found:
                            break
                    else:
                        matched = re.search(d, product_name_group[v].strip())
                        
                        if matched:
                            span_found = matched.span()
                            product_name_group[v] = product_name_group[v].replace(product_name_group[v][span_found[0]:span_found[1]], "")
                            
                            data_dict[data_dict_key].append(matched.group(0).strip())
                            data_dict["processor_details"].update(self.get_processor_details(matched.group(0), cpu_type=a, sub_type=c))
                            
                            v = 0
                            found = True
                            break
                if found:
                    break
            else:
                v +=1
                             
        return data_dict, product_name_group
    
    #=================================================================
    # GET PROCESSOR DETAILS
    #=================================================================
    
    def get_processor_details(self, matched_data=None, cpu_type=None,sub_type=None,family=None):
        
        data = {
            "cpu_type": cpu_type,
            "sub_type": sub_type,
            "family": family,
            "gen": None,
            "u_type": None,
            "nuc": None,
            "n": None,
            "h_type": None,
        }
        
        for key,val in regexFile.FILTER_PROCESSOR_REGEX.items():
            
            matched = re.search(val, matched_data)

            if matched:
                re_search = re.search("\d+", matched.group(0))
                if re_search:
                    data[key] = re_search.group(0)
        return data
    
    #=================================================================
    # CLASSIFIER FUNCTION -- GRAPHICS
    #=================================================================
    
    def graphics_regex_mapper(self, data_dict={}, product_name_group=[], data_dict_key=""):
        
        if bool(data_dict["graphics"]) and data_dict_key=="graphics":
            return data_dict, product_name_group
        
        v = 0
        while v < len(product_name_group):
            
            data = {
                "graphics_mem_type": None,
                "graphics_mem_grid": None,
                "graphics_value": None,
                "graphics_ddr_type": None,
                "graphics_provider": None,
                "graphics_provider_family": None,
                "graphics_provider_version": None,
                "graphics_integrated": None,
            }
            
            found = False
            for a,b in regexFile.GRAPHICS_REGEX.items():
                for c,d in b.items():
                    
                    if isinstance(d, dict):
                        for key,val in d.items():
                            matched = re.search(val, product_name_group[v].strip())
                        
                            if matched:
                                span_found = matched.span()
                                product_name_group[v] = product_name_group[v].replace(product_name_group[v][span_found[0]:span_found[1]], "")
                                
                                data_dict[data_dict_key].append(matched.group(0).strip())
                                
                                data = {
                                    "graphics_mem_type": key,
                                    "graphics_mem_grid": None,
                                    "graphics_value": None,
                                    "graphics_ddr_type": None,
                                    "graphics_provider": a,
                                    "graphics_provider_family": c,
                                    "graphics_provider_version": None,
                                    "graphics_integrated": None,
                                }
                                
                                data = self.get_graphics_details(matched_data=matched.group(0).strip(), data=data)
                                data_dict["graphic_counter"].append(data) 
        
                                v = 0
                                found = True
                                break
                        if found:
                            break
                    else:
                        matched = re.search(d, product_name_group[v].strip())
                        
                        if matched:
                            span_found = matched.span()
                            product_name_group[v] = product_name_group[v].replace(product_name_group[v][span_found[0]:span_found[1]], "")
                            
                            data_dict[data_dict_key].append(matched.group(0).strip())
                            
                            data = {
                                "graphics_mem_type": None,
                                "graphics_mem_grid": None,
                                "graphics_value": None,
                                "graphics_ddr_type": None,
                                "graphics_provider": a,
                                "graphics_provider_family": c,
                                "graphics_provider_version": None,
                                "graphics_integrated": None,
                            }
                                
                            data = self.get_graphics_details(matched_data=matched.group(0).strip(), data=data)
                            
                            data_dict["graphic_counter"].append(data) 
                            
                            v = 0
                            found = True
                            break
                if found:
                    break
            else:
                v +=1
                
        # data_dict["graphics_details"].update(self.get_graphics_details(data_dict["graphics"]))           
        return data_dict, product_name_group
            
    #=================================================================
    # GET GRAPHICS DETAILS
    #=================================================================
    
    def get_graphics_details(self, data={}, matched_data=None):
        
        mem_regex = {
            "tb": r"(?:^\d+\s?tb\s?$)|(?:\d+\s?tb\s?)",
            "gb": r"(?:^\d+\s?gb\s?$)|(?:\d+\s?gb\s?)",
            "mb": r"(?:^\d+\s?mb\s?$)|(?:\d+\s?mb\s?)"
        }
        
        for key,value in mem_regex.items():
            graphics_mem_grid = re.search(value,matched_data)
            if graphics_mem_grid:
                data["graphics_mem_grid"] = key

                graphics_value = re.search(r"\d+\s?",graphics_mem_grid.group(0).strip())
                if graphics_value:
                    data["graphics_value"] = graphics_value.group(0).strip()
        
        return data
    
    
    
    #=================================================================
    # CLASSIFIER FUNCTION -- YEAR
    #=================================================================
    def year_regex_mapper(self, data_dict={}, product_name_group=[], data_dict_key="", pattern=""):
        
        if bool(data_dict["year"]) and data_dict_key=="year":
            return data_dict, product_name_group
            
        v = 0
        while v < len(product_name_group):
            matched = re.search(r"(20\d{2}\s?)", product_name_group[v].strip())

            if matched:
                data_dict[data_dict_key].append(matched.group(0).strip())

                found = matched.span()
                product_name_group[v] = product_name_group[v].replace(product_name_group[v][found[0]:found[1]], "")

                v = 0
                break
            else:
                v +=1
                    
        return data_dict, product_name_group
            
    #=================================================================
    # MAIN CLASSIFIER FUNCTION
    #=================================================================    
    def classifier_func(self, product_name_group=[], data_dict={}):    
        
        if not bool(product_name_group):
            return data_dict


        # check ram
        #===================================================
        
        if not data_dict["memory"]:
            data_dict, product_name_group = self.memory_regex_mapper(data_dict=data_dict, 
                                                        product_name_group=product_name_group,
                                                        data_dict_key = "memory",
                                                        pattern=regexFile.MEMORY_REGEX)
        
        # check storage
        #===================================================
        
        data_dict, product_name_group = self.storage_regex_mapper(data_dict=data_dict, 
                                                    product_name_group=product_name_group, 
                                                    data_dict_key="storage", 
                                                    pattern=regexFile.STORAGE_REGEX)
        
        # check weight/capacity
        #===================================================    

        data_dict, product_name_group = self.dimension_regex_mapper(data_dict=data_dict, 
                                                    product_name_group=product_name_group, 
                                                    data_dict_key="weight", 
                                                    pattern=regexFile.WEIGHT_REGEX)
        # check size/dimensions
        #===================================================    

        data_dict, product_name_group = self.dimension_regex_mapper(data_dict=data_dict, 
                                                    product_name_group=product_name_group, 
                                                    data_dict_key="dimension", 
                                                    pattern=regexFile.DIMENSION_REGEX)
        
        # check processor
        #===================================================
        
        data_dict, product_name_group = self.processor_regex_mapper(data_dict=data_dict, 
                                                            product_name_group=product_name_group, 
                                                            data_dict_key="processor")
        
        # check operating system
        #===================================================    

        data_dict, product_name_group = self.regex_mapper(data_dict=data_dict, 
                                                    product_name_group=product_name_group, 
                                                    data_dict_key="os", 
                                                    pattern=regexFile.OS_REGEX)
        
        # check graphics
        #===================================================    

        data_dict, product_name_group = self.graphics_regex_mapper(data_dict=data_dict, 
                                                    product_name_group=product_name_group, 
                                                    data_dict_key="graphics")
        
        # check Color
        #===================================================

        v = 0
        while v < len(product_name_group):
            if (product_name_group[v].strip() in colors_list.COLORS or 
                product_name_group[v].replace("color", "").strip() in colors_list.COLORS):
                data_dict["color"].append(product_name_group[v].strip())
                product_name_group.remove(product_name_group[v])                          
                v = 0
            else:
                v +=1
                
        
        # check year
        #===================================================
        
        data_dict, product_name_group = self.year_regex_mapper(data_dict=data_dict, 
                                                            product_name_group=product_name_group, 
                                                            data_dict_key="year")
        
        
        return data_dict, product_name_group
    
    #=================================================================
    # function to join left out words
    #=================================================================
    def join_extra_words(self, xx=[]):
        product_name_last = ' '.join(xx).split(" ")
        product_name_last = [x.strip() for x in product_name_last if x.strip() !=""]
        
        o_dict = OrderedDict()

        for x in product_name_last:
            if x.strip() !="-":
                if x in o_dict.keys():
                    o_dict[x] = o_dict[x]+1
                else:
                    o_dict.update({x:1})

        product_final = ' '.join(o_dict)
        return product_final
    
    #=================================================================
    # KEYWORD SPLITTER FUNCTION
    #=================================================================
    def keyword_splitter(self, product_name=None, product_id=None, main_product=True, product_data={}, url=None):
        
        self.product_id = product_id
        self.product_data = product_data
        self.product_model_no = None
        self.product_part_number = None
        
        # Containers
        #=================================================================
        data_dict = {
            "storage":[],
            "storage_details": {},
            "storage_counter":[],
            "memory": [],
            "memory_details":{},
            "other": [],
            "graphics":[],
            "graphic_counter":[],
            "graphics_details":{},
            "processor": [],
            "processor_details": {},
            "color": [],
            "hertz": [],
            "dimension": {},
            "weight": {},
            "os":[],
            "year":[],
            "brand": None,
            "model": None,
            "part_no": None,
            "url": url
        }

        product_ss_group = []
        product_name_group = []
        xx1 = []
        xx2 = []
        
        # print(product_name)
        
        # Initialize product name, model and part_no
        # based on conditions if product_id, product_name and product_data
        #================================================================
        if self.main_product:
            if product_name is not None or bool(self.product_data) is not False:
                if product_name.strip() != "":
                    self.product_name = product_name 
                else:
                    if self.product_data["product_title"].strip() != "":
                        self.product_name = self.product_data["product_title"]

                if bool(self.product_data) is not False:
                    self.product_model_no = self.product_data["product_model_no"]
                    self.product_part_number = self.product_data["product_part_number"]
                    data_dict["model"] = self.product_data["product_model_no"]
                    data_dict["part_no"] = self.product_data["product_part_number"]
                    data_dict["brand"] = self.product_data["product_brand"]
            
        # if it is a main_product then only
        # do not use for bing search results
        # fetch data from database if product_name is not available
        # run complete process along with bing search
        #================================================================
        if main_product:
            self.db_connect = db_connect()
            
            if self.product_name.strip() =="":
                if self.product_id is not None and self.product_id.strip() !="":
                    if self.fetch_product_details():
                        self.product_list = self.keyword_splitter()
        
        # Main
        #=================================================================

        product_name = product_name.lower().replace("\n", "").replace("\r\n", "")
        
        product_name = product_name.encode("ascii", "ignore").decode()
        
        # Remove Stopwords
        #=================================================================
        
        all_stopwords = stopwords.words('english')
        all_stopwords += stop_words.STOP_WORDS
        
        text_tokens = word_tokenize(product_name)
        tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
        
        product_name = ' '.join(tokens_without_sw)
        
        # print("product name ",product_name)
        
        # Fetch Brand Name :: Only if not previously populated
        #=================================================================
        if data_dict["brand"] is None:
            
            tokenize = word_tokenize(product_name)
            trigrams=ngrams(tokenize,3)

            words_dt = [x for x in trigrams]
            
            i = 0
            jj = list(words_dt[0])
            
            while i<3:
                if jj[i] in self.brands_list.keys():
                    data_dict["brand"] = jj[i]
                    break
                else:
                    i +=1  
    
        # Product Name to Numpy Array -- Fetch strings groups
        #=================================================================
        while True:
            main_data = np.array(list(product_name))

            xx = np.where(main_data == "(")[0]

            if not bool(np.size(xx)):
                break
            else:
                sub_data = main_data[xx[-1]:]

                ss = np.where(np.array(sub_data) == ")")[0]

                if bool(np.size(ss)):
                    product_ss_group.append(''.join(main_data[xx[-1]:ss[0]+xx[-1]+1]))

                    main_data = np.delete(main_data, range(xx[-1],ss[0]+xx[-1]+1))
                else:
                    break
            product_name = ''.join(main_data)


        # Replace and split the grouped words
        #=================================================================
        for xx in product_ss_group:
            product_name_group += re.sub(REPLACERS, " | ", xx.replace("(", "").replace(")","")).split("|")

        product_name_group = list(set(product_name_group))

        product_name_list = product_name.replace(",", " | ").replace("+", " | ").split("|")   
            
        # Execute Classifier functions on the word groups
        #=================================================================
        if bool(product_name_group):
            data_dict, xx1 = self.classifier_func(product_name_group, data_dict)
        
        if bool(product_name_list):
            data_dict, xx2 = self.classifier_func(product_name_list, data_dict)
            
        keywords = self.join_extra_words(xx2)+" "+self.join_extra_words(xx1)
        product_name_list_extended = keywords.strip().split(" ")
        
        if bool(product_name_list_extended):
            data_dict, xx3 = self.classifier_func(product_name_list_extended, data_dict)
        
        # print(data_dict,xx1,xx2,xx3,"\n")
        
        keywords = self.join_extra_words(xx3)
        
        # print("keywords", keywords)
        
        # create name from keywords 
        # call only if main_product
        #=================================================================
        
        if data_dict["brand"] is not None:     
            self.compare_data.append(data_dict)
        else:
            return False, None
        
        keywords = self.generate_product_name(data_dict, keywords)
            
        # print(data_dict)
        
        if main_product:
            product_list = self.call_bing_api(keywords)

            self.length_search_list = len(product_list)
        
            if not bool(product_list):
                print("No search results found")
                return False, None
            else:
                return True, product_list
                    
    #=================================================================
    # Generate a proper product name for master product
    #=================================================================  
    def generate_product_name(self, data_dict={}, keywords=""):
        features =""
        for key, val in data_dict.items():
            
            if key not in ["dimension", "weight"]:
                
                if data_dict[key] is not None:
                    
                    try:
                        name = list(filter(None, data_dict[key]))
                        name = ' '.join(name)

                        if name != "":
                            features += f'{name}/' 
                    except:
                        pass
            
            else:
                if bool(data_dict[key]):
                    for idx,v in data_dict[key].items():
                        if v.strip()!="":
                            features += f'{v} {idx}/'
                            
        if features.strip() != "":
            keywords = f'{keywords} ({features.strip("/")})'  
            
        return features 
    
    #=================================================================
    # Filter search results
    #=================================================================
    def filter_search_results(self, search_results=[]):
        for result in search_results:
            self.keyword_splitter(product_name=result["snippet"], main_product=False, url=result["url"])
         
        if len(self.compare_data) >= 1:
            
            # graphics card setter start
            #================================================================
            data = {
                "graphics_mem_type": None,
                "graphics_mem_grid": None,
                "graphics_value": None,
                "graphics_ddr_type": None,
                "graphics_provider": None,
                "graphics_provider_family": None,
                "graphics_provider_version": None,
                "graphics_integrated": None,
            }
            
            for row in self.compare_data:
                if not bool(row["graphics_details"]):
                    row["graphics_details"].update(data)
                    
                for graphic_counter in row["graphic_counter"]:
                    
                    if row["graphics_details"]["graphics_mem_type"] is None:
                        row["graphics_details"]["graphics_mem_type"] = graphic_counter["graphics_mem_type"]
                    
                    if row["graphics_details"]["graphics_mem_grid"] is None:
                        row["graphics_details"]["graphics_mem_grid"] = graphic_counter["graphics_mem_grid"]
                    
                    if row["graphics_details"]["graphics_value"] is None:
                        row["graphics_details"]["graphics_value"] = graphic_counter["graphics_value"]
                    
                    if row["graphics_details"]["graphics_ddr_type"] is None:
                        row["graphics_details"]["graphics_ddr_type"] = graphic_counter["graphics_ddr_type"]
                    
                    if row["graphics_details"]["graphics_provider"] == "generic" or row["graphics_details"]["graphics_provider"] is None:
                        row["graphics_details"]["graphics_provider"] = graphic_counter["graphics_provider"]
                        row["graphics_details"]["graphics_provider_family"] = graphic_counter["graphics_provider_family"]
                        
                    if row["graphics_details"]["graphics_provider_version"] is None:
                        row["graphics_details"]["graphics_provider_version"] = graphic_counter["graphics_provider_version"]
                    
                    if row["graphics_details"]["graphics_integrated"] is None:
                        row["graphics_details"]["graphics_integrated"] = graphic_counter["graphics_integrated"]
                
                del(row["graphic_counter"]) 
                
            # graphics card setter end
            #================================================================
            
            compare_processor = CompareProcessor(self.compare_data)
            compare_processor.compare_processor()
            
        else:
           return False 
        
        
#=================================================================
# Filter compareable products
#=================================================================

class CompareProcessor():

    def __init__(self, main_data={}):
        self.main_data = main_data
        self.result_data = {}
    
        
    
    def compare_processor(self):
        
        main_product = self.main_data[0]
        
        print(main_product)
        print(self.main_data)
    
        key_list = [] 
        
        for key, val in main_product.items(): 
            if isinstance(val, list):
                if bool(val):
                    key_list.append(key)
                    
            if isinstance(val, dict):
                if bool(val):
                    key_list.append(key)
                    
            if isinstance(val, str) and val is not None:
                if val.strip()!="":
                    key_list.append(key)
        
        compared_dataset = []
        
        for row in range(1,len(self.main_data)):
            data_dict = {
                "storage": True,
                "memory": True,
                "other": True,
                "graphics":True,
                "processor": True,
                "color": True,
                "hertz": True,
                "dimension": True,
                "weight": True,
                "os":True,
                "year":True,
                "brand": True,
                "model": True,
                "part_no": True,
                "url": self.main_data[row]["url"]
            }
            
            # Brand checks
            #================================================================
            if main_product["brand"] != self.main_data[row]["brand"]:
                print("Brand mismatch ", main_product["brand"], self.main_data[row]["brand"])
                continue
            
            
            # Storage checks
            #================================================================
            if "storage_details" in key_list:
                
                df_found = []
                
                try:  
                    if self.main_data[row]["storage_details"]["mem_type"] == main_product["storage_details"]["mem_type"]:
                        df_found.append(True)
                    else:
                        df_found.append(False)
                except:
                    pass
                
                try:     
                    if self.main_data[row]["storage_details"]["mem_grid"] == main_product["storage_details"]["mem_grid"]:
                        df_found.append(True)
                    else:
                        df_found.append(False)
                except:
                    pass
                
                try:      
                    if self.main_data[row]["storage_details"]["value"] == main_product["storage_details"]["value"]:
                        df_found.append(True)
                    else:
                        df_found.append(False)
                except:
                    pass
                    
                data_dict["storage"] = True if sum(df_found) == len(df_found) else False
                print("storage", df_found, sum(df_found), all(df_found), data_dict["storage"] ) 
            
            # Memory checks
            #================================================================
            if "memory_details" in key_list:
                df_found = []
                
                try:  
                    if self.main_data[row]["memory_details"]["mem_grid"] == main_product["memory_details"]["mem_grid"]:
                        df_found.append(True)
                    else:
                        df_found.append(False)
                except:
                    pass
                
                try:    
                    if self.main_data[row]["memory_details"]["value"] == main_product["memory_details"]["value"]:
                        df_found.append(True)
                    else:
                        df_found.append(False)
                except:
                    pass
                
                data_dict["memory"] = True if sum(df_found) == len(df_found) else False
                # print("memory", df_found, sum(df_found), all(df_found), data_dict["memory"]) 
                
            # Processor checks
            #================================================================    
            if "processor_details" in key_list:
                df_found = []
                
                try:
                    if self.main_data[row]["processor_details"]["cpu_type"] == main_product["processor_details"]["cpu_type"]:
                        df_found.append(True)
                    else:
                        df_found.append(False)
                except:
                    pass
                    
                try:
                    if self.main_data[row]["processor_details"]["sub_type"] == main_product["processor_details"]["sub_type"]:
                        df_found.append(True)
                    else:
                        df_found.append(False)
                except:
                    pass
                
                try:  
                    if self.main_data[row]["processor_details"]["family"] == main_product["processor_details"]["family"]:
                        df_found.append(True)
                    else:
                        df_found.append(False)
                except:
                    pass
                
                try:          
                    if self.main_data[row]["processor_details"]["gen"] == main_product["processor_details"]["gen"]:
                        df_found.append(True)
                    else:
                        df_found.append(False)
                except:
                    pass
                
                try:      
                    if self.main_data[row]["processor_details"]["u_type"] == main_product["processor_details"]["u_type"]:
                        df_found.append(True)
                    else:
                        df_found.append(False)
                except:
                    pass
                
                try:          
                    if self.main_data[row]["processor_details"]["nuc"] == main_product["processor_details"]["nuc"]:
                        df_found.append(True)
                    else:
                        df_found.append(False)
                except:
                    pass
                
                try:          
                    if self.main_data[row]["processor_details"]["n"] == main_product["processor_details"]["n"]:
                        df_found.append(True)
                    else:
                        df_found.append(False)
                except:
                    pass
                
                try:          
                    if self.main_data[row]["processor_details"]["h_type"] == main_product["processor_details"]["h_type"]:
                        df_found.append(True)
                    else:
                        df_found.append(False)
                except:
                    pass
                
                data_dict["processor"] = True if sum(df_found) == len(df_found) else False
                # print("processor", df_found, sum(df_found), all(df_found), data_dict["processor"])    
                    
                    
            # Graphics checks
            #================================================================  
            print("^"*20)
            
            if "graphics" in key_list:
                
                df_found = []
                
                    
            # Processor checks
            #================================================================    
            if "color" in key_list:
                df_found = []
            
            compared_dataset.append(data_dict)
            
        print(compared_dataset)
        
        
        return self.result_data

#
#
product_title = """OnePlus Nord CE 2 5G (Gray Mirror, 8GB RAM, 128GB Storage)"""

prod_search = BingSearchApi()
ret, product_list = prod_search.keyword_splitter(product_name=product_title, main_product=True)

if ret:
    # print(ret, product_list)
    
    prod_search.filter_search_results(product_list)
    
else:
    print("No search records")
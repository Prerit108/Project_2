import os
import sys
import json

from dotenv import load_dotenv   ##used to call environment variables (.env file)
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")   ## Environment variable name to be called
print(MONGO_DB_URL)

import certifi  ##certify is a Python package that provides a set of root certificates commonly used by Python libraries to create secure HTTP connections
ca = certifi.where()  ## It retrieve the path to the bundle of CA(certificate authorities) certificates. This is critical for establishing secure connections.

import pandas as pd
import numpy as np
import pymongo
from networksecurity.Logging import logger
from networksecurity.Exceptions.exception import NetworkSecurityException

## ETL pipeline
class NetworkDataExtract():
    def __init__(self):
        try:
            pass

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_converter(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop = True,inplace=True) ## Dropping the index of the dataset
            ## List of json arrays 
            records = list(json.loads(data.T.to_json()).values())  #T is transpose
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):  ## collection is essentially the equivalent of a table in a relational database
        try:
            self.database = database
            self.collection = collection
            self.records = records

            ## Mongo client to connect to mongodb
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            
            ## Assigning the database  on mongo client
            self.database = self.mongo_client[database]
            ## Assigning collection to the database
            self.collection = self.database[collection]
            
            self.collection.insert_many(self.records)
            return (len(self.records))
        
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
if __name__ == "__main__":
    FILE_PATH = "D:/Project_2/Network_Data/phisingData.csv"
    DATABASE = "MY_DATABASE"
    COLLECTION = "NetworkData"

    n1_obj = NetworkDataExtract()
    records = n1_obj.csv_to_json_converter(FILE_PATH)
    no_ofrecords = n1_obj.insert_data_mongodb(records,DATABASE,COLLECTION)
    print(no_ofrecords)
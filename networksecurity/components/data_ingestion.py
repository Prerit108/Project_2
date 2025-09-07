import os
import sys

import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from networksecurity.Exceptions.exception import NetworkSecurityException
from networksecurity.Logging.logger import logging
from networksecurity.entity.artifact_entity import Data_IngestionArtifact

## Configuration of data ingestion
from networksecurity.entity.config_entity import DataingestionConfig

## Reading from the Mongodb database

from dotenv import load_dotenv  ## Used to read ".env" file
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config = DataingestionConfig()):
        try : 
            self.data_ingestion_config = data_ingestion_config

        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    ## Function to read from mongodb
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]  

            df = pd.DataFrame(list(collection.find()))
            ## When we read data from mongodb 1 column _id is added
            if "_id" in df.columns.to_list():
                df = df.drop(columns="_id",axis = 1)
            
            df.replace({"na":np.nan},inplace = True)
            
            return df
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
    
    ## Storing the data taken from mongodb into local system
    def export_data_to_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            ## Creating a folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index = False,header=True)
            return dataframe
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def split_data(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set = train_test_split(
                dataframe,test_size= self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split")

            logging.info("Exited split_data method of DataIngestion class")

            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            dir_path = os.path.dirname(self.data_ingestion_config.test_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_set.to_csv(self.data_ingestion_config.train_file_path,index = False, header = True)

            train_set.to_csv(self.data_ingestion_config.test_file_path,index = False, header = True)

            logging.info("Train and test Data Exported")

        except Exception as ex:
            raise NetworkSecurityException(ex,sys)


    def initiate_data_ingestion(self):
        try:
            #Read from mongodb
            dataframe = self.export_collection_as_dataframe()
            ## Storing data locally
            dataframe = self.export_data_to_feature_store(dataframe)
            self.split_data(dataframe)
            

            dataingestion_artifact = Data_IngestionArtifact(
                train_file_path = self.data_ingestion_config.train_file_path,
                test_file_path = self.data_ingestion_config.test_file_path
                )
            ## The output of the data ingestion is train and test file path
            return dataingestion_artifact

        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
    

import os
import sys


from networksecurity.entity.artifact_entity import Data_IngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.Exceptions.exception import NetworkSecurityException
from networksecurity.Logging.logger import logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

from scipy.stats import ks_2samp   ## Checking datadrift
import pandas as pd
import numpy as np 

class DataValidation:
    # Using this caused an error
    # Because train_file_path and test_file_path do not have default values, they become required arguments. using "=" make it optional, and leave it on python to run function and find default values.
    # But when Python tries to run Data_IngestionArtifact(), it sees that the __init__ method requires two arguments (train_file_path and test_file_path) that you didn't provide. So, it immediately raises a TypeError
    # def __init__(self,data_ingestion_artifacts = Data_IngestionArtifact(), 
    #              data_validation_config:DataValidationConfig):
        

    def __init__(self,data_ingestion_artifacts:Data_IngestionArtifact,  # I expect the data_ingestion_artifacts parameter to be an instance of the Data_IngestionArtifact class.
                 data_validation_config:DataValidationConfig):
        try : 
            ##Input for datavalidation
            self.data_ingestion_artifacts = data_ingestion_artifacts
            ## Output of the data validation
            self.data_validation_config = data_validation_config
            ## Reading the yaml file
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
            
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame)-> bool:
        try:
            number_of_columns = len(self.schema_config["columns"])
            logging.info(f"Required number of  columns:{number_of_columns}")
            logging.info(f"Data frame has  columns : {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False

        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def validate_numerical_columns(self,dataframe:pd.DataFrame)-> bool:
        try:
            no_of_numerical_columns = len(self.schema_config["numerical_columns"])
            logging.info(f"Required number of numerical columns:{no_of_numerical_columns}")
            logging.info(f"Data frame has numerical  columns : {len(dataframe.columns)}")
            if len(dataframe.columns) == no_of_numerical_columns:
                return True
            return False

        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    # basedf is the current data taken as reference
    def detect_dataset_drift(self,base_df,current_df,threshold = 0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                
                report.update({column :{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            ## Create a directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
            return status

        except Exception as ex:
            raise NetworkSecurityException(ex,sys)





    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifacts.train_file_path
            test_file_path = self.data_ingestion_artifacts.test_file_path

            ## read from train and test data
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            ## Validate number of columns
            status = self.validate_number_of_columns(dataframe = train_dataframe)
            if not status:
                error_message = f"Train dataframe does not contain all the columns \n"
            status = self.validate_number_of_columns(dataframe = test_dataframe)
            if not status:
                error_message = f"Test dataframe does not contain all the columns \n"

            ## Validate number of numerical columns
            status = self.validate_numerical_columns(dataframe = train_dataframe.select_dtypes(exclude = "O"))
            if not status:
                error_message = f"Train dataframe does not contain all the columns \n"
            status = self.validate_numerical_columns(dataframe = test_dataframe.select_dtypes(exclude = "O"))
            if not status:
                error_message = f"Test dataframe does not contain all the columns \n"

            ## Lets check Datadrift
            status = self.detect_dataset_drift(base_df = train_dataframe,current_df = test_dataframe)
            if status == True:
                dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
                os.makedirs(dir_path,exist_ok = True)

                dir_path = os.path.dirname(self.data_validation_config.valid_test_file_path)
                os.makedirs(dir_path,exist_ok = True)

                train_dataframe.to_csv(
                    self.data_validation_config.valid_train_file_path, index=False, header=True
                )
                test_dataframe.to_csv(
                    self.data_validation_config.valid_test_file_path, index=False, header=True
                )
            
                data_validation_artifact = DataValidationArtifact(
                    validation_status=status,
                    valid_train_file_path=self.data_ingestion_artifacts.train_file_path,
                    valid_test_file_path=self.data_ingestion_artifacts.test_file_path,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path,
                )
                return data_validation_artifact
            
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
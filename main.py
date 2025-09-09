import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.Exceptions.exception import NetworkSecurityException
from networksecurity.Logging.logger import logging
from networksecurity.entity.config_entity import DataingestionConfig,TrainingPipelineConfig,DataValidationConfig
from networksecurity.components.data_validation import DataValidation
# from networksecurity.entity.artifact_entity import Data_IngestionArtifact

 ## Checking if it is working
if __name__ == "__main__":
    try:
        traningpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataingestionConfig(traningpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Started the data ingestion")
        dataingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Completed the data ingestion")
        print(dataingestion_artifact)

        data_validation_config = DataValidationConfig(traningpipelineconfig)
        logging.info("Data Validation started")
        data_validation = DataValidation(dataingestion_artifact,data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_artifact)



    except Exception as ex:
        raise NetworkSecurityException(ex,sys)
         
    

import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.Exceptions.exception import NetworkSecurityException
from networksecurity.Logging.logger import logging
from networksecurity.entity.config_entity import DataingestionConfig,TrainingPipelineConfig

 ## Checking if it is working
if __name__ == "__main__":
    try:
        traningpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataingestionConfig(traningpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Started the data ingestion")

        dataingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(dataingestion_artifact)

        
    except Exception as ex:
        err = NetworkSecurityException(ex,sys)
        logging.info(err)
        raise err 
    

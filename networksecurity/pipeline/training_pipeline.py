import os
import sys

from networksecurity.Exceptions.exception import NetworkSecurityException
from networksecurity.Logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import(
TrainingPipelineConfig,
DataingestionConfig,
DataValidationConfig,
DataTransformationConfig,
ModelTrainerConfig)

from networksecurity.entity.artifact_entity import(
    ModelTrainerArtifact,
    Data_IngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact
)

class TrainingPipeline():
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            data_ingestion_config = DataingestionConfig(self.training_pipeline_config)
            logging.info("Start Data Ingestion")
            data_ingestion = DataIngestion(data_ingestion_config = data_ingestion_config)
            dataingestion_artifact =  data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion Completed and artifacts :{dataingestion_artifact}")
            return dataingestion_artifact
        except Exception as ex:
                raise NetworkSecurityException(ex,sys)
        
    def start_data_validation(self,dataingestion_artifact:Data_IngestionArtifact):
        try:
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            logging.info("Start Data Validation")
            data_validation = DataValidation(data_ingestion_artifacts=dataingestion_artifact,data_validation_config=data_validation_config)
            datavalidation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation Completed and artifacts :{datavalidation_artifact}")
            return datavalidation_artifact
        
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def start_data_transformation(self,datavalidation_artifact:DataValidationArtifact):
            try:
                data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
                logging.info("Start Data Transformation")
                data_transformation = DataTransformation(data_validation_artifact=datavalidation_artifact,data_transformation_config=data_transformation_config)
                data_transformation_artifact = data_transformation.initiate_data_transformation()
                logging.info(f"Data Transformation Completed and artifacts :{data_transformation_artifact}")
                return data_transformation_artifact
            
            except Exception as ex:
                raise NetworkSecurityException(ex,sys)
    
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            logging.info("Model training started")
            model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            modeltrainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            modeltrainer_artifacts = modeltrainer.initiate_model_trainer()
            logging.info(f"Model trained and artifact created {modeltrainer_artifacts}")

        except Exception as ex:
                raise NetworkSecurityException(ex,sys)
    

    def run_pipeline(self):
        try:
            dataingestion_artifact = self.start_data_ingestion()
            datavalidation_artifact = self.start_data_validation(dataingestion_artifact=dataingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(datavalidation_artifact=datavalidation_artifact)
            modeltrainer_artifacts = self.start_model_trainer(data_transformation_artifact= data_transformation_artifact)

        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
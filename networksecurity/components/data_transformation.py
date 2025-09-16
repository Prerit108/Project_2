import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.Exceptions.exception import NetworkSecurityException
from networksecurity.Logging.logger import logging
from networksecurity.utils.main_utils.utils import save_object,save_numpy_array


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config

        except Exception as ex:
            raise NetworkSecurityException(ex,sys) # type: ignore
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as ex:
            raise NetworkSecurityException(ex,sys) # type: ignore
        
    def get_data_transformer_object(self)-> Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.
        
        Args:
        cls: DataTransformation
        
        Returns:
        A Pipeline object
        """
        logging.info("Enter get_data_transformer_object of Transformation")
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)   ## ** means the parameters passed are in the form of key value pair.
            logging.info(f"Initialise KNNIMPUTER with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")

            processor = Pipeline([("imputer",imputer)])

            return processor
        
        except Exception as ex:
            raise NetworkSecurityException(ex,sys) # type: ignore
        
        
    def initiate_data_transformation(self)-> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation of DataTransformation")
        try:
            logging.info("Starting Data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ## Training dataframe
            input_feature_train_df = train_df.drop(columns = [TARGET_COLUMN],axis =1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            
            ## Test dataframe
            input_feature_test_df = test_df.drop(columns = [TARGET_COLUMN],axis =1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor = self.get_data_transformer_object()

            ## Transforming the data
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transform_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            ## can also use fit_transform
            transform_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            ## Knn imputer returns a numpy array
            
            ## Used Numpy array for better compatibility and efficiency
            ## Combining input and target feature into a single numpy array
            train_arr = np.c_[transform_input_train_feature,np.array(target_feature_train_df)]   
            test_arr = np.c_[transform_input_test_feature,np.array(target_feature_test_df)] 

            
            #save numpy array data
            save_numpy_array(self.data_transformation_config.transformed_train_file_path, array=train_arr,)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object,)

            ## Saving the preprocessor file to a different location
            save_object("final_models/preprocessor.pkl",preprocessor_object)

            ## Preparing Artifacts

            data_transformatio_artifacts = DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path,                  
            )

            return data_transformatio_artifacts
            


        except Exception as ex:
            raise NetworkSecurityException(ex,sys) # type: ignore

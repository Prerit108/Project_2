## This file contains info to store processed pickle file and model file
from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

import os
import sys 

from networksecurity.Exceptions.exception import NetworkSecurityException
from networksecurity.Logging. logger import logging

# This class combines both preprocessor and the model
## This class can be used for prediction of new data

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
        
    def Predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_predict = self.model.predict(x_transform)
            return y_predict
        except Exception as ex:
            raise NetworkSecurityException(ex,sys)
    

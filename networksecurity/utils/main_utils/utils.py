import yaml
import dill
import pickle
import os,sys
import numpy as np

from networksecurity.Exceptions.exception import NetworkSecurityException
from networksecurity.Logging.logger import logging

def read_yaml_file(file_path:str) -> dict:
    ## Since Schema is in the form of dictionary, return it in dict
    try:
        with open(file_path,"r") as file:
            return yaml.safe_load(file)
    except Exception as ex:
        raise NetworkSecurityException(ex,sys)

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as ex:
        raise NetworkSecurityException(ex, sys)
    
def save_numpy_array(file_path:str,array:np.array):

    """Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save"""
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as ex:
        raise NetworkSecurityException(ex, sys) from ex
    
## To save the prerpocessor pickle file
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as ex:
        raise NetworkSecurityException(ex,sys) from ex
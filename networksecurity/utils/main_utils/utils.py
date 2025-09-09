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
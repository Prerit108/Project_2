# import yaml
# from networksecurity.Exceptions.exception import NetworkSecurityException
# import sys 

# def read_yaml_file(file_path:str) -> dict:
#     ## Since Schema is in the form of dictionary, return it in dict
#     try:
#         with open(file_path,"r") as file:
#             return yaml.safe_load(file)
#     except Exception as ex:
#         raise NetworkSecurityException(ex,sys)
# schema_config = read_yaml_file("schema.yaml")
# print(schema_config)
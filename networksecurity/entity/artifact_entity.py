from dataclasses import dataclass

@dataclass  ## creates variables for class and data given to them in parameter is stored
class Data_IngestionArtifact:
    ## This is the required ouput from the data_ingestion component
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    ## The info returned after data validation
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str
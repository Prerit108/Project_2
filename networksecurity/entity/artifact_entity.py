from dataclasses import dataclass

@dataclass  ## creates variables for class
class Data_IngestionArtifact:
    ## This is the required ouput from the data_ingestion component
    train_file_path:str
    test_file_path:str
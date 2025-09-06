import logging
import os
from datetime import datetime

logs_dir = os.path.join(os.getcwd(), "logs")           # Construct full path to the log file inside a 'logs' directory in the current working directory
os.makedirs(logs_dir, exist_ok=True)                             # Create the directory path if it doesn't exist. and append in that folder

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"  # Create a log filename with current timestamp (e.g., '08_25_2025_23_43_00.log')
LOG_FILE_PATH = os.path.join(logs_dir,LOG_FILE)  # Create full path to the log file by joining the logs directory path with the log filename

logging.basicConfig(
    filename = LOG_FILE_PATH,
    format= "%(asctime)s %(lineno)d %(name)s %(levelname)s %(message)s",
    level = logging.INFO 
)


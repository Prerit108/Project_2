import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print (mongo_db_url)

import pymongo
from networksecurity.Exceptions.exception import NetworkSecurityException
from networksecurity.Logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

client = pymongo.MongoClient(mongo_db_url,tlsCAFile = ca)


from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME,DATA_INGESTION_DATABASE_NAME
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# Fast api
app = FastAPI()
origins = ["*"]

## For accessing the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods= ["*"],
    allow_headers=["*"],
)

# Taking files from the templates folder
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory = "templates")


# Home page in fast api
## Hardcoded in fast api
## Through this all api in fast api can be seen
@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")

    except Exception as ex:
        raise NetworkSecurityException(ex,sys)

@app.post("/predict")
async def predict_route(request:Request,file:UploadFile = File(...)):  ## - Jinja2 templates often rely on request for things like URL generation, accessing session data, or rendering dynamic content based on request metadata.
    try:
        df=pd.read_csv(file.file)
        preprocesor=load_object(file_path = "final_models/preprocessor.pkl")
        final_model=load_object(file_path = "final_models/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.Predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        
        df.to_csv("predicted_output/predicted.csv")
        ## Converting to html
        table_html = df.to_html(classes='table')

        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as ex:
        raise NetworkSecurityException(ex,sys)
    

if __name__ == "main":
    app_run(app,host = "localhost",port = 8000) 
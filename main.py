import mlflow.sklearn
import mlflow
import pickle

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from typing import List

# set mlflow tracking uri
mlflow.set_tracking_uri("http://127.0.0.1:5000")

app = FastAPI()

# model is a simple linear regression model
class Item(BaseModel):
    data: List[List[float]]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict/")
async def make_prediction(item: Item):
    # read in the model
    # TODO: avoid always reading the model every time a request is made
    # try:
    model = mlflow.sklearn.load_model("toy_model")
    # except:
    #     model = pickle.load(open("toy_model.pkl", "rb"))

    try:
        data = np.array(item.data)
        prediction = model.predict(data)
        return {"prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# @app.post("/yesno/")
# async def yesno(query):
#     if query == "is mlflow working?":
#         return {"response": "yes"}
#     else:
#         return {"response": "no"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

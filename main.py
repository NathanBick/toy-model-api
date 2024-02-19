from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from typing import List

app = FastAPI()

# model is a simple linear regression model
class Item(BaseModel):
    data: List[List[float]]

@app.post("/predict/")
async def make_prediction(item: Item):
    try:
        data = np.array(item.data)
        prediction = model.predict(data)
        return {"prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

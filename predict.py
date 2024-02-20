import requests

# inference data with names
data = {
    "data": [[0.00632,18.00,2.310,0,0.5380,6.5750,65.20,4.0900,1,296.0,15.30,396.90,4.98]]
}

# make request to local fastapi server
response = requests.post("http://127.0.0.1:8000/predict/", json=data)

# print prediction
print(response)
print(response.text)

# make request to azure ml service deployed model endpoint
azure_response = requests.post("https://test-model-hnbss.eastus2.inference.ml.azure.com/score", json=data)

# print prediction
print(response)
print(response.text)
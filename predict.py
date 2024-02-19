import requests

# inference data
data = {
    "data": [[0.00632,18.00,2.310,0,0.5380,6.5750,65.20,4.0900,1,296.0,15.30,396.90,4.98]]
}

# make request
response = requests.post("http://127.0.0.1:8000/predict/", json=data)

# print prediction
print(response)
print(response.text)
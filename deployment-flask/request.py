import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={'roughness':21, 'tension_strenght':14, 'elongation':1.5})

print(r.json())

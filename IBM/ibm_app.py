import numpy as np
from flask import Flask, request, jsonify, render_template
#import pickle

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "MOzoGy2S3E-nzOWNdT15oyn-okHyY0D-Jaa8Za95pRW7"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
#model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = prediction[0]
    if(output==0):
        bar='Material is abs'
    else:
        bar='Material is pla'
    
    return render_template('index.html', prediction_text=bar)

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    #prediction = model.predict([np.array(list(data.values()))])

    #output = prediction[0]
    payload_scoring = {"input_data": [{"fields": [["f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10"]], "values": [[0.02,8,90,0,220,60,40,0,25,18,1.2]]}]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/e4d735c1-abcd-4b7d-8854-83e92635b009/predictions?version=2022-06-03', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    #print("Scoring response")
    #print(response_scoring.json())
    pred=response_scoring.json()
    output=pred['predictions'][0]['values'][0][0]
    if(output==0):
        bar='Material is abs'
    else:
        bar='Material is pla'
   
    return jsonify(bar)


if __name__ == "__main__":
    app.run(debug=True)

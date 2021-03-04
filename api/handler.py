import joblib
import pandas as pd
from crosssell.CrossSell import CrossSell
from flask import Flask, request, Response

## Loading Model
model = joblib.load('../models/linear_regression_cycle1.joblib')

## initialize API
app = Flask(__name__)

@app.route('/crosssell/predict', methods=['POST'])
def crosssell_predict():
    test_json = request.get_json()
    
    if test_json: # there is data
        if isinstance(test_json, dict): # unique example
            test_raw = pd.DataFrame(test_json, index=[0])
            
        else: # multiple example
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())
            
        # Instantiate Rossmann class
        pipeline = CrossSell()
        
        # data preparation
        df1 = pipeline.data_preparation(test_raw)

        # prediction
        df_response = pipeline.get_prediction(model, test_raw, df1)
        
        return df_response

    else:
        return Reponse('{}', status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run('0.0.0.0') 
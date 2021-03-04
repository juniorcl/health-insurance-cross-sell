import joblib
import inflection
import numpy  as np
import pandas as pd
from scipy import stats

class CrossSell:
    
    def __init__(self):
        self.ohe = joblib.load('../functions/one_hot_encoder_cycle1.joblib')
        self.te = joblib.load('../functions/target_encoder_cycle1.joblib')
        self.ss = joblib.load('../functions/standard_scaler_cycle1.joblib')
        self.mm = joblib.load('../functions/minmax_scaler_cycle1.joblib')
        
    def data_preparation(self, df1):

        cols_old = df1.columns.tolist()

        snakecase = lambda x: inflection.underscore(x)
        cols_new = list(map(snakecase, cols_old))

        df1.columns = cols_new

        ## OneHotEncoding
        df1 = df1[['previously_insured', 'vehicle_damage', 'policy_sales_channel', 'age']]
        df1 = self.ohe.transform(df1)
        
        ## Target Encoding
        columns_te = ['policy_sales_channel']
        df1['policy_sales_channel_te'] = self.te.transform(df1[columns_te])
        
        ## BoxCox Transformation
        df1['age_bx'] = stats.boxcox(df1['age'])[0]
        
        ## Standard Scaler
        df1['age_bx_ss'] = self.ss.transform(df1[['age_bx']])
        
        ## MinMax Scaler
        df1['age_mm'] = self.mm.transform(df1[['age']])
        
        cs = ['previously_insured_yes', 'previously_insured_no', 'vehicle_damage_no',
              'vehicle_damage_yes', 'policy_sales_channel_te', 'age_bx_ss', 'age_mm']
        
        return df1[cs]
    
    def get_prediction(self, model, original_data, test_data):
        pred = model.predict(test_data)
        prob = model.predict_proba(test_data)[:, 1]
        
        original_data['prediction'] = pred
        original_data['score'] = prob
        
        original_data.sort_values('score', ascending=False, inplace=True)

        return original_data.to_json(orient="records", date_format="iso")
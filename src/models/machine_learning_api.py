# Now this is the code we used from all the previous steps we performed.


from flask import Flask, request
import pandas as pd
import numpy as np
import json
import pickle
import os

app = Flask(__name__)

#load the model and scaler files
model_path = os.path.join(os.path.pardir, os.path.pardir,'models')
model_filepath = os.path.join(model_path, 'lr_model.pkl')
scaler_filepath = os.path.join(model_path, 'lr_scaler.pkl')

#load them in
scaler = pickle.load(open(scaler_filepath,'rb')) #remember to set read more binary
model  = pickle.load(open(model_filepath,'rb'))

# columns put in order that the ML model will expect
columns = [ u'Age', u'Fare', u'FamilySize', \
       u'IsMother', u'IsMale', u'Deck_A', u'Deck_B', u'Deck_C', u'Deck_D', \
       u'Deck_E', u'Deck_F', u'Deck_G', u'Deck_Z', u'Pclass_1', u'Pclass_2', \
       u'Pclass_3', u'Title_Lady', u'Title_Master', u'Title_Miss', u'Title_Mr', \
       u'Title_Mrs', u'Title_Officer', u'Title_Sir', u'Fare_Bin_very_low', \
       u'Fare_Bin_low', u'Fare_Bin_high', u'Fare_Bin_very_high', u'Embarked_C', \
       u'Embarked_Q', u'Embarked_S', u'AgeState_Adult', u'AgeState_Child'] 

@app.route('/api', methods=['POST'])
def make_predicitions():
    #This will be executed with the API is called
    #Read the json object and convert it to a json string
    data = json.dumps(request.get_json(force='TRUE'))
    #create a data frame from the json string
    df = pd.read_json(data)
    #extract the index passenger id
    passenger_ids = df['PassengerId'].ravel()
    # capture the actual survived values -- we do not have all the actuals, those are on Kaggle, but this is how
    # this API process would work, if we did have a store of all the actual survival data
    actuals = df['Survived'].ravel()
    # extract all the columns from the data and convert into a matrix
    X = df[columns].as_matrix().astype('float')
    # transform the data into the scaled object
    X_scaled = scaler.transform(X)
    # make the predicitions
    predictions = model.predict(X_scaled)
    # create response object dataframe
    df_response = pd.DataFrame({'PassengerId': passenger_ids, 'Predicted': predictions, 'Actual': actuals})
    # return our JSON object
    return df_response.to_json()

if __name__ == '__main__':
    #host the flask app
    app.run(port=10001, debug=True,use_reloader=False) # debug = true for troubleshooting in dev
    
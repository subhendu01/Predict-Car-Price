from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('main.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    try:
        fuel_type_diesel=0
        if request.method == 'POST':
            year = int(request.form['Year'])
            present_price = float(request.form['Present_Price'])
            kms_driven = int(request.form['Kms_Driven'])
            owner = int(request.form['Owner'])
            fuel_type_petrol = request.form['Fuel_Type_Petrol']

            if fuel_type_petrol == 'Petrol':
                    fuel_type_petrol = 1
                    fuel_type_diesel = 0
            elif fuel_type_petrol == 'Diesel':
                fuel_type_petrol = 0
                fuel_type_diesel = 1
            else:
                fuel_type_petrol = 0
                fuel_type_diesel = 0

            year = 2020-year

            seller_type_individual = request.form['Seller_Type_Individual']
            if seller_type_individual == 'Individual':
                seller_type_individual = 1
            else:
                seller_type_individual = 0

            transmission_mannual = request.form['Transmission_Mannual']
            if transmission_mannual == 'Mannual':
                transmission_mannual = 1
            else:
                transmission_mannual = 0
            prediction = model.predict([[present_price, kms_driven, owner, year,
                                         fuel_type_diesel, fuel_type_petrol,
                                         seller_type_individual, transmission_mannual]])
            # print(prediction)
            output = round(prediction[0],2)
            if output < 0:
                return render_template('main.html',prediction_texts="Sorry you cannot sell this car")
            else:
                return render_template('main.html',prediction_text="Predicted Car selling price = {}".format(output))
        else:
            return render_template('main.html')
    except Exception as e:
        print(str(e))
        pass

if __name__=="__main__":
    app.run(debug=True)


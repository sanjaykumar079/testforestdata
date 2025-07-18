import pickle
from flask import Flask, render_template, request
import numpy as np

application = Flask(__name__)
app = application

# Load the trained Ridge model and scaler
ridge_model = pickle.load(open('models/ridge.pkl', 'rb'))
scaler_model = pickle.load(open('models/scaler.pkl', 'rb'))

@app.route("/")
def index():
    return render_template("index.html")  # Form page

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == "POST":
        try:
            # Extract form data
            Temperature = float(request.form.get('Temperature'))
            RH = float(request.form.get('RH'))
            Ws = float(request.form.get('Ws'))
            Rain = float(request.form.get('Rain'))
            FFMC = float(request.form.get('FFMC'))
            DMC = float(request.form.get('DMC'))
            ISI = float(request.form.get('ISI'))
            Classes = float(request.form.get('Classes'))
            Region = float(request.form.get('Region'))

            new_data = np.array([[Temperature, RH, Ws, Rain, FFMC, DMC, ISI, Classes, Region]])
            new_data_scaled = scaler_model.transform(new_data)
            result = ridge_model.predict(new_data_scaled)

            return render_template('home.html', result=result[0])
        except Exception as e:
            return f"Error: {e}"
    
    return render_template('home.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

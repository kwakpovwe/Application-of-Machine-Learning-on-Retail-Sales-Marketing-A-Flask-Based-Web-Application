from flask import Flask, render_template, request
import joblib
import numpy as np
from datetime import datetime

app = Flask(__name__)

# Load the model
best_gb_model = joblib.load('best_gb_model.pkl')

# Define a route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route to render the predict form
@app.route('/predict', methods=['GET'])
def predict_form():
    return render_template('predict.html')

# Endpoint for prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the current year dynamically
        current_year = datetime.now().year

        # Get the necessary features from the form
        features = [
            float(request.form['item_visibility']),  # 'Item_Visibility'
            float(request.form['item_visibility_meanratio']),  # 'Item_Visibility_MeanRatio'
            float(request.form['item_weight']),  # 'Item_Weight'
            float(request.form['item_mrp']),  # 'Item_MRP'
            current_year - int(request.form['outlet_establishment_year']),  # 'Outlet_Age'
            int(request.form['outlet_establishment_year']),  # 'Outlet_Establishment_Year'
            int(request.form['outlet_type_grocery_store']),  # 'Outlet_Type_Grocery_Store'
        ]
        
        # Convert features to a numpy array
        features_array = np.array(features).reshape(1, -1)
        
        # Predict using the best gb model
        prediction = best_gb_model.predict(features_array)[0]
        
        # Render the result template with the prediction
        return render_template('result.html', prediction=prediction)
    except ValueError as e:
        # Return an error message
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
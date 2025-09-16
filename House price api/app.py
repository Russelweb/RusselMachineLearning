# import numpy as np
# import joblib
# from flask import Flask, request, render_template

# # Load the trained model
# filename = 'Linear regression with loaded dataset(excel)'
# loaded_model = joblib.load(filename)

# # Initialize Flask app
# app = Flask(__name__)

# def linear_reg(input):
#     input = input.reshape(-1, 1)
#     prediction = loaded_model.predict(input)
#     return prediction[0]

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     prediction = None
#     if request.method == 'POST':
#         try:
#             # Get house size from the form
#             house_size = float(request.form['house_size'])
#             new_data = np.array(house_size)
#             prediction = linear_reg(new_data)
#         except ValueError:
#             prediction = "Invalid input. Please enter a valid number."

#     return render_template('index.html', prediction=prediction)

# if __name__ == '__main__':
#     app.run(debug=True)

# redo with full api functionalities


import numpy as np
import joblib
from flask import Flask, request, jsonify

# Load the trained model
filename = 'Linear regression with loaded dataset(excel)'
loaded_model = joblib.load(filename)

# Initialize Flask app
app = Flask(__name__)

def linear_reg(input):
    input = input.reshape(-1, 1)  # Reshape for model input
    prediction = loaded_model.predict(input)
    return prediction[0]

@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Get house size from the URL parameters
        house_size = float(request.args.get('house_size'))  # Use request.args
        new_data = np.array([house_size])  # Create a 1D array
        prediction = linear_reg(new_data)
        return jsonify({'prediction': prediction})  # Return JSON response
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input. Please enter a valid number.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
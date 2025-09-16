
# #RENDERING THE STLED HTML FILE

# from flask import Flask, request, render_template
# import pandas as pd
# import joblib
# from datetime import datetime
# import os

# # Load trained model
# model = joblib.load("cancer_model.pkl")

# app = Flask(__name__)

# # Excel file to store results
# RESULTS_FILE = "predictions.xlsx"

# # Ensure Excel file exists with headers
# if not os.path.exists(RESULTS_FILE):
#     df_init = pd.DataFrame(columns=[
#         "Timestamp", "Age", "Gender", "BMI", "Smoking", 
#         "GeneticRisk", "PhysicalActivity", "AlcoholIntake", 
#         "CancerHistory", "Prediction", "Confidence"
#     ])
#     df_init.to_excel(RESULTS_FILE, index=False)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     result = None
#     if request.method == "POST":
#         # Collect form data
#         data = {
#             "Age": int(request.form["age"]),
#             "Gender": int(request.form["gender"]),
#             "BMI": float(request.form["bmi"]),
#             "Smoking": int(request.form["smoking"]),
#             "GeneticRisk": int(request.form["geneticrisk"]),
#             "PhysicalActivity": float(request.form["physicalactivity"]),
#             "AlcoholIntake": float(request.form["alcoholintake"]),
#             "CancerHistory": int(request.form["cancerhistory"])
#         }

#         # Convert to DataFrame
#         df_input = pd.DataFrame([data])

#         # Predictions
#         pred = model.predict(df_input)[0]
#         prob = model.predict_proba(df_input)[:, 1][0]

#         risk = "⚠️ Possible Cancer Detected" if pred == 1 else "✅ No Cancer Detected"
#         confidence = round(prob * 100, 2)

#         result = {"risk": risk, "confidence": confidence}

#         # Append to Excel
#         df_new = pd.DataFrame([{
#             "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             **data,
#             "Prediction": risk,
#             "Confidence": f"{confidence}%"
#         }])

#         df_existing = pd.read_excel(RESULTS_FILE)
#         df_all = pd.concat([df_existing, df_new], ignore_index=True)
#         df_all.to_excel(RESULTS_FILE, index=False)

#     return render_template("index.html", result=result)

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000, debug=True)



# REDO with full api functionalities

from flask import Flask, request, jsonify
import pandas as pd
import joblib
from datetime import datetime
import os

# Load trained model
model = joblib.load("cancer_model.pkl")

app = Flask(__name__)

# Excel file to store results
RESULTS_FILE = "predictions.xlsx"

# Ensure Excel file exists with headers
if not os.path.exists(RESULTS_FILE):
    df_init = pd.DataFrame(columns=[
        "Timestamp", "Age", "Gender", "BMI", "Smoking", 
        "GeneticRisk", "PhysicalActivity", "AlcoholIntake", 
        "CancerHistory", "Prediction", "probability"
    ])
    df_init.to_excel(RESULTS_FILE, index=False)

@app.route("/predict", methods=["GET"])
def predict():
    try:
        # Collect parameters from query string
        age = int(request.args.get("age"))
        gender = int(request.args.get("gender"))
        bmi = float(request.args.get("bmi"))
        smoking = int(request.args.get("smoking"))
        geneticrisk = int(request.args.get("geneticrisk"))
        physicalactivity = float(request.args.get("physicalactivity"))
        alcoholintake = float(request.args.get("alcoholintake"))
        cancerhistory = int(request.args.get("cancerhistory"))

        # Prepare input data
        input_data = {
            "Age": age,
            "Gender": gender,
            "BMI": bmi,
            "Smoking": smoking,
            "GeneticRisk": geneticrisk,
            "PhysicalActivity": physicalactivity,
            "AlcoholIntake": alcoholintake,
            "CancerHistory": cancerhistory
        }
       

        # Convert to DataFrame
        df_input = pd.DataFrame([input_data])

        # Predictions
        pred = model.predict(df_input)[0]
        prob = model.predict_proba(df_input)[:, 1][0]

        risk = "⚠️ Possible Cancer Detected" if pred == 1 else "✅ No Cancer Detected"
        prob = round(prob * 100, 2)
        probability = f'{prob}%'

        # Prepare the result
        result = {
            "risk": risk,
            "probability": probability
        }

        # Append to Excel
        df_new = pd.DataFrame([{
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **input_data,
            "Prediction": risk,
            "probability": f"{probability}%"
        }])

        df_existing = pd.read_excel(RESULTS_FILE)
        df_all = pd.concat([df_existing, df_new], ignore_index=True)
        df_all.to_excel(RESULTS_FILE, index=False)

        return jsonify(result)

    except Exception as e:
       return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
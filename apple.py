import pandas as pd
import joblib
import streamlit as st

# Function to load models
def load_models():
    models = []
    for i in range(1, 11):
        model_path = f"model_{i}.pkl"
        model = joblib.load(model_path)
        models.append(model)
    return models

# Function for ensemble prediction
def predict_ensemble(models, input_data, features):
    user_data = pd.DataFrame([input_data], columns=features)  # Convert user input to DataFrame
    predictions = []

    for model in models:
        model_predictions = model.predict(user_data[features])  # Use specified features
        predictions.append(model_predictions)

    # Sum individual predictions for each model
    summed_predictions = sum(predictions)[0]  # Convert the sum to a scalar value
    print(summed_predictions)

    # Output based on cutoffs
    if summed_predictions <= 4:
        return "Low Risk / No Diabetes"
    elif 5 <= summed_predictions <= 7:
        return "Moderate Risk / Prediabetes"
    else:
        return "High Risk / Diabetes"

# Load models
models = load_models()

# Features
features = [
    'HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke', 'HeartDiseaseorAttack',
    'PhysActivity', 'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost',
    'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education', 'Income'
]

# Streamlit app
def main():
    st.title("Diabetes Prediction App")
    st.write("Fill in the values for each feature to predict diabetes.")

    # Get user input for each feature
    user_input = {}
    for feature in features:
        user_input[feature] = st.text_input(f"{feature}:", value="", key=feature)

    # Add a button to trigger the prediction
    if st.button("Predict"):
        # Check if any required field is not filled
        if "" in user_input.values():
            st.warning("Please fill in all required fields.")
        else:
            # Convert input values to float
            user_input = {key: float(value) for key, value in user_input.items()}

            # Make prediction
            prediction_result = predict_ensemble(models, user_input, features)

            # Display prediction result
            st.subheader("Diabetes Prediction Result:")
            st.write(prediction_result)
            

# Run the Streamlit app
if __name__ == "__main__":
    main()

import pandas as pd
import streamlit as st
import joblib

# Function to load models
def load_models():
    models = []
    for i in range(1, 11):
        model_path = f"model_{i}.pkl"
        model = joblib.load(model_path)
        models.append(model)
    return models

# Function for ensemble prediction
def predict_ensemble(models, input_data, features, threshold=0.5):
    user_data = pd.DataFrame([input_data], columns=features)  # Convert user input to DataFrame
    predictions = []

    for model in models:
        model_predictions = model.predict(user_data)  # Use the specified features
        predictions.append(model_predictions)

    # Assuming equal weights for all models
    #weights = [1 / len(models)] * len(models)
    weights = [1.6149, 1.3567, 1.6115, 1.6376, 1.5458, 1.5083, 1.6601, 1.6440, 1.6485, 1.5897]

    # Calculate the weighted sum
    weighted_sum = sum(weight * prediction for weight, prediction in zip(weights, predictions))

    # Make a decision based on the weighted sum (e.g., using a threshold)
    ensemble_prediction = (weighted_sum > threshold).astype(int)

    return ensemble_prediction[0]

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
            ensemble_prediction = predict_ensemble(models, user_input, features)

            # Display prediction
            st.subheader("Diabetes Prediction Result:")
            if ensemble_prediction == 1:
                st.error("Based on the provided information, it is predicted that you HAVE DIABETES.")
                st.error("This prediction is 95.1 percent accurate")
            else:
                st.success("Based on the provided information, it is predicted that you do NOT HAVE DIABETES.")
                st.success("This prediction is 95.1 percent accurate")

# Run the Streamlit app
if __name__ == "__main__":
    main()

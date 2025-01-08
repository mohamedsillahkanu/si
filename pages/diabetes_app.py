import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import requests

# Function to preprocess user input and make predictions
def predict_diabetes(user_input, model):
    # Preprocess user input
    data = {
        'HighBP': [user_input['HighBP']],
        'HighChol': [user_input['HighChol']],
        'CholCheck': [user_input['CholCheck']],
        'BMI': [float(user_input['BMI'])],
        'Smoker': [user_input['Smoker']],
        'Stroke': [user_input['Stroke']],
        'HeartDiseaseorAttack': [user_input['HeartDiseaseorAttack']],
        'PhysActivity': [user_input['PhysActivity']],
        'Fruits': [user_input['Fruits']],
        'Veggies': [user_input['Veggies']],
        'HvyAlcoholConsump': [user_input['HvyAlcohol']],
        'AnyHealthcare': [user_input['AnyHealthCare']],
        'NoDocbcCost': [user_input['NoDcbcCost']],
        'GenHlth': [user_input['GenHlth']],
        'MentHlth': [float(user_input['MentHlth'])],
        'PhysHlth': [float(user_input['PhysHlth'])],
        'DiffWalk': [user_input['DiffWalk']],
        'Sex': [user_input['Sex']],
        'Age': [user_input['Age']],
        'Education': [user_input['Education']],
        'Income': [user_input['Income']]
    }

    df = pd.DataFrame(data)

    # Standardize the features
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    # Make a prediction for the user input
    prediction = model.predict(df_scaled)

    return prediction[0]

# Streamlit app
st.title("Diabetes Prediction App")

# GitHub raw file URL
github_raw_url = 'https://raw.githubusercontent.com/mohamedsillahkanu/si/main/model_1.pkl'

# Load pre-trained model
response = requests.get(github_raw_url)
if response.status_code == 200:
    with open("model_1.pkl", "wb") as f:
        f.write(response.content)
    model = joblib.load("model_1.pkl")
else:
    st.error("Failed to download the model. Please try again later.")

# Mappings for dropdowns
yes_no_map = {"Yes": 1, "No": 0}

# Collect user input
user_input = {
    'HighBP': yes_no_map[st.selectbox("Do you have high blood pressure?", ["Yes", "No"], key='HighBP')],
    'HighChol': yes_no_map[st.selectbox("Have you been diagnosed with high cholesterol?", ["Yes", "No"], key='HighChol')],
    'CholCheck': yes_no_map[st.selectbox("Do you usually check your cholesterol?", ["Yes", "No"], key='CholCheck')],
    'BMI': st.text_input("Enter your BMI:", "", key='BMI'),
    'Smoker': yes_no_map[st.selectbox("Have you smoked at least 100 cigarettes (5 packs) in your entire life?", ["Yes", "No"], key='Smoker')],
    'Stroke': yes_no_map[st.selectbox("Ever been told you have had a stroke?", ["Yes", "No"], key='Stroke')],
    'HeartDiseaseorAttack': yes_no_map[st.selectbox("Have you been diagnosed with heart disease or suffered a heart attack?", ["Yes", "No"], key='HeartDiseaseorAttack')],
    'PhysActivity': yes_no_map[st.selectbox("Physical activity in the past 30 days (excluding job)?", ["Yes", "No"], key='PhysActivity')],
    'Fruits': yes_no_map[st.selectbox("Do you consume fruit more than once per day?", ["Yes", "No"], key='Fruits')],
    'Veggies': yes_no_map[st.selectbox("Do you eat vegetables more than once per day?", ["Yes", "No"], key='Veggies')],
    'HvyAlcohol': yes_no_map[st.selectbox("Do you consume more than 7 drinks of alcohol per week?", ["Yes", "No"], key='HvyAlcohol')],
    'AnyHealthCare': yes_no_map[st.selectbox("Do you have any kind of health care coverage?", ["Yes", "No"], key='AnyHealthCare')],
    'NoDcbcCost': yes_no_map[st.selectbox("Have you avoided visiting a doctor because of cost?", ["Yes", "No"], key='NoDcbcCost')],
    'GenHlth': st.selectbox("Would you say in general your health is:", [1, 2, 3, 4, 5], key='GenHlth'),
    'MentHlth': st.selectbox("Days of poor mental health (0-30):", list(range(0, 31)), key='MentHlth'),
    'PhysHlth': st.selectbox("Days of poor physical health (0-30):", list(range(0, 31)), key='PhysHlth'),
    'DiffWalk': yes_no_map[st.selectbox("Do you experience difficulty walking or moving?", ["Yes", "No"], key='DiffWalk')],
    'Sex': st.selectbox("Select your gender:", ["Female", "Male"], key='Sex', format_func=lambda x: "Female" if x == "Female" else "Male"),
    'Age': st.selectbox("Select your age group:", list(range(1, 14)), key='Age'),
    'Education': st.selectbox("Select your highest education level:", list(range(1, 7)), key='Education'),
    'Income': st.selectbox("Select your approximate annual household income:", list(range(1, 9)), key='Income')
}

# Add a submit button and validate required fields
if st.button('Submit'):
    if "" in user_input.values() or not user_input['BMI']:
        st.warning("Please fill in all required fields.")
    else:
        # Predict diabetes
        prediction = predict_diabetes(user_input, model)

        # Display prediction
        st.subheader("Diabetes Prediction Result:")
        if prediction == 1:
            st.write("Based on the provided information, it is predicted that you have diabetes.")
        else:
            st.write("Based on the provided information, it is predicted that you do not have diabetes.")

# Add a clear button to reset selections
if st.button('Clear Selections'):
    st.experimental_rerun()

import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

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

# Load pre-trained model
url = '/workspaces/si/model_1.pkl'
model = joblib.load(url)

# Define a function to reset selections
def reset_selections():
    for key in user_input:
        user_input[key] = ""

# Collect user input
user_input = {
    'HighBP': st.selectbox("Do you have high blood pressure?", ["", 0, 1], key='HighBP'),
    'HighChol': st.selectbox("Have you been diagnosed with high cholesterol?", ["", 0, 1], key='HighChol'),
    'CholCheck': st.selectbox("How often do you get your cholesterol checked?", ["", 0, 1], key='CholCheck'),
    'BMI': st.selectbox("Select your BMI:", [""] + list(range(5, 151)), key='BMI'),  # Range from 5 to 150
    'Smoker': st.selectbox("Are you a smoker?", ["", 0, 1], key='Smoker'),
    'Stroke': st.selectbox("Have you ever had a stroke?", ["", 0, 1], key='Stroke'),
    'HeartDiseaseorAttack': st.selectbox("Have you been diagnosed with heart disease or suffered a heart attack?", ["", 0, 1], key='HeartDiseaseorAttack'),
    'PhysActivity': st.selectbox("How often do you engage in physical activity per week?", ["", 0, 1], key='PhysActivity'),
    'Fruits': st.selectbox("How many servings of fruits do you consume on a typical day?", ["", 0, 1], key='Fruits'),
    'Veggies': st.selectbox("How many servings of vegetables do you consume on a typical day?", ["", 0, 1], key='Veggies'),
    'HvyAlcohol': st.selectbox("How often do you consume heavy alcohol?", ["", 0, 1], key='HvyAlcohol'),
    'AnyHealthCare': st.selectbox("Have you accessed any form of healthcare in the past year?", ["", 0, 1], key='AnyHealthCare'),
    'NoDcbcCost': st.selectbox("Have you avoided visiting a doctor because of cost?", ["", 0, 1], key='NoDcbcCost'),
    'GenHlth': st.selectbox("General Health", ["", 1, 2, 3, 4, 5], key='GenHlth'),
    'MentHlth': st.selectbox("Rate your mental health:", [""] + list(range(0, 31)), key='MentHlth'),  # Range from 0 to 30
    'PhysHlth': st.selectbox("Rate your physical health:", [""] + list(range(0, 31)), key='PhysHlth'),  # Range from 0 to 30
    'DiffWalk': st.selectbox("Do you experience difficulty walking or moving?", ["", 0, 1], key='DiffWalk'),
    'Sex': st.selectbox("Select your gender:", ["", 0, 1], key='Sex'),
    'Age': st.selectbox("Select your age:", ["", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], key='Age'),
    'Education': st.selectbox("Select your highest education level:", ["", 1, 2, 3, 4, 5, 6], key='Education'),
    'Income': st.selectbox("Select your approximate annual household income:", ["", 1, 2, 3, 4, 5, 6, 7, 8], key='Income')
}

# Add a submit button and validate required fields
if st.button('Submit'):
    # Check if any required field is not selected
    if "" in user_input.values():
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
    reset_selections()

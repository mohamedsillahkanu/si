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

# Collect user input
user_input = {
    'HighBP': st.selectbox("Do you have high blood pressure? Hint:0=No and 1=Yes", ["", 0, 1], key='HighBP'),
    'HighChol': st.selectbox("Have you been diagnosed with high cholesterol? Hint:0=No and 1=Yes", ["", 0, 1], key='HighChol'),
    'CholCheck': st.selectbox("Do you usually check your cholesterol? Hint:0=No and 1=Yes", ["", 0, 1], key='CholCheck'),
    'BMI': st.text_input("Enter your BMI:", "", key='BMI'),
    'Smoker': st.selectbox("Have you smoke at leat 100 cigarettes (5 packs) in your entire life? Hint:0=No and 1=Yes ", ["", 0, 1], key='Smoker'),
    'Stroke': st.selectbox("Ever been told you have stroke? Hint:0=No and 1=Yes", ["", 0, 1], key='Stroke'),
    'HeartDiseaseorAttack': st.selectbox("Have you been diagnosed with heart disease or suffered a heart attack? Hint:0=No and 1=Yes", ["", 0, 1], key='HeartDiseaseorAttack'),
    'PhysActivity': st.selectbox("Physical activity in the past 30 days-not including job? Hint:0=No and 1=Yes", ["", 0, 1], key='PhysActivity'),
    'Fruits': st.selectbox("Do you consume fruit more than one times per day? Hint:0=No and 1=Yes", ["", 0, 1], key='Fruits'),
    'Veggies': st.selectbox("Do you eat vegetables more than 1 time per day? Hint:0=No and 1=Yes", ["", 0, 1], key='Veggies'),
    'HvyAlcohol': st.selectbox("Do you consume more than 7 drinks of alcohol per week? Hint:0=No and 1=Yes", ["", 0, 1], key='HvyAlcohol'),
    'AnyHealthCare': st.selectbox("Do you have any kind of health care coverage? Hint:0=No and 1=Yes", ["", 0, 1], key='AnyHealthCare'),
    'NoDcbcCost': st.selectbox("Have you avoided visiting a doctor because of cost? Hint: 0=No, 1=Yes", ["", 0, 1], key='NoDcbcCost'),
    'GenHlth': st.selectbox("Would you say in general your health is: Hint: 1=Excellent, 2=Very Good, 3=Good, 4=Fair, 5=Poor", ["", 1, 2, 3, 4, 5], key='GenHlth'),
    'MentHlth': st.selectbox(" Days of poor mental health scales 1-30 days:", [""] + list(range(0, 31)), key='MentHlth'),  # Range from 0 to 30
    'PhysHlth': st.selectbox("Physical illness or injury days in past 30 days scale 1-30 days:", [""] + list(range(0, 31)), key='PhysHlth'),  # Range from 0 to 30
    'DiffWalk': st.selectbox("Do you experience difficulty walking or moving? Hint:0=No and 1=Yes", ["", 0, 1], key='DiffWalk'),
    'Sex': st.selectbox("Select your gender: Hint O=Female, 1=Male", ["", 0, 1], key='Sex'),
    'Age': st.selectbox("Select your age group: Hint: 1=18-24, 2=25-29, 3=30-34, 4=35-39, 5=40-44, 6=45-49, 7=50-54, 8=55-59, 9=60-64, 10=65-69, 11=70-74, 12=75-79, 13=80 and older", ["", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], key='Age'),
    'Education': st.selectbox("Select your highest education level: Hint: 1=Never Attended/only kindergarten, 2=grades 1-8, 3=grades 9-11, 4=grade 12 or GED, 5=college 1-3 years, 6=college 4+", ["", 1, 2, 3, 4, 5, 6], key='Education'),
    'Income': st.selectbox("Select your approximate annual household income: Hint: 1= Less than $10k, 2= Less than $15k, 3= Less than $20, 4= Less than $25k, 5= Less than $35, 6= Less than 50k, 7= Less than $75k, 8=More than $75k", ["", 1, 2, 3, 4, 5, 6, 7, 8], key='Income')
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
    for key in user_input:
        user_input[key] = ""

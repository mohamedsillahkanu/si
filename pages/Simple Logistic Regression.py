import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("Simple Logistic Regression")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Simple Logistic Regression")
    
    st.subheader("When to Use It")
    st.write("""
        Simple Logistic Regression is used to model the relationship between one or more independent variables 
        (predictors) and a binary dependent variable (outcome). This is particularly useful in cases where the 
        dependent variable is categorical with two levels, such as 'Positive'/'Negative' or 'Yes'/'No'.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("At least 20-30 samples per predictor variable are recommended for reliable results.")
    
    st.subheader("Number of Variables")
    st.write("One independent (predictor) variable and one binary dependent (outcome) variable are required.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of logistic regression is to predict the probability that the dependent variable equals 1
        (e.g., probability of testing positive for a disease) based on the independent variable(s).
    """)
    
    st.subheader("Real-Life Medical Example (Malaria)")
    st.write("Example of logistic regression applied in malaria research:")
    
    st.write("""
    1. **Malaria Diagnosis and Body Temperature**: A researcher might want to predict whether a patient has malaria
       (binary outcome: Positive/Negative) based on their body temperature (continuous predictor variable).
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Simple Logistic Regression")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        # Load the dataset
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the predictor and outcome variable
            predictor_column = st.selectbox("Select the predictor (independent) variable", df.columns)
            outcome_column = st.selectbox("Select the outcome (dependent) variable", df.columns)
            
            st.write(f"You selected: {predictor_column} as the predictor and {outcome_column} as the outcome.")
            
            # Convert the outcome column to numeric if it's categorical (e.g., 'Positive'/'Negative')
            if df[outcome_column].dtype == 'object':
                unique_values = df[outcome_column].unique()
                if len(unique_values) == 2:
                    df[outcome_column] = df[outcome_column].map({unique_values[0]: 0, unique_values[1]: 1})
                    st.write(f"Converted the outcome '{outcome_column}' from {unique_values} to [0, 1].")
                else:
                    st.error("The outcome variable must have exactly 2 unique values (e.g., binary outcome).")
                    st.stop()
            
            # Prepare the data for logistic regression
            X = df[[predictor_column]]  # Independent variable
            y = df[outcome_column]  # Dependent variable
            
            # Add a constant to the predictor variable (required for logistic regression)
            X = sm.add_constant(X)
            
            # Perform logistic regression
            model = sm.Logit(y, X)
            result = model.fit()
            
            st.subheader("Logistic Regression Results:")
            st.write(result.summary())
            
            # Plot the predicted probabilities
            df['predicted_prob'] = result.predict(X)
            
            plt.figure(figsize=(8, 6))
            sns.scatterplot(x=predictor_column, y=outcome_column, data=df, label="Actual")
            sns.lineplot(x=predictor_column, y='predicted_prob', data=df, color='red', label="Predicted Probability")
            plt.title("Logistic Regression Fit")
            plt.xlabel(predictor_column)
            plt.ylabel("Probability of " + outcome_column)
            st.pyplot(plt)
        
        except Exception as e:
            st.error(f"Error loading or processing the file: {e}")

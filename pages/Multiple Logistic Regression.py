import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import logit

# App title
st.title("Multiple Logistic Regression")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Multiple Logistic Regression")
    
    st.subheader("When to Use It")
    st.write("""
        Multiple logistic regression is used when the dependent variable is binary and you want to assess the 
        effect of multiple independent variables on the outcome probability. It helps in understanding 
        the relationship between the dependent variable and several predictors.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("A minimum sample size of 100 is recommended for reliable estimates in logistic regression, depending on the number of predictors.")
    
    st.subheader("Number of Categorical and Numeric Variables")
    st.write("Multiple logistic regression can include both categorical and numeric independent variables.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of multiple logistic regression is to model the relationship between a binary outcome 
        variable and multiple predictor variables, allowing for controlling confounding variables.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Impact of Socioeconomic Factors on Malaria Infection**: Multiple logistic regression can assess how various 
       socioeconomic factors (income level, education, etc.) affect the likelihood of being infected with malaria.
    """)
    
    st.write("""
    2. **Effect of Symptoms and Treatments on Malaria Outcomes**: This analysis can determine how different symptoms and treatment types 
       influence the probability of recovery from malaria.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Multiple Logistic Regression")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the dependent variable and independent variables
            dependent_var = st.selectbox("Select the dependent variable (binary)", df.columns)
            independent_vars = st.multiselect("Select independent variables", df.columns)
            
            if st.button("Run Logistic Regression"):
                # Fit the logistic regression model
                formula = f"{dependent_var} ~ " + " + ".join(independent_vars)
                model = logit(formula, data=df).fit()
                
                # Display the results
                st.write("Logistic Regression Results:")
                st.write(model.summary())
                
                # Display interpretation of coefficients
                st.write("Interpretation of Coefficients:")
                st.write(model.params)
                st.write("Odds Ratios:")
                st.write(np.exp(model.params))  # Odds ratios

        except Exception as e:
            st.error(f"Error loading file: {e}")

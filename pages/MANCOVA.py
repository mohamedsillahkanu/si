import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.multivariate.manova import MANOVA

# App title
st.title("MANCOVA Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: MANCOVA Test")
    
    st.subheader("When to Use It")
    st.write("""
        The MANCOVA (Multivariate Analysis of Covariance) test is used to assess the effect of independent categorical variables 
        on two or more dependent variables while controlling for one or more continuous covariates. It is particularly useful 
        when you have multiple outcomes and you want to see if the independent variables influence them, taking covariates into account.
    """)
    
    st.subheader("Number of Variables Required")
    st.write("""
        - At least two dependent variables (continuous).
        - One or more independent variables (categorical).
        - One or more covariates (continuous) to control for their effect.
    """)
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the MANCOVA test is to analyze whether the dependent variables vary across levels of the independent variables 
        while accounting for the covariates.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Effect of Malaria Treatment on Multiple Health Outcomes**: Researchers can use MANCOVA to determine if different malaria treatments 
       affect several health outcomes (e.g., hemoglobin levels and parasite counts), while controlling for age as a covariate.
    """)
    
    st.write("""
    2. **Impact of Region on Health Outcomes**: Researchers can analyze if malaria outcomes (e.g., recovery time and symptom severity) 
       differ across regions, while controlling for initial health status as a covariate.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: MANCOVA Test")
    
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
            
            # Ask the user to select dependent variables, independent variables, and covariates
            dependent_vars = st.multiselect("Select dependent variables (continuous)", df.columns)
            independent_var = st.selectbox("Select the independent variable (categorical)", df.columns)
            covariate = st.selectbox("Select the covariate (continuous)", df.columns)
            
            # Ensure that multiple dependent variables are selected
            if len(dependent_vars) < 2:
                st.error("Please select at least two dependent variables.")
            else:
                # Prepare the formula for the MANCOVA model
                formula = f"{'+'.join(dependent_vars)} ~ C({independent_var}) + {covariate}"
                st.write(f"Generated formula: {formula}")
                
                # Fit the MANCOVA model
                try:
                    mancova_model = MANOVA.from_formula(formula, data=df)
                    results = mancova_model.mv_test()
                    
                    st.subheader("MANCOVA Test Results")
                    st.write(results)
                    
                except Exception as e:
                    st.error(f"Error in running MANCOVA: {e}")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

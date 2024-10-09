import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.multivariate.manova import MANOVA

# App title
st.title("MANOVA: Multivariate Analysis of Variance")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: MANOVA")
    
    st.subheader("When to Use It")
    st.write("""
        MANOVA is used to determine whether there are any differences in the means of two or more dependent variables 
        based on one or more categorical independent variables. It extends the ANOVA by allowing multiple dependent variables
        to be analyzed simultaneously.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("You need data with at least two dependent variables and one or more categorical independent variables.")

    st.subheader("Number of Categorical and Numeric Variables")
    st.write("You need at least one categorical independent variable and two or more numeric dependent variables.")

    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of MANOVA is to assess whether the independent variable(s) have an effect on the combination of 
        dependent variables, and if so, how.
    """)

    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how MANOVA can be used in malaria research:")
    
    st.write("""
    1. **Effect of Region on Multiple Health Outcomes**: Researchers can use MANOVA to determine if region (independent variable) 
       affects multiple health outcomes, such as malaria infection rates, recovery times, and immune responses (dependent variables).
    """)
    
    st.write("""
    2. **Impact of Treatment Type on Multiple Patient Indicators**: The test can be used to evaluate if different treatments 
       (independent variable) for malaria affect patient indicators like blood pressure, body temperature, and hemoglobin levels (dependent variables).
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: MANOVA")
    
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
            
            # Ask the user to select the dependent and independent variables
            dependent_vars = st.multiselect("Select the dependent variables (numeric)", df.select_dtypes(include=[np.number]).columns)
            independent_var = st.selectbox("Select the independent variable (categorical)", df.select_dtypes(include=['object', 'category']).columns)
            
            if dependent_vars and independent_var:
                # Perform MANOVA
                dependent_vars_str = " + ".join(dependent_vars)
                formula = f"{dependent_vars_str} ~ {independent_var}"
                
                manova = MANOVA.from_formula(formula, data=df)
                result = manova.mv_test()
                
                # Extract results and display them in a tabular format
                st.write("MANOVA Test Results:")
                st.write(result)
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

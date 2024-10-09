import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.multivariate.manova import MANOVA

# App title
st.title("MANOVA Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: MANOVA")
    
    st.subheader("When to Use It")
    st.write("""
        MANOVA (Multivariate Analysis of Variance) is used to test if two or more dependent variables 
        are influenced by one or more independent categorical variables. It's an extension of ANOVA 
        that allows for multiple dependent variables.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("""
        You need data with at least one independent categorical variable and two or more dependent numeric variables. 
        Each category should have enough observations for analysis, ideally at least 10 samples per category.
    """)
    
    st.subheader("Number of Variables")
    st.write("""
        - **Dependent Variables**: Two or more continuous numeric variables.
        - **Independent Variable**: One or more categorical variables.
    """)
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of MANOVA is to determine if the combination of dependent variables is influenced 
        by the categorical independent variables. This test is helpful in analyzing multivariate data.
    """)
    
    st.subheader("Real-Life Medical Example (Malaria)")
    st.write("""
    **Malaria Treatment Effect on Health Indicators**: MANOVA can be used to test whether different malaria treatment methods 
    (e.g., Drug A, Drug B, Placebo) affect multiple health indicators such as `Blood Pressure` and `Hemoglobin Level` after treatment.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: MANOVA")

    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        try:
            # Load the dataset
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the independent variable (categorical) and dependent variables (numeric)
            independent_var = st.selectbox("Select the independent (categorical) variable", df.columns)
            dependent_vars = st.multiselect("Select the dependent (numeric) variables (select two or more)", df.select_dtypes(include=[np.number]).columns)
            
            if len(dependent_vars) >= 2:
                st.write(f"You selected {independent_var} as the independent variable and {dependent_vars} as the dependent variables.")
                
                # Fit MANOVA model
                formula = f"{' + '.join(dependent_vars)} ~ {independent_var}"
                manova = MANOVA.from_formula(formula, data=df)
                result = manova.mv_test()
                
                # Display the MANOVA test results
                st.write("MANOVA Test Results:")
                st.write(result)
            else:
                st.warning("Please select at least two dependent variables for the MANOVA test.")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.multivariate.manova import MANOVA

# App title
st.title("MANCOVA (Multivariate Analysis of Covariance)")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: MANCOVA")

    st.subheader("When to Use It")
    st.write("""
        The MANCOVA is used to evaluate whether two or more population means on multiple dependent variables 
        are equal across levels of a categorical independent variable, while controlling for the effects of covariates.
    """)

    st.subheader("Number of Samples Required")
    st.write("At least two dependent variables and one or more covariates are required, with a sufficient sample size depending on your data.")

    st.subheader("Number of Variables")
    st.write("""
        - Dependent Variables: 2 or more continuous variables.
        - Independent Variable: Categorical variable (factor).
        - Covariate: A continuous variable that may influence the dependent variables.
    """)

    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of MANCOVA is to determine if there is a significant difference between groups on multiple dependent variables,
        while accounting for the influence of covariates.
    """)

    st.subheader("Real-Life Medical Examples")
    st.write("""
        1. **Effect of Malaria Treatments on Multiple Health Outcomes**: MANCOVA can be used to test whether different malaria treatment methods (e.g., drug A vs. drug B) 
           have significant effects on multiple health outcomes, such as fever reduction and recovery time, while controlling for age.
        
        2. **Impact of Malaria Prevention on Multiple Health Indicators**: You can use MANCOVA to see if different prevention methods (e.g., bed nets vs. no bed nets) 
           impact health indicators like infection rate and hospital visits, while controlling for factors such as region or household size.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: MANCOVA")

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

            # Select dependent variables, independent variable, and covariate
            dep_vars = st.multiselect("Select the dependent variables (2 or more)", df.columns)
            indep_var = st.selectbox("Select the independent (categorical) variable", df.columns)
            covariate = st.selectbox("Select the covariate (continuous)", df.columns)

            if len(dep_vars) >= 2:
                # Prepare the MANCOVA model
                formula = f"{' + '.join(dep_vars)} ~ {indep_var} + {covariate}"
                model = MANOVA.from_formula(formula, data=df)
                result = model.mv_test()

                st.write("MANCOVA Results:")
                # Display the results in a tabular form
                result_table = result.summary().tables[0]
                st.write(result_table)
            
        except Exception as e:
            st.error(f"Error loading file: {e}")

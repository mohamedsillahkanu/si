import streamlit as st
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tools import add_constant

# App title
st.title("Analysis of Covariance (ANCOVA)")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: ANCOVA")
    
    st.subheader("When to Use It")
    st.write("""
        ANCOVA is used when you want to compare the means of a dependent variable across two or more groups,
        while controlling for the influence of one or more continuous covariates.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("You need data with at least one categorical independent variable, one continuous dependent variable, and one covariate.")

    st.subheader("Number of Categorical and Numeric Variables")
    st.write("You need at least one categorical variable and one continuous covariate to use ANCOVA.")

    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of ANCOVA is to determine if there are significant differences in the dependent variable
        across groups while adjusting for the covariate(s), which may influence the dependent variable.
    """)

    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how ANCOVA can be used in malaria research:")
    
    st.write("""
    1. **Malaria Treatment Effectiveness by Age**: ANCOVA can be used to compare the effectiveness of different malaria treatments (categorical) 
       on recovery time (continuous) while controlling for the patient's age (continuous covariate).
    """)
    
    st.write("""
    2. **Malaria Intervention Impact by Region**: It can assess the impact of different interventions (categorical, e.g., use of bed nets) 
       on infection rates (continuous), while controlling for average regional rainfall (continuous covariate).
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: ANCOVA")
    
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
            
            # Select variables for ANCOVA
            dep_var = st.selectbox("Select the dependent variable (continuous)", df.select_dtypes(include=['float64', 'int64']).columns)
            covariate = st.selectbox("Select the covariate (continuous)", df.select_dtypes(include=['float64', 'int64']).columns)
            cat_var = st.selectbox("Select the independent variable (categorical)", df.select_dtypes(include=['object', 'category']).columns)
            
            st.write(f"You selected: Dependent Variable = {dep_var}, Covariate = {covariate}, Independent Variable = {cat_var}")
            
            # Perform ANCOVA
            st.write("Performing ANCOVA...")

            # Create the formula for ANCOVA
            formula = f'{dep_var} ~ {cat_var} + {covariate}'

            # Fit the model
            ancova_model = smf.ols(formula, data=df).fit()

            # Display results
            st.write("ANCOVA Results:")
            st.write(ancova_model.summary())

            # Interpretation of results
            st.write("""
            The ANCOVA results include the F-statistics and p-values for both the categorical variable and the covariate.
            If the p-value for the categorical variable is below 0.05, it indicates that the groups have significantly different means after controlling for the covariate.
            """)

        except Exception as e:
            st.error(f"Error loading file: {e}")

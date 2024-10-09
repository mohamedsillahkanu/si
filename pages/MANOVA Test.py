import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.multivariate.manova import MANOVA

# App title
st.title("Multivariate Analysis of Variance (MANOVA)")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: MANOVA")
    
    st.subheader("When to Use It")
    st.write("""
        MANOVA is used when you have two or more dependent variables and one or more categorical independent variables. 
        It assesses whether the mean differences between groups on multiple dependent variables are statistically significant.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("You need data with at least two continuous (numeric) dependent variables and one or more categorical independent variables.")
    
    st.subheader("Number of Variables")
    st.write("""
    - Dependent variables: Two or more numeric variables.
    - Independent variable: One or more categorical variables.
    """)
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of MANOVA is to test the hypothesis that the dependent variable means are equal across groups, taking into 
        account multiple dependent variables at once.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("""
    1. **Blood Count and Parasite Density by Treatment Group**: Researchers can use MANOVA to compare the means of blood count and parasite density 
       across different malaria treatment groups.
    """)
    
    st.write("""
    2. **Hemoglobin and Platelet Levels by Malaria Status**: MANOVA can assess whether there are significant differences in hemoglobin and platelet levels 
       between malaria-positive and malaria-negative patients.
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
            
            # Ask the user to select dependent and independent variables
            dep_vars = st.multiselect("Select dependent variables (numeric)", df.select_dtypes(include=np.number).columns)
            indep_var = st.selectbox("Select the independent variable (categorical)", df.select_dtypes(include='object').columns)
            
            if len(dep_vars) >= 2:
                # Perform MANOVA
                dep_vars_str = ' + '.join(dep_vars)
                formula = f"{dep_vars_str} ~ {indep_var}"
                manova = MANOVA.from_formula(formula, data=df)
                result = manova.mv_test()

                st.subheader("MANOVA Results:")
                
                # Display results in a tabular format
                st.write(result)
                
                # Extract the results to display in a more readable table
                result_table = result.results[0].summary_frame()
                st.write(result_table)
            else:
                st.warning("Please select at least two dependent variables.")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.stats.contingency_tables import StratifiedTable

# App title
st.title("Cochran-Mantel-Haenszel Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Cochran-Mantel-Haenszel Test")
    
    st.subheader("When to Use It")
    st.write("""
        The Cochran-Mantel-Haenszel (CMH) test is used to test for an association between two categorical variables 
        while controlling for the effect of a third categorical variable (stratification). This test is useful when
        you want to assess whether the relationship between two variables is consistent across different strata or
        groups of a third variable.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("You need data with at least two categorical variables, and a third variable to act as the strata.")
    
    st.subheader("Number of Categorical Variables")
    st.write("Three categorical variables are required: two variables for the contingency table and one for stratification.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the CMH test is to determine if the association between two categorical variables holds 
        consistently across different strata defined by a third categorical variable.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Malaria Symptoms and Diagnostic Results by Age Group**: Researchers can use the CMH test to determine if there is an association 
       between malaria symptoms (e.g., fever, chills) and diagnostic test results (positive/negative), while controlling for different age groups.
    """)
    
    st.write("""
    2. **Malaria Prevention Methods and Infection Status by Region**: The CMH test can assess whether the association between the use of prevention 
       methods (e.g., bed nets) and malaria infection status is consistent across different regions.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Cochran-Mantel-Haenszel Test")
    
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
            
            # Ask the user to select the two categorical columns for the contingency table and one for the strata
            cat_column1 = st.selectbox("Select the first categorical variable", df.columns)
            cat_column2 = st.selectbox("Select the second categorical variable", df.columns)
            strata_column = st.selectbox("Select the stratification variable", df.columns)
            
            st.write(f"You selected: {cat_column1}, {cat_column2}, and {strata_column} for the test.")
            
            # Build stratified tables
            tables = []
            for stratum in df[strata_column].unique():
                subset = df[df[strata_column] == stratum]
                contingency_table = pd.crosstab(subset[cat_column1], subset[cat_column2])
                tables.append(contingency_table.values)
            
            # Perform Cochran-Mantel-Haenszel Test
            cmh_test = StratifiedTable(tables)
            result = cmh_test.test_null_odds()
            
            # Display test results
            st.write("Cochran-Mantel-Haenszel Test Results:")
            st.write(f"Test Statistic: {result.statistic}")
            st.write(f"p-value: {result.pvalue}")
            
            # Interpretation of results
            if result.pvalue < 0.05:
                st.write("The association between the two variables is statistically significant across strata (Reject H0).")
            else:
                st.write("There is no significant association between the two variables across strata (Fail to reject H0).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import wilcoxon

# App title
st.title("Wilcoxon Signed-Rank Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Wilcoxon Signed-Rank Test")
    
    st.subheader("When to Use It")
    st.write("""
        The Wilcoxon Signed-Rank Test is used to compare two related samples or repeated measurements 
        on a single sample to assess whether their population mean ranks differ. It is often used as an alternative 
        to the paired t-test when the data does not meet the assumption of normality.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("You need two related samples or paired observations, typically the same subjects measured under two different conditions or times.")
    
    st.subheader("Number of Numeric Variables")
    st.write("Two numeric variables representing the two related samples.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The Wilcoxon Signed-Rank Test is used to determine whether there is a significant difference between two related samples or 
        repeated measurements under two conditions, without assuming a normal distribution.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Comparing Pre-Treatment and Post-Treatment Malaria Parasite Count**: Researchers can use the Wilcoxon Signed-Rank Test to determine if there is 
       a significant difference in parasite count before and after treatment in the same group of patients.
    """)
    
    st.write("""
    2. **Effect of Two Different Anti-Malaria Drugs on Blood Hemoglobin Levels**: The test can compare the hemoglobin levels before and after 
       treatment with two different drugs in the same set of patients.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Wilcoxon Signed-Rank Test")
    
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
            
            # Ask the user to select the two numeric columns for the Wilcoxon Signed-Rank Test
            numeric_columns = df.select_dtypes(include=['number']).columns
            col1 = st.selectbox("Select the first numeric variable (e.g., before treatment)", numeric_columns)
            col2 = st.selectbox("Select the second numeric variable (e.g., after treatment)", numeric_columns)
            
            st.write(f"You selected: {col1} and {col2} for the test.")
            
            # Perform the Wilcoxon Signed-Rank Test
            stat, p_value = wilcoxon(df[col1], df[col2])
            
            # Display test results
            st.write("Wilcoxon Signed-Rank Test Results:")
            st.write(f"Test Statistic: {stat}")
            st.write(f"p-value: {p_value}")
            
            # Interpretation of results
            if p_value < 0.05:
                st.write("There is a significant difference between the two related samples (Reject H0).")
            else:
                st.write("There is no significant difference between the two related samples (Fail to reject H0).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

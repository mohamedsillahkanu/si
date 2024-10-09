import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import wilcoxon

# App title
st.title("Sign Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Sign Test")
    
    st.subheader("When to Use It")
    st.write("""
        The Sign Test is a non-parametric test used to assess whether the median of a single sample 
        differs from a specified value. It is also used for paired samples to evaluate whether their 
        median differences are zero.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("You need a minimum of 5 samples for the test to be meaningful.")
    
    st.subheader("Number of Categorical Variables")
    st.write("The Sign Test is typically used with one continuous variable.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the Sign Test is to determine if there is a significant difference between the 
        median of a sample and a hypothesized median or between two related samples.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Efficacy of a New Treatment**: Researchers can compare the median time to recovery for patients treated with a new malaria treatment 
       against a known median recovery time to assess its efficacy.
    """)
    
    st.write("""
    2. **Change in Parasite Load**: The Sign Test can be used to analyze the median change in parasite load (measured before and after treatment) 
       for a group of patients to see if the treatment significantly reduces the load.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Sign Test")
    
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
            
            # Ask the user to select the column for the test
            variable_column = st.selectbox("Select the continuous variable for the Sign Test", df.columns)
            hypothesized_median = st.number_input("Enter the hypothesized median", value=0.0)
            
            # Perform Sign Test
            differences = df[variable_column] - hypothesized_median
            sign_test_results = wilcoxon(differences[differences != 0])
            
            # Display test results
            st.write("Sign Test Results:")
            st.write(f"Test Statistic: {sign_test_results.statistic}")
            st.write(f"p-value: {sign_test_results.pvalue}")
            
            # Interpretation of results
            if sign_test_results.pvalue < 0.05:
                st.write("The median differs significantly from the hypothesized median (Reject H0).")
            else:
                st.write("There is no significant difference from the hypothesized median (Fail to reject H0).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

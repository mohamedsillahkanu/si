import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

# App title
st.title("One-Sample t-Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: One-Sample t-Test")
    
    st.subheader("When to Use It")
    st.write("""
        The One-Sample t-Test is used to determine whether the mean of a sample is significantly different 
        from a known or hypothesized population mean. 
    """)
    
    st.subheader("Number of Samples Required")
    st.write("The test requires a single sample of numeric data.")
    
    st.subheader("Number of Numeric Variables")
    st.write("One numeric variable is needed for the test, which will be compared to a specified population mean.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the One-Sample t-Test is to test the null hypothesis that the sample mean equals the 
        population mean (H0: μ = μ0). The alternative hypothesis is that the sample mean differs from the population mean (H1: μ ≠ μ0).
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples related to malaria:")
    
    st.write("""
    1. **Average Parasite Count in Malaria Patients**: You could use a one-sample t-test to determine if the average parasite count in a sample of malaria patients 
       differs from the expected population mean parasite count in a certain region.
    """)
    
    st.write("""
    2. **Average Recovery Time after Malaria Treatment**: Researchers can use the test to determine if the average recovery time of malaria patients from a specific hospital 
       differs from the standard recovery time known in malaria treatment protocols.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: One-Sample t-Test")
    
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
            
            # Ask the user to select a numeric column for the test
            numeric_column = st.selectbox("Select the numeric variable for the t-test", df.select_dtypes(include=[np.number]).columns)
            
            # Ask the user to input the population mean
            pop_mean = st.number_input("Enter the hypothesized population mean", step=0.1)
            
            # Perform One-Sample t-Test
            sample_data = df[numeric_column].dropna()  # Remove missing values
            t_stat, p_value = stats.ttest_1samp(sample_data, pop_mean)
            
            # Display test results
            st.write(f"One-Sample t-Test Results:")
            st.write(f"Test Statistic (t): {t_stat:.4f}")
            st.write(f"p-value: {p_value:.4f}")
            
            # Interpretation of results
            if p_value < 0.05:
                st.write("The sample mean is significantly different from the population mean (Reject H0).")
            else:
                st.write("There is no significant difference between the sample mean and the population mean (Fail to reject H0).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

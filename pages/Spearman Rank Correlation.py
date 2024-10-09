import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import spearmanr

# App title
st.title("Spearman Rank Correlation")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Spearman Rank Correlation")
    
    st.subheader("When to Use It")
    st.write("""
        Spearman's rank correlation coefficient is used to measure the strength and direction of the association 
        between two ranked variables. It is a non-parametric measure and is useful when the data does not 
        necessarily follow a normal distribution.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("At least two paired samples are required to perform this test.")
    
    st.subheader("Number of Categorical Variables")
    st.write("Two numeric variables are required for the test.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the Spearman rank correlation test is to assess the degree to which the relationship 
        between two variables can be described by a monotonic function.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Correlation Between Fever Duration and Parasite Density**: Researchers can use the Spearman test 
       to assess whether there is a correlation between the duration of fever in malaria patients and the 
       density of parasites in their blood samples.
    """)
    
    st.write("""
    2. **Correlation Between Treatment Duration and Recovery Rate**: The Spearman rank correlation can be 
       used to examine the relationship between the duration of malaria treatment and the rate of recovery 
       among patients.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Spearman Rank Correlation")
    
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
            
            # Ask the user to select two numeric columns for correlation analysis
            numeric_column1 = st.selectbox("Select the first numeric variable", df.select_dtypes(include=[np.number]).columns)
            numeric_column2 = st.selectbox("Select the second numeric variable", df.select_dtypes(include=[np.number]).columns)
            
            st.write(f"You selected: {numeric_column1} and {numeric_column2} for the test.")
            
            # Perform Spearman rank correlation
            correlation, p_value = spearmanr(df[numeric_column1], df[numeric_column2])
            
            # Display test results
            st.write("Spearman Rank Correlation Results:")
            st.write(f"Spearman's correlation coefficient: {correlation:.4f}")
            st.write(f"p-value: {p_value:.4f}")
            
            # Interpretation of results
            if p_value < 0.05:
                st.write("The correlation is statistically significant (Reject H0).")
            else:
                st.write("There is no significant correlation (Fail to reject H0).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

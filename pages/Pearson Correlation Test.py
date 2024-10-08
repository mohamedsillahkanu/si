import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# App title
st.title("Pearson Correlation Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Pearson Correlation Test")
    
    st.subheader("When to Use It")
    st.write("""
        Pearson correlation is used to measure the linear relationship between two continuous numeric variables.
        It helps determine how closely the two variables are linearly related. The closer the Pearson coefficient
        is to +1 or -1, the stronger the linear relationship.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("The Pearson correlation works best with a moderate to large number of samples (generally > 30 samples).")
    
    st.subheader("Number of Numeric Variables")
    st.write("Two continuous (numeric) variables are required to perform the Pearson correlation test.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the Pearson correlation test is to quantify the strength and direction of the linear
        relationship between two continuous variables.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Malaria Parasite Density vs. Fever Severity**: Researchers can use the Pearson correlation to assess whether there is a linear relationship
       between malaria parasite density in blood and the severity of fever in patients.
    """)
    
    st.write("""
    2. **Temperature and Malaria Incidence**: The test can be used to analyze if there is a linear relationship between average temperature
       and malaria incidence rates in a given region.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Pearson Correlation Test")
    
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
            
            # Ask the user to select two numeric columns
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_columns) < 2:
                st.error("Your dataset must contain at least two numeric variables for Pearson correlation.")
            else:
                num_column1 = st.selectbox("Select the first numeric variable", numeric_columns)
                num_column2 = st.selectbox("Select the second numeric variable", numeric_columns)
                
                st.write(f"You selected: {num_column1} and {num_column2} for the test.")
                
                # Calculate Pearson correlation
                correlation, p_value = pearsonr(df[num_column1], df[num_column2])
                
                # Display results
                st.write(f"Pearson Correlation Coefficient: {correlation:.3f}")
                st.write(f"p-value: {p_value:.3f}")
                
                # Interpretation of results
                if p_value < 0.05:
                    st.write("The correlation is statistically significant (p < 0.05).")
                else:
                    st.write("The correlation is not statistically significant (p ≥ 0.05).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.multivariate.cancorr import CanCorr

# App title
st.title("Canonical Correlation Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Canonical Correlation Analysis")
    
    st.subheader("When to Use It")
    st.write("""
        Canonical Correlation Analysis (CCA) is used to examine the relationships between two sets of multivariate variables. 
        It is particularly useful when you want to understand how two sets of variables influence each other.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("There is no strict rule for the number of samples, but generally, you need at least 20 samples per variable.")
    
    st.subheader("Number of Categorical Variables")
    st.write("CCA is primarily used with continuous variables; however, categorical variables can be included by converting them into dummy variables.")
    
    st.subheader("Number of Numeric Variables")
    st.write("You should have at least two sets of numeric variables to perform the analysis.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of Canonical Correlation Analysis is to explore the relationships between two sets of variables and to identify 
        the most important relationships that exist between them.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Relationship Between Symptoms and Laboratory Results**: CCA can be used to investigate how different malaria symptoms relate to various laboratory test results (e.g., blood counts, parasite counts).
    """)
    
    st.write("""
    2. **Effect of Environmental Factors on Malaria Incidence**: CCA can be applied to assess how environmental factors (e.g., rainfall, temperature) influence the incidence of malaria cases across different regions.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Canonical Correlation Analysis")
    
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
            
            # Ask the user to select two sets of variables for analysis
            st.subheader("Select the variable sets for CCA")
            set1_columns = st.multiselect("Select variables for Set 1", df.columns)
            set2_columns = st.multiselect("Select variables for Set 2", df.columns)
            
            if set1_columns and set2_columns:
                st.write(f"You selected: Set 1: {set1_columns}, Set 2: {set2_columns}.")
                
                # Perform Canonical Correlation Analysis
                X = df[set1_columns]
                Y = df[set2_columns]
                
                cancorr = CanCorr(X, Y)
                cancorr.fit()
                
                # Display results
                st.write("Canonical Correlations:")
                st.write(cancorr.cancorr)
                
                # Display coefficients
                st.write("Coefficients for Set 1:")
                st.write(cancorr.xcoef)
                
                st.write("Coefficients for Set 2:")
                st.write(cancorr.ycoef)

        except Exception as e:
            st.error(f"Error loading file: {e}")

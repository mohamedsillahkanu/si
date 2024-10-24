import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import friedmanchisquare

# App title
st.title("Friedman Test Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Friedman Test Overview", "Friedman Test Illustration"])

# 1. Friedman Test Overview Section
if section == "Friedman Test Overview":
    st.header("Friedman Test for Statistical Analysis")
    
    st.subheader("When to Use It")
    st.write("""
        The Friedman Test is a non-parametric statistical test used to detect differences in treatments across multiple test attempts.
        It is an alternative to the repeated-measures ANOVA when the assumption of normality is not met.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using the Friedman Test:")
    st.write("1. **Three or More Related Samples**: Measurements taken under different conditions or at different times for the same subjects.")
    
    st.subheader("Purpose of the Friedman Test")
    st.write("""
        The purpose of the Friedman Test is to determine if there are statistically significant differences between the distributions of the related samples.
    """)
    
    st.write("For more information, visit the [Wikipedia page on the Friedman Test](https://en.wikipedia.org/wiki/Friedman_test).")

# 2. Friedman Test Illustration Section
elif section == "Friedman Test Illustration":
    st.header("Friedman Test Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="friedman_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the relevant columns
            columns = st.multiselect("Select the columns representing the related samples", df.columns)
            
            if len(columns) >= 3:
                # Perform the Friedman Test
                data = [df[col] for col in columns]
                stat, p_value = friedmanchisquare(*data)
                
                # Display the results
                st.subheader("Friedman Test Results")
                st.write(f"Test Statistic: {stat}")
                st.write(f"P-value: {p_value}")
                
                # Interpretation tips
                st.subheader("How to Interpret the Results")
                st.write("""
                    - **Test Statistic**: The test statistic indicates the degree of difference between the groups.
                    - **P-value**: A p-value less than 0.05 indicates that there are significant differences between the groups.
                    
                    If the p-value is significant, you can conclude that at least one of the samples differs from the others.
                """)
            else:
                st.warning("Please select at least three columns for the Friedman Test.")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



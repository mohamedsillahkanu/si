import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kendalltau

# App title
st.title("Kendall's Tau Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Kendall's Tau Overview", "Kendall's Tau Illustration"])

# 1. Kendall's Tau Overview Section
if section == "Kendall's Tau Overview":
    st.header("Kendall's Tau for Correlation Analysis")
    
    st.subheader("When to Use It")
    st.write("""
        Kendall's Tau is a non-parametric statistic used to measure the ordinal association between two measured quantities.
        It is used to determine the strength and direction of the relationship between two variables, particularly when the data is not normally distributed.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using Kendall's Tau:")
    st.write("1. **Two Continuous or Ordinal Variables**: The variables for which you want to determine the correlation.")
    
    st.subheader("Purpose of Kendall's Tau")
    st.write("""
        The purpose of calculating Kendall's Tau is to assess the strength and direction of association between two variables. 
        A positive value indicates a positive association, while a negative value indicates a negative association.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Kendall's Tau](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient).")

# 2. Kendall's Tau Illustration Section
elif section == "Kendall's Tau Illustration":
    st.header("Kendall's Tau Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="kendall_file")
    
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
            column1 = st.selectbox("Select the first variable", df.columns)
            column2 = st.selectbox("Select the second variable", df.columns)
            
            # Calculate Kendall's Tau
            tau, p_value = kendalltau(df[column1], df[column2])
            
            # Display the results
            st.subheader("Kendall's Tau Results")
            st.write(f"Kendall's Tau: {tau}")
            st.write(f"P-value: {p_value}")
            
            # Interpretation tips
            st.subheader("How to Interpret the Results")
            st.write("""
                - **Kendall's Tau Value**: A positive value indicates a positive association, while a negative value indicates a negative association between the variables.
                - **P-value**: A p-value less than 0.05 indicates that the association is statistically significant.
                
                The closer the Kendall's Tau value is to 1 or -1, the stronger the association. A value close to 0 indicates little to no association.
            """)
                
        except Exception as e:
            st.error(f"Error loading file: {e}")


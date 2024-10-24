import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import f_oneway

# App title
st.title("F-Test Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["F-Test Overview", "F-Test Illustration"])

# 1. F-Test Overview Section
if section == "F-Test Overview":
    st.header("F-Test for Comparing Variances or Means")
    
    st.subheader("When to Use It")
    st.write("""
        The F-Test is used to compare the variances or means of two or more groups. It is commonly used in ANOVA (Analysis of Variance) to determine if the means of multiple groups are significantly different.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using the F-Test:")
    st.write("1. **Two or More Independent Samples**: The samples should be normally distributed, and the data should be continuous.")
    
    st.subheader("Purpose of the F-Test")
    st.write("""
        The purpose of the F-Test is to determine if there are significant differences between the variances or means of the groups. It helps assess whether the observed differences are due to random chance or a significant factor.
    """)
    
    st.write("For more information, visit the [Wikipedia page on the F-Test](https://en.wikipedia.org/wiki/F-test).")

# 2. F-Test Illustration Section
elif section == "F-Test Illustration":
    st.header("F-Test Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="ftest_file")
    
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
            columns = st.multiselect("Select the columns representing the groups", df.columns)
            
            if len(columns) >= 2:
                # Perform the F-Test
                data = [df[col] for col in columns]
                stat, p_value = f_oneway(*data)
                
                # Display the results
                st.subheader("F-Test Results")
                st.write(f"F-Statistic: {stat}")
                st.write(f"P-value: {p_value}")
                
                # Interpretation tips
                st.subheader("How to Interpret the Results")
                st.write("""
                    - **F-Statistic**: The F-statistic indicates the ratio of the variance between the groups to the variance within the groups.
                    - **P-value**: A p-value less than 0.05 indicates that there are significant differences between the groups.
                    
                    If the p-value is significant, you can conclude that at least one of the group means differs from the others.
                """)
            else:
                st.warning("Please select at least two columns for the F-Test.")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



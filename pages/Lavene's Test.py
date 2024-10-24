import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import levene

# App title
st.title("Levene's Test for Homogeneity of Variances")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Levene's Test Overview", "Levene's Test Illustration"])

# 1. Levene's Test Overview Section
if section == "Levene's Test Overview":
    st.header("Levene's Test for Comparing Variances")
    
    st.subheader("When to Use It")
    st.write("""
        Levene's Test is used to assess the equality of variances for a variable calculated for two or more groups. It is particularly useful for testing the assumption of homogeneity of variances before conducting ANOVA.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using Levene's Test:")
    st.write("1. **Two or More Independent Samples**: The samples should be from different groups, and the data should be continuous.")
    
    st.subheader("Purpose of Levene's Test")
    st.write("""
        The purpose of Levene's Test is to determine if the variances of the groups are equal. 
        A significant result indicates that the variances are not equal, which may violate the assumptions of certain statistical tests like ANOVA.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Levene's Test](https://en.wikipedia.org/wiki/Levene%27s_test).")

# 2. Levene's Test Illustration Section
elif section == "Levene's Test Illustration":
    st.header("Levene's Test Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="levene_file")
    
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
                # Perform Levene's Test
                data = [df[col] for col in columns]
                stat, p_value = levene(*data)
                
                # Display the results
                st.subheader("Levene's Test Results")
                st.write(f"Levene Statistic: {stat}")
                st.write(f"P-value: {p_value}")
                
                # Interpretation tips
                st.subheader("How to Interpret the Results")
                st.write("""
                    - **Levene Statistic**: The Levene statistic indicates the degree of difference in the variances of the groups.
                    - **P-value**: A p-value less than 0.05 indicates that the variances are significantly different.
                    
                    If the p-value is significant, you can conclude that the variances are not equal across the groups.
                """)
            else:
                st.warning("Please select at least two columns for Levene's Test.")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



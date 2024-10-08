import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

# App title
st.title("Paired T-Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Paired T-Test")
    
    st.subheader("When to Use It")
    st.write("""
        The Paired T-Test is used to compare the means of two related groups, typically before and after some intervention or treatment.
        It helps determine whether there is a statistically significant difference between the two sets of observations.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("You need at least two related samples for this test. For example, you can have 'pre-treatment' and 'post-treatment' values for each individual.")

    st.subheader("Number of Numeric Variables")
    st.write("Two numeric variables that are related to each other are required.")

    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the Paired T-Test is to determine whether there is a significant difference in the mean values of two related groups.
        This test is often used in clinical research to assess the impact of a treatment, intervention, or change in conditions.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("""
        1. **Malaria Treatment Effectiveness**: Comparing the malaria parasite count before and after administering a new drug in a group of patients.
        2. **Malaria Symptoms Before and After Treatment**: Assessing whether a significant reduction in fever symptoms occurs before and after treatment in malaria patients.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Paired T-Test")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        try:
            # Load the dataset based on file type
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select two related numeric columns for the paired t-test
            numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
            col1 = st.selectbox("Select the first numeric column (before treatment)", numeric_columns)
            col2 = st.selectbox("Select the second numeric column (after treatment)", numeric_columns)
            
            st.write(f"You selected: {col1} (Before) and {col2} (After) for the Paired T-Test.")
            
            # Perform Paired T-Test
            t_stat, p_value = stats.ttest_rel(df[col1], df[col2])
            
            # Display the results
            st.write("Paired T-Test Results:")
            st.write(f"T-Statistic: {t_stat}")
            st.write(f"P-Value: {p_value}")
            
            # Interpretation of results
            if p_value < 0.05:
                st.write("The difference between the two groups is statistically significant (Reject H0).")
            else:
                st.write("There is no significant difference between the two groups (Fail to reject H0).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

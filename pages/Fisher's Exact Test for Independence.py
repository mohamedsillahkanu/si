import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import fisher_exact

# App title
st.title("Fisher's Exact Test for Independence")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Fisher's Exact Test")
    
    st.subheader("When to Use It")
    st.write("""
        Fisher's Exact Test is used when you have two categorical variables, and you want to determine if 
        there is a significant association between the two variables. This test is particularly useful when 
        sample sizes are small and the expected frequencies in any of the cells of a contingency table are low.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("This test is designed for analyzing 2x2 contingency tables (two categorical variables).")
    
    st.subheader("Number of Categorical Variables")
    st.write("You need two categorical variables for this test, each with two levels (or more).")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of Fisher's Exact Test is to determine whether there is a non-random association 
        between two categorical variables.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Drug Efficacy and Malaria Strain**: 
       A researcher can use Fisher's Exact Test to determine if there is a significant association between 
       malaria strain (e.g., strain A or strain B) and the efficacy of a certain drug (e.g., effective or not effective).
    """)
    
    st.write("""
    2. **Presence of Symptoms and Diagnostic Test Results**: 
       The test can help to identify if there is a significant association between the presence of specific malaria symptoms 
       (e.g., fever or no fever) and the result of a diagnostic test (positive or negative).
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Fisher's Exact Test")
    
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
            
            # Ask the user to select the two categorical columns for the 2x2 contingency table
            cat_column1 = st.selectbox("Select the first categorical variable", df.columns)
            cat_column2 = st.selectbox("Select the second categorical variable", df.columns)
            
            st.write(f"You selected: {cat_column1} and {cat_column2} for the test.")
            
            # Generate the contingency table
            contingency_table = pd.crosstab(df[cat_column1], df[cat_column2])
            st.write("Contingency Table (Observed Frequencies):")
            st.write(contingency_table)
            
            # Check if the table is 2x2 (Fisher's Exact Test works for 2x2 tables)
            if contingency_table.shape == (2, 2):
                # Perform Fisher's Exact Test
                oddsratio, p_value = fisher_exact(contingency_table)
                
                st.write("Fisher's Exact Test Results:")
                st.write(f"Odds Ratio: {oddsratio}")
                st.write(f"p-value: {p_value}")
                
                # Interpretation of results
                if p_value < 0.05:
                    st.write("The association between the two variables is statistically significant (Reject H0).")
                else:
                    st.write("There is no significant association between the two variables (Fail to reject H0).")
            else:
                st.error("Fisher's Exact Test is only applicable to 2x2 contingency tables. Please select two categorical variables with exactly two levels each.")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import bartlett

# App title
st.title("Bartlett's Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Bartlett's Test")
    
    st.subheader("When to Use It")
    st.write("""
        Bartlett's test is used to test the null hypothesis that multiple samples have equal variances. 
        It is particularly useful in ANOVA when the assumption of equal variances is critical.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("You need at least three samples (groups) to perform Bartlett's test.")
    
    st.subheader("Number of Categorical Variables")
    st.write("Bartlett's test requires at least one categorical variable to define the groups being compared.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of Bartlett's test is to assess whether the variances of multiple groups are equal. 
        A significant result indicates that at least one group has a different variance.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Comparison of Treatment Variability**: Researchers can use Bartlett's test to compare the variances of treatment outcomes 
       (e.g., reduction in malaria symptoms) across different treatment groups (e.g., different medications).
    """)
    
    st.write("""
    2. **Assessment of Diagnostic Test Variability**: Bartlett's test can assess the variability in diagnostic test results 
       (e.g., parasite counts) among different laboratories or testing methods.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Bartlett's Test")
    
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
            
            # Ask the user to select the categorical variable for groups
            group_column = st.selectbox("Select the categorical variable", df.columns)
            
            # Ask the user to select numeric variables for variance comparison
            numeric_columns = st.multiselect("Select numeric variables for comparison", df.columns, 
                                              default=df.select_dtypes(include=[np.number]).columns.tolist())
            
            st.write(f"You selected: {group_column} as the grouping variable and {numeric_columns} for comparison.")
            
            # Perform Bartlett's Test
            groups = [df[df[group_column] == group][numeric_columns].values.flatten() for group in df[group_column].unique()]
            stat, p_value = bartlett(*groups)
            
            # Display test results
            st.write("Bartlett's Test Results:")
            st.write(f"Test Statistic: {stat}")
            st.write(f"p-value: {p_value}")
            
            # Interpretation of results
            if p_value < 0.05:
                st.write("The variances are significantly different (Reject H0).")
            else:
                st.write("The variances are equal (Fail to reject H0).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

# App title
st.title("Kruskal-Wallis Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Kruskal-Wallis Test")
    
    st.subheader("When to Use It")
    st.write("""
        The Kruskal-Wallis test is used to determine if there are statistically significant differences 
        between the medians of three or more independent groups. It is a non-parametric alternative to 
        one-way ANOVA and does not assume a normal distribution.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("You need data from at least three independent groups to conduct this test.")
    
    st.subheader("Number of Categorical Variables")
    st.write("One categorical variable is required for grouping, and one continuous variable for measurement.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the Kruskal-Wallis test is to determine if there is a significant difference 
        in the distribution of a continuous variable across different groups defined by a categorical variable.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Effectiveness of Malaria Treatment**: Researchers can use the Kruskal-Wallis test to compare the effectiveness 
       of different malaria treatments (e.g., Treatment A, Treatment B, Treatment C) by measuring the recovery time in 
       days.
    """)
    
    st.write("""
    2. **Comparison of Malaria Incidence Rates by Region**: The test can be used to compare the incidence rates 
       of malaria across different regions (e.g., Region 1, Region 2, Region 3) to see if there are significant differences.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Kruskal-Wallis Test")
    
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
            
            # Ask the user to select the categorical variable for groups and the continuous variable for measurement
            group_var = st.selectbox("Select the categorical variable (grouping)", df.columns)
            measurement_var = st.selectbox("Select the continuous variable (measurement)", df.columns)
            
            st.write(f"You selected: {group_var} for grouping and {measurement_var} for measurement.")
            
            # Perform Kruskal-Wallis Test
            groups = [group[measurement_var].values for name, group in df.groupby(group_var)]
            stat, p_value = stats.kruskal(*groups)
            
            # Display test results
            st.write("Kruskal-Wallis Test Results:")
            st.write(f"Test Statistic: {stat}")
            st.write(f"p-value: {p_value}")
            
            # Interpretation of results
            if p_value < 0.05:
                st.write("There is a significant difference in the medians of the groups (Reject H0).")
            else:
                st.write("There is no significant difference in the medians of the groups (Fail to reject H0).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

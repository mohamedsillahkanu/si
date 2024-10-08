import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats

# App title
st.title("One-Way ANOVA Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: One-Way ANOVA")

    st.subheader("When to Use It")
    st.write("""
        The One-Way ANOVA test is used to determine if there are any statistically significant differences between the means
        of three or more independent groups. It tests whether the factor (grouping variable) has a significant impact
        on the dependent variable.
    """)

    st.subheader("Number of Samples Required")
    st.write("You need at least three independent groups to perform a One-Way ANOVA.")

    st.subheader("Number of Categorical and Numeric Variables")
    st.write("One categorical grouping variable and one numeric dependent variable are required.")

    st.subheader("Purpose of the Test")
    st.write("""
        The One-Way ANOVA test is used to determine whether there are statistically significant differences in means
        between different groups based on one factor.
    """)

    st.subheader("Real-Life Medical Example (Malaria)")
    st.write("""
        One practical example of using the One-Way ANOVA test in malaria research is to compare the mean recovery times 
        of patients who received three different types of antimalarial drugs. 
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: One-Way ANOVA")
    
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
            
            # Ask the user to select the categorical (grouping) and numeric variables
            cat_column = st.selectbox("Select the grouping (categorical) variable", df.columns)
            num_column = st.selectbox("Select the dependent (numeric) variable", df.columns)
            
            st.write(f"You selected: Grouping variable - {cat_column}, Numeric variable - {num_column}")
            
            # Group the data by the selected categorical variable
            grouped_data = [df[df[cat_column] == group][num_column] for group in df[cat_column].unique()]
            
            # Perform One-Way ANOVA
            f_stat, p_value = stats.f_oneway(*grouped_data)
            
            # Display test results
            st.write("One-Way ANOVA Test Results:")
            st.write(f"F-Statistic: {f_stat}")
            st.write(f"p-value: {p_value}")
            
            # Interpretation of results
            if p_value < 0.05:
                st.write("The means of the groups are significantly different (Reject H0).")
            else:
                st.write("The means of the groups are not significantly different (Fail to reject H0).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

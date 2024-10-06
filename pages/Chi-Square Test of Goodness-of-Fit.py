import streamlit as st
import pandas as pd
from scipy.stats import chisquare

# App title
st.title("Chi-Square Test of Goodness-of-Fit")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Chi-Square Test of Goodness-of-Fit")
    
    st.subheader("When to Use It")
    st.write("""
        The Chi-Square Test of Goodness-of-Fit is used to determine if an observed frequency distribution
        matches an expected frequency distribution. It's suitable for categorical data and larger sample sizes.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("Typically, a minimum of 5 samples per category is recommended for reliable results.")
    
    st.subheader("Number of Categorical Variables")
    st.write("The test is applied to a single categorical variable with multiple categories.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the Chi-Square Test of Goodness-of-Fit is to assess whether the observed data distribution
        fits a specific theoretical distribution.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in the field of malaria research:")
    
    st.write("""
    1. **Efficacy of Malaria Treatments**: 
        A study can be conducted to evaluate the efficacy of different treatments for malaria by comparing the 
        observed number of patients responding to each treatment against expected outcomes based on historical data.
    """)
    
    st.write("""
    2. **Insecticide Resistance**: 
        Researchers can use the test to determine if the observed resistance levels in mosquito populations
        fit expected frequencies based on previous studies and environmental factors.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Chi-Square Test of Goodness-of-Fit")
    
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
            
            # Ask user to select the categorical column and expected frequencies
            categorical_column = st.selectbox("Select the categorical column", df.columns)
            st.write(f"You selected: {categorical_column}")
            
            categories = df[categorical_column].unique()
            st.write(f"Unique categories in {categorical_column}: {categories}")
            
            expected_frequencies = []
            for category in categories:
                freq = st.number_input(f"Enter expected frequency for {category}", min_value=0, step=1)
                expected_frequencies.append(freq)
            
            # Calculate observed frequencies
            observed_frequencies = df[categorical_column].value_counts().sort_index().values
            
            # Perform the goodness-of-fit test
            if st.button("Run Test"):
                result = chisquare(f_obs=observed_frequencies, f_exp=expected_frequencies)
                st.write("Test Result:")
                st.write(result)
                
                # Conclusion
                if result.pvalue < 0.05:
                    st.write("The observed distribution does not match the expected distribution (Reject H0).")
                else:
                    st.write("The observed distribution matches the expected distribution (Fail to reject H0).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

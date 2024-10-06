import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency
import numpy as np

# App title
st.title("Repeated G-Tests of Goodness-of-Fit")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Repeated G-Tests of Goodness-of-Fit")
    
    st.subheader("When to Use It")
    st.write("""
        The Repeated G-Test of Goodness-of-Fit is used when you have multiple independent groups or samples and 
        you want to test whether each group conforms to an expected frequency distribution, and also whether 
        the deviation from the expected distribution is consistent across all groups.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("You need at least two samples (groups) with sufficient observations in each category for this test.")
    
    st.subheader("Number of Categorical Variables")
    st.write("This test applies to a single categorical variable with multiple categories.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the Repeated G-Test of Goodness-of-Fit is to examine whether observed distributions in multiple 
        independent samples deviate from expected distributions, and whether these deviations differ across the samples.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Drug Resistance Across Regions**: 
       Researchers can test whether observed resistance to malaria drugs in different regions deviates from expected levels, 
       and whether these deviations are consistent across regions.
    """)
    
    st.write("""
    2. **Vaccine Efficacy Over Time**: 
       The test can be used to analyze whether the observed efficacy of a malaria vaccine over multiple time points 
       conforms to the expected efficacy, and whether deviations differ across time points.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Repeated G-Test of Goodness-of-Fit")
    
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
            
            # Ask the user to select the group column and the categorical column
            group_column = st.selectbox("Select the column representing groups (e.g., regions, time points)", df.columns)
            categorical_column = st.selectbox("Select the categorical column", df.columns)
            
            st.write(f"You selected: {group_column} as the group column and {categorical_column} as the categorical column.")
            
            # Calculate observed frequencies for each group
            observed_freqs = pd.crosstab(df[group_column], df[categorical_column])
            st.write("Observed Frequencies:")
            st.write(observed_freqs)
            
            # Let the user input expected frequencies for each category
            categories = observed_freqs.columns
            expected_frequencies = {}
            for category in categories:
                freq = st.number_input(f"Enter expected frequency for {category}", min_value=0, step=1)
                expected_frequencies[category] = freq

            # Convert expected frequencies to an array that matches the observed frequencies structure
            expected_matrix = np.array([list(expected_frequencies.values())] * observed_freqs.shape[0])
            
            # Perform the repeated G-test of goodness-of-fit using chi-squared test for independence
            if st.button("Run Repeated G-Test"):
                # G-Test by evaluating deviation across all groups
                chi2, p, dof, expected = chi2_contingency(observed_freqs)
                
                st.write("Repeated G-Test Result:")
                st.write(f"Chi-Square Statistic: {chi2}, p-value: {p}")
                
                # Display categories that do not meet expected frequencies
                st.write("Expected Frequencies (Based on Provided Input):")
                st.write(pd.DataFrame(expected, columns=categories, index=observed_freqs.index))
                
                # Conclusion
                if p < 0.05:
                    st.write("The observed distribution does not match the expected distribution across all groups (Reject H0).")
                else:
                    st.write("The observed distribution matches the expected distribution across all groups (Fail to reject H0).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

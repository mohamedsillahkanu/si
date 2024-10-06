import streamlit as st
import pandas as pd
from scipy.stats import chisquare

# App title
st.title("Exact Test for Goodness-of-Fit")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Exact Test for Goodness-of-Fit")
    
    st.subheader("When to Use It")
    st.write("""
        The Exact Test for Goodness-of-Fit is used to determine if an observed categorical distribution matches a theoretical or expected distribution.
        This test is ideal for small sample sizes (e.g., less than 20) where assumptions of other tests, such as the chi-square test, might not hold.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("Typically small (e.g., less than 20 samples). For larger sample sizes, consider using the chi-square goodness-of-fit test.")
    
    st.subheader("Number of Categorical Variables")
    st.write("The test is applied to a single categorical variable with multiple categories.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the Exact Test for Goodness-of-Fit is to determine whether the observed data distribution fits a particular theoretical distribution.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in the field of malaria research:")
    
    st.write("""
    1. **Malaria Diagnostic Test Kit Validation**: 
        Suppose a diagnostic test for malaria gives either 'positive' or 'negative' results. We can use this test to determine whether the observed proportion of positive and negative results matches the expected prevalence of malaria in the population.
    """)
    
    st.write("""
    2. **Antimalarial Drug Resistance**: 
        In regions categorized as 'resistant' or 'susceptible' to antimalarial drugs, this test can help verify if the observed distribution of resistance fits the expected resistance levels based on historical or clinical data.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Exact Goodness-of-Fit Test")
    
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
            st.write(df)
            
            # Ask user to select the observed categorical column and expected frequencies
            categorical_column = st.selectbox("Select the categorical column", df.columns)
            st.write(f"You selected: {categorical_column}")
            
            # User input expected frequencies
            categories = df[categorical_column].unique()
            st.write(f"Unique categories in {categorical_column}: {categories}")
            
            expected_frequencies = []
            for category in categories:
                freq = st.number_input(f"Enter expected frequency for {category}", min_value=0.0, step=0.01)
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

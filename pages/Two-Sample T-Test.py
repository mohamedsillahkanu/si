import streamlit as st
import pandas as pd
from scipy import stats

# App title
st.title("Two-Sample T-Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Two-Sample T-Test")
    
    st.subheader("When to Use It")
    st.write("""
        The two-sample t-test is used to compare the means of two independent groups. This test helps determine 
        whether the means of two populations are different based on sample data.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("You need two independent groups and a numeric variable for each group to conduct the test.")
    
    st.subheader("Number of Categorical and Numeric Variables")
    st.write("One categorical variable to separate the two groups and one numeric variable for comparison.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the test is to determine whether the means of two independent groups are significantly 
        different, which can help in evaluating treatment effects or conditions.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Malaria Treatment Effectiveness**: Compare the mean recovery time between two groups of patients receiving different malaria treatments.
    """)
    
    st.write("""
    2. **Hemoglobin Levels in Malaria Patients**: Compare the mean hemoglobin levels between malaria patients and healthy controls to see if there's a significant difference.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Two-Sample T-Test")
    
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
            
            # Ask the user to select the numeric variable for the t-test
            numeric_column = st.selectbox("Select the numeric variable", df.select_dtypes(include=['float64', 'int64']).columns)
            
            # Ask the user to select the categorical variable to divide the groups
            categorical_column = st.selectbox("Select the categorical variable (Group)", df.select_dtypes(include=['object', 'category']).columns)
            
            # Identify the unique groups within the selected categorical variable
            groups = df[categorical_column].unique()
            
            if len(groups) != 2:
                st.error("Please select a categorical variable with exactly two groups.")
            else:
                # Split the data into two groups
                group1 = df[df[categorical_column] == groups[0]][numeric_column]
                group2 = df[df[categorical_column] == groups[1]][numeric_column]
                
                # Perform two-sample t-test
                t_stat, p_value = stats.ttest_ind(group1, group2, nan_policy='omit')
                
                # Display test results
                st.write(f"Group 1: {groups[0]} (n = {len(group1)})")
                st.write(f"Group 2: {groups[1]} (n = {len(group2)})")
                st.write(f"T-Statistic: {t_stat}")
                st.write(f"P-Value: {p_value}")
                
                # Interpretation of results
                if p_value < 0.05:
                    st.write("There is a statistically significant difference between the means of the two groups (Reject H0).")
                else:
                    st.write("There is no statistically significant difference between the means of the two groups (Fail to reject H0).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

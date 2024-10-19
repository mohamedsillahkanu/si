import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# App title
st.title("Chi-Square Test for Independence")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Chi-Square Test for Independence")
    
    st.subheader("When to Use It")
    st.write("""
        The Chi-Square Test of Independence is used when you have two categorical variables, and you want 
        to determine whether there is a significant association between these variables. The test assesses 
        whether the observed frequencies in a contingency table differ significantly from the expected frequencies.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("This test works well when you have at least 5 observations per category, but it can handle larger contingency tables (not limited to 2x2).")
    
    st.subheader("Number of Categorical Variables")
    st.write("You need two categorical variables for this test. Each variable can have more than two categories.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the Chi-Square Test of Independence is to determine if there is a significant relationship 
        between two categorical variables.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")    
    st.write("""1. **Malaria Symptoms and Diagnostic Results**: Researchers may use the Chi-Square Test to determine if there is a significant association between the type of malaria symptoms (e.g., fever, chills, headaches) and the result of a diagnostic test (positive or negative).""")
    st.write("""2. **Malaria Prevention Methods and Infection Status**: The test can be used to evaluate whether there is an association between the use of malaria prevention methods (e.g., bed nets, repellents) and malaria infection status (infected or not infected).""")

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Chi-Square Test for Independence")
    
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
            
            # Option to use an existing contingency table or create one
            use_existing_table = st.radio("Do you have a contingency table in the file?", ["Yes", "No"])
            
            if use_existing_table == "Yes":
                st.subheader("Select the contingency table")
                table_name = st.selectbox("Select the table", df.columns)
                
                # Assuming the selected column contains the contingency table data
                contingency_table = df[table_name].values.reshape(-1, 2)  # Modify as necessary for the actual structure
                contingency_table = pd.DataFrame(contingency_table)
                st.write("Contingency Table (Observed Frequencies):")
                st.write(contingency_table)
            else:
                # Ask the user to select the two categorical columns for the contingency table
                cat_column1 = st.selectbox("Select the first categorical variable", df.columns)
                cat_column2 = st.selectbox("Select the second categorical variable", df.columns)
                
                st.write(f"You selected: {cat_column1} and {cat_column2} for the test.")
                
                # Generate the contingency table
                contingency_table = pd.crosstab(df[cat_column1], df[cat_column2])
                st.write("Contingency Table (Observed Frequencies):")
                st.write(contingency_table)

            # Perform the Chi-Square Test of Independence
            chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)
            
            st.write("Chi-Square Test Results:")
            st.write(f"Chi-Square Statistic: {chi2_stat}")
            st.write(f"p-value: {p_value}")
            st.write(f"Degrees of Freedom: {dof}")
            
            # Show expected frequencies table
            st.write("Expected Frequencies Table:")
            expected_df = pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns)
            st.write(expected_df)
            
            # Mark significant differences in the contingency table
            significance_mask = expected_df > 5  # Adjust threshold as necessary
            significant_contingency_table = contingency_table.copy()

            # Add asterisks for significant values
            for i in range(contingency_table.shape[0]):
                for j in range(contingency_table.shape[1]):
                    if (expected[i, j] > 5) and (p_value < 0.05):
                        significant_contingency_table.iat[i, j] = str(contingency_table.iat[i, j]) + '*'
            
            st.write("Contingency Table with Significance Indicators:")
            st.write(significant_contingency_table)

            # Interpretation of results
            if p_value < 0.05:
                st.write("The association between the two variables is statistically significant (Reject H0).")
            else:
                st.write("There is no significant association between the two variables (Fail to reject H0).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# Function for G-Test
def g_test(contingency_table):
    obs = contingency_table.values
    row_totals = obs.sum(axis=1, keepdims=True)
    col_totals = obs.sum(axis=0, keepdims=True)
    total = obs.sum()
    expected = row_totals @ col_totals / total
    g_stat = 2 * np.sum(obs * np.log(obs / expected))
    dof = (obs.shape[0] - 1) * (obs.shape[1] - 1)
    return g_stat, dof, expected

# App title
st.title("G-Test for Independence")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: G-Test for Independence")
    
    st.subheader("When to Use It")
    st.write("""
        The G-Test of Independence is used when you have two categorical variables, and you want to determine 
        whether there is a significant association between these variables, similar to the Chi-Square Test of Independence.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("This test works well with large samples and is used primarily for contingency tables.")
    
    st.subheader("Number of Categorical Variables")
    st.write("You need two categorical variables for this test. Each variable can have more than two categories.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the G-Test of Independence is to determine if there is a significant relationship between two categorical variables.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Malaria Symptoms and Diagnostic Results**: 
       Researchers may use the G-Test to determine if there is a significant association between the type of malaria symptoms 
       (e.g., fever, chills, headaches) and the result of a diagnostic test (positive or negative).
    """)
    
    st.write("""
    2. **Malaria Prevention Methods and Infection Status**: 
       The test can be used to evaluate whether there is an association between the use of malaria prevention methods (e.g., bed nets, 
       repellents) and malaria infection status (infected or not infected).
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: G-Test for Independence")
    
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
            
            # Ask the user to select the two categorical columns for the contingency table
            cat_column1 = st.selectbox("Select the first categorical variable", df.columns)
            cat_column2 = st.selectbox("Select the second categorical variable", df.columns)
            
            st.write(f"You selected: {cat_column1} and {cat_column2} for the test.")
            
            # Generate the contingency table
            contingency_table = pd.crosstab(df[cat_column1], df[cat_column2])
            st.write("Contingency Table (Observed Frequencies):")
            st.write(contingency_table)
            
            # Perform the G-Test of Independence
            g_stat, dof, expected = g_test(contingency_table)
            
            st.write("G-Test Results:")
            st.write(f"G-Statistic: {g_stat}")
            st.write(f"Degrees of Freedom: {dof}")
            
            # Show expected frequencies table
            st.write("Expected Frequencies Table:")
            st.write(pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns))
            
            # Interpretation of results
            if g_stat > chi2_contingency(contingency_table)[0]:  # Compare with chi-square value
                st.write("The association between the two variables is statistically significant (Reject H0).")
            else:
                st.write("There is no significant association between the two variables (Fail to reject H0).")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2

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

# Function to calculate p-value
def calculate_p_value(g_stat, dof):
    return 1 - chi2.cdf(g_stat, dof)

# Streamlit app code
st.title("G-Test for Independence")

# Upload dataset
uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        
        st.write("Here is a preview of your data:")
        st.write(df.head())
        
        # Select columns for the G-Test
        cat_column1 = st.selectbox("Select the first categorical variable", df.columns)
        cat_column2 = st.selectbox("Select the second categorical variable", df.columns)
        
        st.write(f"You selected: {cat_column1} and {cat_column2} for the test.")
        
        # Create the contingency table
        contingency_table = pd.crosstab(df[cat_column1], df[cat_column2])
        st.write("Contingency Table (Observed Frequencies):")
        st.write(contingency_table)
        
        # Perform the G-Test
        g_stat, dof, expected = g_test(contingency_table)
        
        st.write("G-Test Results:")
        st.write(f"G-Statistic: {g_stat}")
        st.write(f"Degrees of Freedom: {dof}")
        
        # Calculate p-value
        p_value = calculate_p_value(g_stat, dof)
        st.write(f"P-Value: {p_value}")
        
        # Show expected frequencies table
        st.write("Expected Frequencies Table:")
        st.write(pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns))
        
        # Interpretation of results
        if p_value < 0.05:
            st.write("The association between the two variables is statistically significant (Reject H0).")
        else:
            st.write("There is no significant association between the two variables (Fail to reject H0).")
    
    except Exception as e:
        st.error(f"Error loading file: {e}")

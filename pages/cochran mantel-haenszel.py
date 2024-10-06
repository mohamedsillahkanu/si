import streamlit as st
import pandas as pd
from statsmodels.stats.contingency_tables import stratified_tables

# Cochran-Mantel-Haenszel Test Function
def cmh_test(data, stratifying_col, cat_col1, cat_col2):
    # Create a list of contingency tables stratified by the `stratifying_col`
    stratified_data = data.groupby(stratifying_col).apply(lambda x: pd.crosstab(x[cat_col1], x[cat_col2]))
    
    # CMH test using statsmodels
    cmh_result = stratified_tables(stratified_data).test_null_odds()
    
    return cmh_result

# Streamlit app
st.title("Cochran-Mantel-Haenszel (CMH) Test")

# Upload dataset
uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Read the file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        
        st.write("Here is a preview of your data:")
        st.write(df.head())
        
        # Select columns for the CMH test
        stratifying_col = st.selectbox("Select the stratifying variable (e.g., hospital or group)", df.columns)
        cat_col1 = st.selectbox("Select the first categorical variable (e.g., treatment)", df.columns)
        cat_col2 = st.selectbox("Select the second categorical variable (e.g., outcome)", df.columns)
        
        st.write(f"You selected: {stratifying_col}, {cat_col1}, and {cat_col2} for the test.")
        
        # Perform the CMH test
        cmh_result = cmh_test(df, stratifying_col, cat_col1, cat_col2)
        
        st.write("CMH Test Results:")
        st.write(f"CMH Statistic: {cmh_result.statistic}")
        st.write(f"P-Value: {cmh_result.pvalue}")
        
        # Interpretation
        if cmh_result.pvalue < 0.05:
            st.write("There is a significant association after controlling for the stratifying variable.")
        else:
            st.write("There is no significant association after controlling for the stratifying variable.")
    
    except Exception as e:
        st.error(f"Error loading file: {e}")


import streamlit as st
import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Streamlit app layout
st.title("Tukey-Kramer Test")

# File upload
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read the uploaded file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # Display the dataframe
    st.write("Here is a preview of your dataset:")
    st.write(df.head())

    # Column selection for the test
    numeric_col = st.selectbox("Select the numeric column (Outcome Measure)", df.select_dtypes(include=['number']).columns)
    categorical_col = st.selectbox("Select the categorical column (Group Variable)", df.select_dtypes(include=['object', 'category']).columns)

    if st.button("Run Tukey-Kramer Test"):
        # Perform Tukey-Kramer Test
        tukey_result = pairwise_tukeyhsd(endog=df[numeric_col], groups=df[categorical_col], alpha=0.05)

        # Convert result to DataFrame
        tukey_summary = pd.DataFrame(data=tukey_result.summary().data[1:], columns=tukey_result.summary().data[0])

        # Display results in table form
        st.write("Tukey-Kramer Test Results")
        st.dataframe(tukey_summary)

        # Provide an option to download the results as an Excel file
        output_file = "tukey_kramer_test_results.xlsx"
        tukey_summary.to_excel(output_file, index=False)

        with open(output_file, "rb") as file:
            st.download_button(label="Download Results as Excel", data=file, file_name=output_file)

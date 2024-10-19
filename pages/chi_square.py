import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# App title
st.title("Chi-Square Test for Independence")

# Step 1: Upload the Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Load the dataset
    df = pd.read_excel(uploaded_file, sheet_name=0)

    # Step 2: Select one categorical variable
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    selected_categorical = st.selectbox("Select one categorical variable", categorical_columns)

    # Step 3: Select multiple numeric variables
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    selected_numeric = st.multiselect("Select one or more numeric variables", numeric_columns)

    if st.button("Generate Contingency Table and Chi-Square Test"):
        if selected_categorical and selected_numeric:
            # Step 4: Create a contingency table
            contingency_table = pd.DataFrame()

            for num_col in selected_numeric:
                # Group by the categorical variable and sum the numeric variable
                temp_table = df.groupby(selected_categorical)[num_col].sum().reset_index()
                temp_table.rename(columns={num_col: 'Total'}, inplace=True)
                temp_table[selected_categorical] = temp_table[selected_categorical].astype(str)
                contingency_table = pd.concat([contingency_table, temp_table.set_index(selected_categorical)], axis=1)

            # Step 5: Perform Chi-Square Test
            # Ensure that the contingency table is in the correct format
            contingency_table.fillna(0, inplace=True)  # Replace NaNs with 0 for Chi-Square test
            chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

            # Step 6: Display results
            st.write("Contingency Table:")
            st.write(contingency_table)

            st.write("Chi-Square Test Results:")
            st.write(f"Chi-Square Statistic: {chi2_stat}")
            st.write(f"p-value: {p_value}")
            st.write(f"Degrees of Freedom: {dof}")

            # Show expected frequencies
            expected_df = pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns)
            st.write("Expected Frequencies Table:")
            st.write(expected_df)

            # Interpretation of results
            if p_value < 0.05:
                st.write("The association between the categorical variable and numeric variables is statistically significant (Reject H0).")
            else:
                st.write("There is no significant association between the categorical variable and numeric variables (Fail to reject H0).")
        else:
            st.error("Please select a categorical variable and at least one numeric variable.")

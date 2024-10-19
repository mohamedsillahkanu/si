import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# App title
st.title("Chi-Square Test for Independence with Aggregation")

# Step 1: Upload the Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Load the dataset
    df = pd.read_excel(uploaded_file, sheet_name=0)

    # Step 2: Select categorical and numeric variables
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    # User selects categorical variables
    selected_categorical = st.multiselect("Select one or more categorical variables", categorical_columns)

    # User selects numeric variables
    selected_numeric = st.multiselect("Select one or more numeric variables", numeric_columns)

    if st.button("Generate Aggregated Table"):
        if selected_categorical and selected_numeric:
            # Step 3: Perform row-wise aggregation
            aggregated_df = df[selected_categorical + selected_numeric].groupby(selected_categorical).agg(
                count=('District', 'size'), 
                total=sum
            ).reset_index()

            # Calculate percentage
            aggregated_df['percentage'] = (aggregated_df['total'] / aggregated_df['total'].sum()) * 100

            # Format the count and percentage in brackets
            aggregated_df['count (percentage)'] = aggregated_df.apply(lambda x: f"{x['count']} ({x['percentage']:.1f}%)", axis=1)

            st.write("Aggregated Table:")
            st.write(aggregated_df)

            # Step 4: Prepare data for Chi-Square Test
            contingency_table = pd.crosstab(index=aggregated_df[selected_categorical[0]], columns=aggregated_df[selected_numeric[0]])

            # Perform Chi-Square Test
            chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

            # Step 5: Display Chi-Square test results
            st.write("Chi-Square Test Results:")
            st.write(f"Chi-Square Statistic: {chi2_stat}")
            st.write(f"p-value: {p_value}")
            st.write(f"Degrees of Freedom: {dof}")

            # Show expected frequencies
            st.write("Expected Frequencies Table:")
            expected_df = pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns)
            st.write(expected_df)

            # Interpretation of results
            if p_value < 0.05:
                st.write("The association between the two variables is statistically significant (Reject H0).")
            else:
                st.write("There is no significant association between the two variables (Fail to reject H0).")

        else:
            st.error("Please select at least one categorical variable and one numeric variable.")

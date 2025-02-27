import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# App title
st.title("Chi-Square Test for Independence with Percentages")

# Step 1: Upload the Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Load the dataset
    df = pd.read_excel(uploaded_file, sheet_name=0)

    # Step 2: Select one categorical variable
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    selected_categorical = st.selectbox("Select one categorical variable", categorical_columns)

    # Step 3: Select two numeric variables
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    selected_numeric = st.multiselect("Select two numeric variables", numeric_columns, max_selections=2)

    if st.button("Calculate Percentages and Perform Chi-Square Test"):
        if selected_categorical and len(selected_numeric) == 2:
            # Step 4: Calculate row-wise sums
            df['Total'] = df[selected_numeric[0]] + df[selected_numeric[1]]

            # Step 5: Calculate row-wise percentages
            df['Percentage_Numeric_1'] = (df[selected_numeric[0]] / df['Total']) * 100
            df['Percentage_Numeric_2'] = (df[selected_numeric[1]] / df['Total']) * 100

            # Prepare a contingency table
            contingency_table = df.groupby(selected_categorical)[['Percentage_Numeric_1', 'Percentage_Numeric_2']].mean().reset_index()

            # Display the contingency table with variable names
            contingency_table.columns = [selected_categorical] + [f"{selected_numeric[0]} (%)", f"{selected_numeric[1]} (%)"]
            st.write("Contingency Table with Row-wise Percentages:")
            st.write(contingency_table)

            # Step 6: Perform Chi-Square Test
            chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table[[f"{selected_numeric[0]} (%)", f"{selected_numeric[1]} (%)"]])

            # Step 7: Display Chi-Square test results
            st.write("Chi-Square Test Results:")
            st.write(f"Chi-Square Statistic: {chi2_stat}")
            st.write(f"p-value: {p_value}")
            st.write(f"Degrees of Freedom: {dof}")

            # Show expected frequencies
            expected_df = pd.DataFrame(expected, index=contingency_table[selected_categorical], columns=['Expected ' + f"{selected_numeric[0]} (%)", 'Expected ' + f"{selected_numeric[1]} (%)"])
            st.write("Expected Frequencies Table:")
            st.write(expected_df)

            # Interpretation of results
            if p_value < 0.05:
                st.write("The association between the categorical variable and numeric variables is statistically significant (Reject H0).")
            else:
                st.write("There is no significant association between the categorical variable and numeric variables (Fail to reject H0).")

            # Marking significant values with an asterisk (*)
            significant_table = contingency_table.copy()
            for i in range(len(contingency_table)):
                if (expected[i][0] > 5 and expected[i][1] > 5):  # Ensure valid conditions for significance
                    if p_value < 0.05:
                        significant_table.iloc[i, 1] = str(round(contingency_table.iloc[i, 1], 2)) + '*'
                        significant_table.iloc[i, 2] = str(round(contingency_table.iloc[i, 2], 2)) + '*'

            st.write("Contingency Table with Significance Indicators:")
            st.write(significant_table)

        else:
            st.error("Please select one categorical variable and exactly two numeric variables.")

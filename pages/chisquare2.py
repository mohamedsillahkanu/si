import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# App title
st.title("Chi-Square Test for Independence with Row-wise Analysis")

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

            # Rename columns for clarity
            contingency_table.columns = [selected_categorical] + [f"{selected_numeric[0]} (%)", f"{selected_numeric[1]} (%)"]
            st.write("Contingency Table with Row-wise Percentages:")
            st.write(contingency_table)

            # Initialize a column to mark significance
            contingency_table['Significance'] = ''

            # Step 6: Perform Chi-Square Test for each category
            for i in range(len(contingency_table)):
                row_data = contingency_table.iloc[i][[f"{selected_numeric[0]} (%)", f"{selected_numeric[1]} (%)"]].values
                chi2_stat, p_value, dof = chi2_contingency([row_data, [1, 1]])  # Test against a uniform distribution

                # Mark significant results
                if p_value < 0.05:
                    contingency_table.at[i, 'Significance'] = '*'  # Add asterisk for statistical significance

            st.write("Contingency Table with Significance Indicators:")
            st.write(contingency_table)

            # Interpretation of results
            if any(contingency_table['Significance'] == '*'):
                st.write("There are statistically significant differences between the two numeric variables in some categories.")
            else:
                st.write("There are no statistically significant differences between the two numeric variables.")

        else:
            st.error("Please select one categorical variable and exactly two numeric variables.")

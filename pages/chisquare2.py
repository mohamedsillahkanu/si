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

            # Prepare a contingency table with counts
            contingency_table = df.groupby(selected_categorical)[[selected_numeric[0], selected_numeric[1]]].sum().reset_index()

            # Rename columns for clarity
            contingency_table.columns = [selected_categorical] + [f"{selected_numeric[0]} (Total)", f"{selected_numeric[1]} (Total)"]
            st.write("Contingency Table with Total Counts:")
            st.write(contingency_table)

            # Step 6: Perform Chi-Square Test for each category
            significance_results = []

            for index, row in contingency_table.iterrows():
                # Extract the observed counts for Chi-Square test
                observed_counts = np.array([row[f"{selected_numeric[0]} (Total)"], row[f"{selected_numeric[1]} (Total)"]])

                # Perform Chi-Square test only if both counts are greater than 0
                if np.all(observed_counts > 0):
                    chi2_stat, p_value, dof = chi2_contingency([observed_counts])  # Only one row of observed data

                    # Mark significance
                    significance_results.append('*' if p_value < 0.05 else '')
                else:
                    significance_results.append('')  # No significance if counts are zero or less

            # Add significance results to the contingency table
            contingency_table['Significance'] = significance_results

            # Display the contingency table with significance indicators
            st.write("Contingency Table with Significance Indicators:")
            st.write(contingency_table)

            # Interpretation of results
            if any(significance_results):
                st.write("There are statistically significant differences between the two numeric variables in some categories.")
            else:
                st.write("There are no statistically significant differences between the two numeric variables.")
        else:
            st.error("Please select one categorical variable and exactly two numeric variables.")

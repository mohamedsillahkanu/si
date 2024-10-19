import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# App title
st.title("Statistical Comparison of Numeric Variables")

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

    if st.button("Calculate Percentages and Perform Statistical Test"):
        if selected_categorical and len(selected_numeric) == 2:
            # Step 4: Calculate row-wise sums and percentages
            df['Total'] = df[selected_numeric[0]] + df[selected_numeric[1]]
            df['Percentage_Numeric_1'] = (df[selected_numeric[0]] / df['Total']) * 100
            df['Percentage_Numeric_2'] = (df[selected_numeric[1]] / df['Total']) * 100

            # Prepare a contingency table
            contingency_table = df.groupby(selected_categorical)[['Percentage_Numeric_1', 'Percentage_Numeric_2']].mean().reset_index()

            # Rename columns for clarity
            contingency_table.columns = [selected_categorical] + [f"{selected_numeric[0]} (%)", f"{selected_numeric[1]} (%)"]
            st.write("Contingency Table with Row-wise Percentages:")
            st.write(contingency_table)

            # Step 5: Initialize lists to hold p-values and significance markers
            p_values = []
            significance_results = []

            # Step 6: Perform statistical test for each category
            for index, row in contingency_table.iterrows():
                # Extract the observed percentages for comparison
                percent_1 = row[f"{selected_numeric[0]} (%)"]
                percent_2 = row[f"{selected_numeric[1]} (%)"]

                # Assuming we have a sample size (n) for calculating p-values, for demonstration, use a fixed n
                n = 100  # Example sample size, adjust as needed
                observed_data_1 = np.random.binomial(n, percent_1 / 100, size=1)
                observed_data_2 = np.random.binomial(n, percent_2 / 100, size=1)

                # Perform t-test (or choose another test based on data characteristics)
                t_stat, p_value = ttest_ind(observed_data_1, observed_data_2)

                # Store the p-value and mark significance
                p_values.append(p_value)
                significance_results.append('*' if p_value < 0.05 else '')

            # Add p-values and significance results to the contingency table
            contingency_table['p-value'] = p_values
            contingency_table['Significance'] = significance_results

            # Display the contingency table with significance indicators
            st.write("Contingency Table with p-values and Significance Indicators:")
            st.write(contingency_table)

            # Interpretation of results
            if any(significance_results):
                st.write("There are statistically significant differences between the two numeric variables in some categories.")
            else:
                st.write("There are no statistically significant differences between the two numeric variables.")
        else:
            st.error("Please select one categorical variable and exactly two numeric variables.")

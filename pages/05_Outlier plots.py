import streamlit as st
from io import BytesIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to detect outliers using Scatterplot with Q1 and Q3 lines
def detect_outliers_scatterplot(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return lower_bound, upper_bound

# Function to apply winsorization to a column
def winsorize_series(series, lower_bound, upper_bound):
    return series.clip(lower=lower_bound, upper=upper_bound)

# Function to process a single column using Winsorization
def process_column_winsorization(df, column):
    grouped = df.groupby(['hf_uid', 'year'])

    results = []
    for (hf_uid, year), group in grouped:
        lower_bound, upper_bound = detect_outliers_scatterplot(group, column)

        group[f'{column}_lower_bound'] = lower_bound
        group[f'{column}_upper_bound'] = upper_bound
        group[f'{column}_category'] = np.where(
            (group[column] < lower_bound) | (group[column] > upper_bound), 'Outlier', 'Non-Outlier'
        )

        # Apply winsorization
        group[f'{column}_winsorized'] = winsorize_series(group[column], lower_bound, upper_bound)

        results.append(group)

    final_df = pd.concat(results)

    return final_df

# Function to generate subplot for original and winsorized data
def generate_subplot(df, column, hf_uid, year):
    filtered_df = df[(df['hf_uid'] == hf_uid) & (df['year'] == year)]

    if filtered_df.empty:
        st.write("No data to preview.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=True)

    # Original column scatter plot
    axes[0].scatter(
        filtered_df.index,
        filtered_df[column],
        c=np.where(
            (filtered_df[column] < filtered_df[f'{column}_lower_bound']) |
            (filtered_df[column] > filtered_df[f'{column}_upper_bound']),
            'red',
            'blue'
        ),
        alpha=0.7
    )
    axes[0].set_title(f'Original {column}')
    axes[0].set_xlabel('Index')
    axes[0].set_ylabel(column)

    # Winsorized column scatter plot
    for idx, row in filtered_df.iterrows():
        if row[column] != row[f'{column}_winsorized']:
            axes[1].scatter(idx, row[f'{column}_winsorized'], c='green', alpha=0.7, label='Corrected Value')

    axes[1].scatter(
        filtered_df.index,
        filtered_df[f'{column}_winsorized'],
        c='blue',
        alpha=0.7
    )
    axes[1].set_title(f'Winsorized {column}')
    axes[1].set_xlabel('Index')

    handles, labels = axes[1].get_legend_handles_labels()
    if 'Corrected Value' not in labels:
        axes[1].legend().remove()

    st.pyplot(fig)

# Streamlit app setup
st.title("Outlier Detection, Winsorization, and Visualization")

uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel):", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    if df.empty:
        st.write("No data to preview.")
    else:
        st.write("### Preview of the uploaded dataset:")
        st.write(df.head())

        columns_to_process = ['allout', 'susp', 'test', 'conf', 'maltreat', 'pres', 'maladm', 'maldth']

        processed_dfs = []

        for column in columns_to_process:
            processed_df = process_column_winsorization(df, column)
            processed_dfs.append(processed_df)

        final_combined_df = pd.concat(processed_dfs, axis=0)

        st.write("### Processed Data:")
        st.write(final_combined_df.head())

        # Allow user to select hf_uid and year for visualization
        unique_hf_uids = final_combined_df['hf_uid'].unique()
        unique_years = final_combined_df['year'].unique()

        selected_hf_uid = st.selectbox("Select hf_uid:", unique_hf_uids)
        selected_year = st.selectbox("Select year:", unique_years)

        selected_column = st.selectbox("Select column to visualize:", columns_to_process)

        if st.button("Generate Subplots"):
            generate_subplot(final_combined_df, selected_column, selected_hf_uid, selected_year)

        # Export combined DataFrame
        combined_buffer = BytesIO()
        final_combined_df.to_csv(combined_buffer, index=False)
        st.download_button(
            label="Download Processed Data",
            data=combined_buffer.getvalue(),
            file_name="processed_data.csv",
            mime="text/csv"
        )

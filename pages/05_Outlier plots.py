import streamlit as st
from io import BytesIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to detect outliers using IQR method
def detect_outliers_iqr(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return lower_bound, upper_bound

# Function to generate scatter plot for original and winsorized columns
def generate_scatter_plot(df, column, hf_uid, year):
    # Filter the data for the selected hf_uid and year
    filtered_df = df[(df['hf_uid'] == hf_uid) & (df['year'] == year)]

    if filtered_df.empty:
        st.write("No data to preview.")
        return

    # Calculate outlier bounds for the original column
    original_lower, original_upper = detect_outliers_iqr(filtered_df[column])

    # Calculate outlier bounds for the winsorized column
    winsorized_lower, winsorized_upper = detect_outliers_iqr(filtered_df[f'{column}_winsorized'])

    # Create scatter plot
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=True)

    # Scatter plot for the original column
    axes[0].scatter(
        filtered_df['month'],
        filtered_df[column],
        c=np.where(
            (filtered_df[column] < original_lower) | (filtered_df[column] > original_upper),
            'red',
            'blue'
        ),
        alpha=0.7
    )
    axes[0].axhline(original_lower, color='green', linestyle='--', label='Lower Bound (Original)')
    axes[0].axhline(original_upper, color='red', linestyle='--', label='Upper Bound (Original)')
    axes[0].set_title(f'Original {column}')
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel(column)
    axes[0].legend()

    # Scatter plot for the winsorized column
    axes[1].scatter(
        filtered_df['month'],
        filtered_df[f'{column}_winsorized'],
        c=np.where(
            (filtered_df[f'{column}_winsorized'] < winsorized_lower) |
            (filtered_df[f'{column}_winsorized'] > winsorized_upper),
            'red',
            'blue'
        ),
        alpha=0.7
    )
    axes[1].axhline(winsorized_lower, color='green', linestyle='--', label='Lower Bound (Winsorized)')
    axes[1].axhline(winsorized_upper, color='red', linestyle='--', label='Upper Bound (Winsorized)')
    axes[1].set_title(f'Winsorized {column}')
    axes[1].set_xlabel('Month')
    axes[1].legend()

    st.pyplot(fig)

# Streamlit app setup
st.title("Scatter Plot for Original and Winsorized Columns")

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

        # Allow user to select hf_uid, year, and column for visualization
        unique_hf_uids = df['hf_uid'].unique()
        unique_years = df['year'].unique()

        selected_hf_uid = st.selectbox("Select hf_uid:", unique_hf_uids)
        selected_year = st.selectbox("Select year:", unique_years)

        # Assume the dataset contains original columns and their corresponding winsorized columns
        numeric_columns = [col for col in df.columns if col.endswith('_winsorized')]
        original_columns = [col.replace('_winsorized', '') for col in numeric_columns]
        column_mapping = dict(zip(original_columns, numeric_columns))

        selected_column = st.selectbox("Select column to visualize:", original_columns)

        if st.button("Generate Scatter Plot"):
            generate_scatter_plot(df, selected_column, selected_hf_uid, selected_year)

import streamlit as st
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to generate strip plot for original and winsorized columns
def generate_strip_plot(df, column, hf_uid, year):
    # Filter the data for the selected hf_uid and year
    filtered_df = df[(df['hf_uid'] == hf_uid) & (df['year'] == year)]

    if filtered_df.empty:
        st.write("No data to preview.")
        return

    # Check if the winsorized column exists
    winsorized_column = f'{column}_winsorized'
    if winsorized_column not in filtered_df.columns:
        st.write(f"The winsorized column '{winsorized_column}' does not exist in the dataset.")
        return

    # Create strip plots for the selected column and its winsorized counterpart
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=True)

    # Add title
    fig.suptitle("Outlier Detection and Correction Using Strip Plots", fontsize=16)

    # Strip plot for the original column
    sns.stripplot(ax=axes[0], data=filtered_df, y=column, color="blue", alpha=0.7)
    axes[0].set_title(f"Strip Plot for {column} (Original)")
    axes[0].set_ylabel(column)
    axes[0].tick_params(axis='y', which='both', labelsize=10)

    # Strip plot for the winsorized column
    sns.stripplot(ax=axes[1], data=filtered_df, y=winsorized_column, color="green", alpha=0.7)
    axes[1].set_title(f"Strip Plot for {winsorized_column} (Winsorized)")
    axes[1].set_ylabel(column)
    axes[1].tick_params(axis='y', which='both', labelsize=10)

    plt.tight_layout()
    st.pyplot(fig)

# Streamlit app setup
st.title("Strip Plot for Original and Winsorized Columns")

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

        if st.button("Generate Strip Plot"):
            generate_strip_plot(df, selected_column, selected_hf_uid, selected_year)

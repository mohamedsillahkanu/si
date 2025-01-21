import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import iqr
from io import BytesIO

# Helper functions
def detect_outliers_scatterplot(series, threshold=1.5):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    return lower_bound, upper_bound

def calculate_moving_avg(series, window):
    filled_series = series.fillna(method='bfill').fillna(method='ffill')
    moving_avg = filled_series.rolling(window=window, min_periods=1).mean()
    return moving_avg.where(series.notna(), np.nan)

def calculate_moving_avg_excluding_outliers(series, window, threshold=1.5):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR

    clean_series = series[(series >= lower_bound) & (series <= upper_bound)]
    filled_series = clean_series.fillna(method='bfill').fillna(method='ffill')
    moving_avg = filled_series.rolling(window=window, min_periods=1).mean()
    return moving_avg.where(series.notna(), np.nan)

def winsorize_series(series, threshold=1.5):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    return series.clip(lower=lower_bound, upper=upper_bound)

def process_group(group, columns, threshold=1.5, window=3):
    for column in columns:
        lower_bound, upper_bound = detect_outliers_scatterplot(group[column], threshold)
        group[f"{column}_lower_bound"] = lower_bound
        group[f"{column}_upper_bound"] = upper_bound

        group[f"{column}_category"] = np.where(
            (group[column] < lower_bound) | (group[column] > upper_bound),
            "Outlier", "Non-Outlier"
        )

        non_outliers = group[column][(group[column] >= lower_bound) & (group[column] <= upper_bound)]

        group[f"{column}_corrected_mean_include"] = np.where(
            group[f"{column}_category"] == "Outlier", group[column].mean(), group[column]
        )
        group[f"{column}_corrected_mean_exclude"] = np.where(
            group[f"{column}_category"] == "Outlier", non_outliers.mean(), group[column]
        )
        group[f"{column}_corrected_median_include"] = np.where(
            group[f"{column}_category"] == "Outlier", group[column].median(), group[column]
        )
        group[f"{column}_corrected_median_exclude"] = np.where(
            group[f"{column}_category"] == "Outlier", non_outliers.median(), group[column]
        )
        group[f"{column}_corrected_moving_avg_include"] = calculate_moving_avg(group[column], window)
        group[f"{column}_corrected_moving_avg_exclude"] = calculate_moving_avg_excluding_outliers(group[column], window, threshold)
        group[f"{column}_corrected_winsorized"] = winsorize_series(group[column], threshold)

    return group

@st.cache_data
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output

# Streamlit app
st.title("Outlier Detection and Correction Tool")

uploaded_file = st.file_uploader("Upload your dataset (CSV, XLSX, or XLS):", type=["csv", "xlsx", "xls"])
if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]
    if file_type == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("### Dataset Preview")
    st.dataframe(df.head())

    # Allow user to select columns to process
    columns_to_process = st.multiselect(
        "Select columns to process:", options=df.columns, default=df.columns[0] if len(df.columns) > 0 else None
    )

    # Configure outlier detection threshold and window size
    if columns_to_process:
        threshold = st.slider(
            "Select threshold for outlier detection (IQR multiplier):", min_value=1.0, max_value=3.0, step=0.1, value=1.5
        )

        window = st.slider(
            "Select window size for moving average:", min_value=2, max_value=10, step=1, value=3
        )

        # Add button to apply all methods
        if st.button("Apply All Methods"):
            with st.spinner("Processing data..."):
                grouped_df = df.groupby(['hf_uid', 'year'])
                df = grouped_df.apply(lambda group: process_group(group, columns_to_process, threshold, window)).reset_index(drop=True)

            st.success("All methods applied successfully!")

            # Display processed data
            st.write("### Processed Data Preview")
            st.dataframe(df.head())

            # Prepare data for download
            processed_data = convert_df_to_excel(df)

            # Add download button
            st.download_button(
                label="Download Processed Data",
                data=processed_data,
                file_name="processed_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

else:
    st.info("Please upload a dataset to begin.")

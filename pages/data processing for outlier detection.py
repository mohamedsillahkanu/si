import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import iqr

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

def process_column(df, column, threshold=1.5, window=3):
    lower_bound, upper_bound = detect_outliers_scatterplot(df[column], threshold)
    df[f"{column}_lower_bound"] = lower_bound
    df[f"{column}_upper_bound"] = upper_bound

    df[f"{column}_category"] = np.where(
        (df[column] < lower_bound) | (df[column] > upper_bound),
        "Outlier", "Non-Outlier"
    )

    non_outliers = df[column][(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    df[f"{column}_corrected_mean_include"] = np.where(
        df[f"{column}_category"] == "Outlier", df[column].mean(), df[column]
    )
    df[f"{column}_corrected_mean_exclude"] = np.where(
        df[f"{column}_category"] == "Outlier", non_outliers.mean(), df[column]
    )
    df[f"{column}_corrected_median_include"] = np.where(
        df[f"{column}_category"] == "Outlier", df[column].median(), df[column]
    )
    df[f"{column}_corrected_median_exclude"] = np.where(
        df[f"{column}_category"] == "Outlier", non_outliers.median(), df[column]
    )
    df[f"{column}_corrected_moving_avg_include"] = calculate_moving_avg(df[column], window)
    df[f"{column}_corrected_moving_avg_exclude"] = calculate_moving_avg_excluding_outliers(df[column], window, threshold)
    df[f"{column}_corrected_winsorized"] = winsorize_series(df[column], threshold)

    return df

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

    columns_to_process = st.multiselect(
        "Select columns to process:", options=df.columns, default=df.columns[0] if len(df.columns) > 0 else None
    )

    if columns_to_process:
        threshold = st.slider(
            "Select threshold for outlier detection (IQR multiplier):", min_value=1.0, max_value=3.0, step=0.1, value=1.5
        )

        window = st.slider(
            "Select window size for moving average:", min_value=2, max_value=6, step=1, value=3
        )

        methods = st.multiselect(
            "Select correction methods:",
            options=[
                "Mean (Include Outliers)", 
                "Mean (Exclude Outliers)", 
                "Median (Include Outliers)", 
                "Median (Exclude Outliers)",
                "Moving Average (Include Outliers)",
                "Moving Average (Exclude Outliers)",
                "Winsorization"
            ]
        )

        process_button = st.button("Process Selected Columns")

        if process_button:
            with st.spinner("Processing data..."):
                for column in columns_to_process:
                    df = process_column(df, column, threshold, window)

            st.success("Processing complete!")
            st.write("### Processed Data Preview")
            st.dataframe(df.head())

            @st.cache_data
            def convert_df_to_excel(df):
                return df.to_excel(index=False, engine='openpyxl')

            processed_data = convert_df_to_excel(df)

            st.download_button(
                label="Download Processed Data",
                data=processed_data,
                file_name="clean_routine_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

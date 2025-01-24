import streamlit as st
from io import BytesIO
import pandas as pd
import numpy as np

# Function to detect outliers using Scatterplot with Q1 and Q3 lines
def detect_outliers_scatterplot(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return lower_bound, upper_bound

# Function to calculate moving average
def calculate_moving_avg(series, window):
    ma = series.rolling(window=window, min_periods=1).mean()
    return ma.combine_first(series)

# Improved function to calculate moving average excluding outliers
def calculate_moving_avg_excluding_outliers(series, window, threshold=1.5):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - threshold * iqr
    upper_bound = q3 + threshold * iqr

    non_outlier_mask = (series >= lower_bound) & (series <= upper_bound)
    clean_series = series.where(non_outlier_mask)
    ma = clean_series.rolling(window=window, min_periods=1).mean()
    return ma.combine_first(series)

# Function to process and export the results for a single column
def process_column(df, column):
    grouped = df.groupby(['adm1', 'adm2', 'adm3', 'hf_uid', 'year'])

    results = []
    for (adm1, adm2, adm3, hf_uid, year), group in grouped:
        lower_bound, upper_bound = detect_outliers_scatterplot(group, column)

        group[f'{column}_lower_bound'] = lower_bound
        group[f'{column}_upper_bound'] = upper_bound
        group[f'{column}_category'] = np.where(
            (group[column] < lower_bound) | (group[column] > upper_bound), 'Outlier', 'Non-Outlier'
        )

        mean_include_outliers = group[column].mean()
        mean_exclude_outliers = group[(group[column] >= lower_bound) & (group[column] <= upper_bound)][column].mean()
        median_include_outliers = group[column].median()
        median_exclude_outliers = group[(group[column] >= lower_bound) & (group[column] <= upper_bound)][column].median()
        moving_avg_include_outliers = calculate_moving_avg(group[column], window=3)
        moving_avg_exclude_outliers = calculate_moving_avg_excluding_outliers(group[column], window=3)
        winsorised = group[column].clip(lower=lower_bound, upper=upper_bound)

        group[f'{column}_corrected_mean_include'] = group[column].where(group[f'{column}_category'] == 'Non-Outlier', mean_include_outliers)
        group[f'{column}_corrected_mean_exclude'] = group[column].where(group[f'{column}_category'] == 'Non-Outlier', mean_exclude_outliers)
        group[f'{column}_corrected_median_include'] = group[column].where(group[f'{column}_category'] == 'Non-Outlier', median_include_outliers)
        group[f'{column}_corrected_median_exclude'] = group[column].where(group[f'{column}_category'] == 'Non-Outlier', median_exclude_outliers)
        group[f'{column}_corrected_moving_avg_include'] = moving_avg_include_outliers
        group[f'{column}_corrected_moving_avg_exclude'] = moving_avg_exclude_outliers
        group[f'{column}_corrected_winsorised'] = group[column].where(group[f'{column}_category'] == 'Non-Outlier', winsorised)

        results.append(group)

    final_df = pd.concat(results)

    export_columns = [
        'adm1', 'adm2', 'adm3', 'hf', 'hf_uid','year','month', 'Date', column,
        f'{column}_category', f'{column}_lower_bound', f'{column}_upper_bound',
        f'{column}_corrected_mean_include', f'{column}_corrected_mean_exclude',
        f'{column}_corrected_median_include', f'{column}_corrected_median_exclude',
        f'{column}_corrected_moving_avg_include', f'{column}_corrected_moving_avg_exclude',
        f'{column}_corrected_winsorised'
    ]

    return final_df[export_columns]

# Streamlit app setup
st.title("Outlier Detection and Correction")

uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel):", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("### Preview of the uploaded dataset:")
    st.write(df.head())

    columns_to_process = ['allout', 'susp', 'test', 'conf', 'maltreat', 'pres', 'maladm', 'maldth']

    if columns_to_process:
        processed_dfs = []

        for column in columns_to_process:
            st.write(f"Processing column: {column}")
            processed_df = process_column(df, column)
            processed_dfs.append(processed_df)

            st.write(f"### Processed Data for {column}:")
            st.write(processed_df.head())

        # Merge all processed DataFrames on the specified keys
        merge_keys = ['adm1', 'adm2', 'adm3', 'hf', 'year', 'month']
        final_combined_df = processed_dfs[0]
        for df_to_merge in processed_dfs[1:]:
            final_combined_df = final_combined_df.merge(df_to_merge, on=merge_keys, how='outer')

        st.write("### Final Combined Data:")
        st.write(final_combined_df.head())

        # Export combined DataFrame
        combined_buffer = BytesIO()
        final_combined_df.to_csv(combined_buffer, index=False)
        st.download_button(
            label="Download Cleaned Routine Data",
            data=combined_buffer.getvalue(),
            file_name="clean_routine_data.csv",
            mime="text/csv"
        )

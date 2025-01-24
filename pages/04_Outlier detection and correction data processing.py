import streamlit as st
import pandas as pd
import numpy as np
from typing import Tuple

def detect_outliers_scatterplot(series: pd.Series) -> Tuple[float, float]:
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return lower_bound, upper_bound

def calculate_moving_avg(series: pd.Series, window: int) -> pd.Series:
    # Store original NA positions
    na_mask = series.isna()
    
    # Temporarily fill NAs for calculation
    temp_series = series.copy()
    temp_series = temp_series.fillna(method='ffill').fillna(method='bfill')
    
    # Calculate moving average
    ma = temp_series.rolling(window=window, min_periods=1).mean()
    
    # Restore original NAs
    ma[na_mask] = np.nan
    return ma

def calculate_moving_avg_excluding_outliers(series: pd.Series, window: int, threshold: float = 1.5) -> pd.Series:
    # Store original NA positions
    na_mask = series.isna()
    
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    
    # Create mask for outliers and combine with original NA mask
    outlier_mask = (series < lower_bound) | (series > upper_bound)
    
    clean_series = series.copy()
    clean_series[outlier_mask] = np.nan
    
    # Temporarily fill NAs for calculation
    temp_series = clean_series.fillna(method='ffill').fillna(method='bfill')
    
    # Calculate moving average
    ma = temp_series.rolling(window=window, min_periods=1).mean()
    
    # Restore original NAs
    ma[na_mask] = np.nan
    return ma

def process_columns(df: pd.DataFrame, column: str) -> pd.DataFrame:
    try:
        # Handle a single column and retain all original columns
        df = df.copy()
        grouped = df.groupby(['adm1', 'adm2', 'adm3', 'hf', 'year'])
        
        # Calculate outlier bounds and metrics for the column
        lower_bound, upper_bound = detect_outliers_scatterplot(df[column])
        df[f'{column}_lower_bound'] = lower_bound
        df[f'{column}_upper_bound'] = upper_bound
        
        mask = (df[column] < lower_bound) | (df[column] > upper_bound)
        df[f'{column}_category'] = np.where(mask, 'Outlier', 'Non-Outlier')
        
        non_outliers = ~mask
        mean_include = df[column].mean()
        mean_exclude = df[column][non_outliers].mean()
        median_include = df[column].median()
        median_exclude = df[column][non_outliers].median()
        moving_avg_include = calculate_moving_avg(df[column], 3)
        moving_avg_exclude = calculate_moving_avg_excluding_outliers(df[column], 3)
        winsorised = np.clip(df[column], lower_bound, upper_bound)
        
        df[f'{column}_corrected_mean_include'] = np.where(mask, mean_include, df[column])
        df[f'{column}_corrected_mean_exclude'] = np.where(mask, mean_exclude, df[column])
        df[f'{column}_corrected_median_include'] = np.where(mask, median_include, df[column])
        df[f'{column}_corrected_median_exclude'] = np.where(mask, median_exclude, df[column])
        df[f'{column}_corrected_moving_avg_include'] = np.where(mask, moving_avg_include, df[column])
        df[f'{column}_corrected_moving_avg_exclude'] = np.where(mask, moving_avg_exclude, df[column])
        df[f'{column}_corrected_winsorised'] = np.where(mask, winsorised, df[column])
        
        return df
        
    except Exception as e:
        st.error(f"Error processing column {column}: {str(e)}")
        return None

st.title("Malaria Data Outlier Processor")

uploaded_file = st.file_uploader("Upload key_variables.csv", type=['csv', 'xlsx', 'xls'])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        columns_to_process = ["allout", "susp", "test", "conf", "maltreat", 
                            "pres", "maladm", "maldth"]
        
        # Process each column and keep all results in a single dataframe
        processed_df = df.copy()
        progress_bar = st.progress(0)
        
        for i, column in enumerate(columns_to_process):
            temp_df = process_columns(processed_df, column)
            if temp_df is not None:
                processed_df = temp_df
            progress_bar.progress((i + 1) / len(columns_to_process))
        
        st.success("Processing complete!")
        with st.expander("View Processed Data"):
            st.dataframe(processed_df)
        
        csv = processed_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Results",
            csv,
            "outlier_analysis_results.csv",
            "text/csv"
        )
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

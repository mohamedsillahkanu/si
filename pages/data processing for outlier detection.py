import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import iqr
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(layout="wide", page_title="Step-by-Step Outlier Tool")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'df' not in st.session_state:
    st.session_state.df = None
if 'settings' not in st.session_state:
    st.session_state.settings = {}
if 'processed_df' not in st.session_state:
    st.session_state.processed_df = None

# Helper functions
def detect_outliers_scatterplot(series, threshold=1.5):
    """Detect outliers using IQR method"""
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    return lower_bound, upper_bound

def calculate_moving_avg(series, window):
    """Calculate moving average with handling for missing values"""
    filled_series = series.fillna(method='bfill').fillna(method='ffill')
    moving_avg = filled_series.rolling(window=window, min_periods=1).mean()
    return moving_avg.where(series.notna(), np.nan)

def calculate_moving_avg_excluding_outliers(series, window, threshold=1.5):
    """Calculate moving average excluding outliers"""
    lower_bound, upper_bound = detect_outliers_scatterplot(series, threshold)
    clean_series = series.copy()
    clean_series[(series < lower_bound) | (series > upper_bound)] = np.nan
    return calculate_moving_avg(clean_series, window)

def calculate_exponential_ma(series, span):
    """Calculate exponential moving average"""
    return series.ewm(span=span, adjust=False).mean()

def calculate_double_ma(series, window):
    """Calculate double moving average"""
    first_ma = calculate_moving_avg(series, window)
    return calculate_moving_avg(first_ma, window)

def calculate_triple_ma(series, window):
    """Calculate triple moving average"""
    first_ma = calculate_moving_avg(series, window)
    second_ma = calculate_moving_avg(first_ma, window)
    return calculate_moving_avg(second_ma, window)

def calculate_weighted_ma(series, window):
    """Calculate weighted moving average"""
    weights = np.linspace(1, 2, window)
    return series.rolling(window=window, min_periods=1).apply(
        lambda x: np.average(x, weights=weights[-len(x):])
    )

def process_group(group, settings):
    """Process a group of data with the specified settings"""
    column = settings['column']
    threshold = settings['threshold']
    window = settings['window']
    method = settings['correction_method']
    
    # Detect outliers
    lower_bound, upper_bound = detect_outliers_scatterplot(group[column], threshold)
    is_outlier = (group[column] < lower_bound) | (group[column] > upper_bound)
    group['outlier_status'] = np.where(is_outlier, 'Outlier', 'Normal')
    
    # Apply selected correction method
    if method == 'Simple Moving Average':
        corrected_values = calculate_moving_avg(group[column], window)
    elif method == 'Exponential Moving Average':
        corrected_values = calculate_exponential_ma(group[column], window)
    elif method == 'Double Moving Average':
        corrected_values = calculate_double_ma(group[column], window)
    elif method == 'Triple Moving Average':
        corrected_values = calculate_triple_ma(group[column], window)
    elif method == 'Weighted Moving Average':
        corrected_values = calculate_weighted_ma(group[column], window)
    elif method == 'Moving Average (Excluding Outliers)':
        corrected_values = calculate_moving_avg_excluding_outliers(group[column], window, threshold)
    else:  # Default to winsorization
        corrected_values = group[column].clip(lower=lower_bound, upper=upper_bound)
    
    # Apply corrections only to outliers
    group['corrected_values'] = np.where(is_outlier, corrected_values, group[column])
    return group

# Main app
st.title("🔍 Step-by-Step Outlier Detection and Correction")

# Progress indicator
progress_text = {
    1: "Step 1: Upload Data",
    2: "Step 2: Configure Settings",
    3: "Step 3: Process Data",
    4: "Step 4: Export Results"
}

st.write(f"**Current Stage:** {progress_text[st.session_state.step]}")
progress_bar = st.progress(st.session_state.step / 4)

# Step 1: File Upload
if st.session_state.step == 1:
    st.header("📤 Upload Your Data")
    
    uploaded_file = st.file_uploader(
        "Upload your dataset (CSV, XLSX, or XLS)",
        type=["csv", "xlsx", "xls"]
    )
    
    if uploaded_file:
        try:
            file_type = uploaded_file.name.split('.')[-1]
            if file_type == "csv":
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success("✅ File uploaded successfully!")
            
            # Display data preview
            st.subheader("Data Preview")
            col1, col2, col3 = st.columns(3)
            col1.metric("Rows", df.shape[0])
            col2.metric("Columns", df.shape[1])
            col3.metric("Missing Values", df.isna().sum().sum())
            
            st.dataframe(df.head())
            
            if st.button("✨ Proceed to Settings"):
                st.session_state.df = df
                st.session_state.step = 2
                st.experimental_rerun()
        
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")

# Step 2: Settings Configuration
elif st.session_state.step == 2:
    st.header("⚙️ Configure Analysis Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Basic settings
        numeric_cols = st.session_state.df.select_dtypes(include=[np.number]).columns
        selected_column = st.selectbox(
            "Select column to analyze:",
            options=numeric_cols
        )
        
        grouping_cols = st.multiselect(
            "Select grouping columns:",
            options=st.session_state.df.columns,
            default=['hf_uid', 'year'] if all(col in st.session_state.df.columns for col in ['hf_uid', 'year']) else []
        )
    
    with col2:
        # Method selection
        correction_method = st.selectbox(
            "Select correction method:",
            [
                "Simple Moving Average",
                "Exponential Moving Average",
                "Double Moving Average",
                "Triple Moving Average",
                "Weighted Moving Average",
                "Moving Average (Excluding Outliers)",
                "Winsorization"
            ]
        )
    
    # Advanced settings
    st.subheader("Advanced Settings")
    col3, col4 = st.columns(2)
    
    with col3:
        threshold = st.slider(
            "Outlier detection threshold:",
            min_value=1.0, max_value=3.0, value=1.5, step=0.1,
            help="Higher values are more permissive"
        )
    
    with col4:
        window_size = st.slider(
            "Window size:",
            min_value=2, max_value=12, value=3,
            help="Used for moving averages and rolling calculations"
        )
    
    # Navigation buttons
    col5, col6 = st.columns(2)
    with col5:
        if st.button("⬅️ Back to Upload"):
            st.session_state.step = 1
            st.experimental_rerun()
    
    with col6:
        if st.button("✨ Save Settings & Continue"):
            st.session_state.settings = {
                'column': selected_column,
                'grouping_cols': grouping_cols,
                'correction_method': correction_method,
                'threshold': threshold,
                'window': window_size
            }
            st.session_state.step = 3
            st.experimental_rerun()

# Step 3: Processing
elif st.session_state.step == 3:
    st.header("🔄 Process Data")
    
    # Display current settings
    st.subheader("Current Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Column:** {st.session_state.settings['column']}")
        st.write(f"**Method:** {st.session_state.settings['correction_method']}")
        st.write(f"**Threshold:** {st.session_state.settings['threshold']}")
    
    with col2:
        st.write(f"**Window Size:** {st.session_state.settings['window']}")
        st.write(f"**Grouping:** {', '.join(st.session_state.settings['grouping_cols'])}")
    
    # Process button
    if st.button("🚀 Process Data"):
        with st.spinner("Processing data..."):
            try:
                grouped = st.session_state.df.groupby(st.session_state.settings['grouping_cols'])
                processed_df = grouped.apply(
                    lambda x: process_group(x, st.session_state.settings)
                ).reset_index(drop=True)
                
                st.session_state.processed_df = processed_df
                st.success("✅ Processing complete!")
                
                # Show preview of results
                st.subheader("Results Preview")
                st.dataframe(processed_df.head())
                
                if st.button("✨ Continue to Export"):
                    st.session_state.step = 4
                    st.experimental_rerun()
            
            except Exception as e:
                st.error(f"Error during processing: {str(e)}")
    
    # Navigation
    if st.button("⬅️ Back to Settings"):
        st.session_state.step = 2
        st.experimental_rerun()

# Step 4: Export
elif st.session_state.step == 4:
    st.header("💾 Export Results")
    
    # Export options
    export_format = st.radio(
        "Select export format:",
        ["Excel", "CSV"]
    )
    
    filename = st.text_input(
        "Enter filename:",
        f"processed_data_{datetime.now().strftime('%Y%m%d')}"
    )
    
    columns_to_export = st.multiselect(
        "Select columns to export:",
        st.session_state.processed_df.columns,
        default=st.session_state.processed_df.columns
    )
    
    if st.button("📥 Export Data"):
        export_df = st.session_state.processed_df[columns_to_export]
        
        if export_format == "Excel":
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                export_df.to_excel(writer, index=False)
            
            st.download_button(
                label="📥 Download Excel file",
                data=output.getvalue(),
                file_name=f"{filename}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            csv = export_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV file",
                data=csv,
                file_name=f"{filename}.csv",
                mime="text/csv"
            )
    
    # Navigation and reset
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("⬅️ Back to Processing"):
            st.session_state.step = 3
            st.experimental_rerun()
    
    with col2:
        if st.button("🔄 Start New Analysis"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.session_state.step = 1
            st.experimental_rerun()

# Bottom of page - Always show step indicator
st.markdown("---")
st.caption(f"Progress: {st.session_state.step}/4 - {progress_text[st.session_state.step]}")

import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import iqr
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(layout="wide", page_title="Advanced Outlier Tool")

# Helper functions for median methods
def calculate_median_all(series):
    """Calculate median including outliers"""
    return series.median()

def calculate_median_excluding_outliers(series, threshold=1.5):
    """Calculate median excluding outliers"""
    lower_bound, upper_bound = detect_outliers_scatterplot(series, threshold)
    clean_series = series[(series >= lower_bound) & (series <= upper_bound)]
    return clean_series.median()

def calculate_rolling_median(series, window):
    """Calculate rolling median"""
    return series.rolling(window=window, min_periods=1).median()

def calculate_weighted_median(series, window):
    """Calculate weighted median with more weight on recent values"""
    weights = np.linspace(1, 2, window)
    return series.rolling(window=window, min_periods=1).apply(
        lambda x: np.average(x, weights=weights[-len(x):])
    )

# Helper functions for moving average methods
def calculate_simple_ma(series, window):
    """Calculate simple moving average"""
    return series.rolling(window=window, min_periods=1).mean()

def calculate_exponential_ma(series, span):
    """Calculate exponential moving average"""
    return series.ewm(span=span, adjust=False).mean()

def calculate_double_ma(series, window):
    """Calculate double moving average"""
    first_ma = calculate_simple_ma(series, window)
    return calculate_simple_ma(first_ma, window)

def calculate_triple_ma(series, window):
    """Calculate triple moving average"""
    first_ma = calculate_simple_ma(series, window)
    second_ma = calculate_simple_ma(first_ma, window)
    return calculate_simple_ma(second_ma, window)

def calculate_weighted_ma(series, window):
    """Calculate weighted moving average"""
    weights = np.linspace(1, 2, window)
    return series.rolling(window=window, min_periods=1).apply(
        lambda x: np.average(x, weights=weights[-len(x):])
    )

def detect_outliers_scatterplot(series, threshold=1.5):
    """Detect outliers using IQR method"""
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    return lower_bound, upper_bound

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
    if method == 'Median (All Values)':
        corrected_values = calculate_median_all(group[column])
    elif method == 'Median (Excluding Outliers)':
        corrected_values = calculate_median_excluding_outliers(group[column], threshold)
    elif method == 'Rolling Median':
        corrected_values = calculate_rolling_median(group[column], window)
    elif method == 'Weighted Median':
        corrected_values = calculate_weighted_median(group[column], window)
    elif method == 'Simple Moving Average':
        corrected_values = calculate_simple_ma(group[column], window)
    elif method == 'Exponential Moving Average':
        corrected_values = calculate_exponential_ma(group[column], window)
    elif method == 'Double Moving Average':
        corrected_values = calculate_double_ma(group[column], window)
    elif method == 'Triple Moving Average':
        corrected_values = calculate_triple_ma(group[column], window)
    elif method == 'Weighted Moving Average':
        corrected_values = calculate_weighted_ma(group[column], window)
    else:  # Default to winsorization
        corrected_values = group[column].clip(lower=lower_bound, upper=upper_bound)
    
    # Apply corrections only to outliers
    group['corrected_values'] = np.where(is_outlier, corrected_values, group[column])
    return group

# Main app
st.title("🔍 Advanced Outlier Detection and Correction Tool")

# File upload section
with st.expander("📤 Upload Data", expanded=True):
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
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Rows", df.shape[0])
            col2.metric("Columns", df.shape[1])
            col3.metric("Missing Values", df.isna().sum().sum())
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            st.stop()
    else:
        st.info("Please upload a file to begin analysis")
        st.stop()

# Create tabs
tab1, tab2, tab3 = st.tabs([
    "⚙️ Method Selection",
    "📊 Analysis & Visualization",
    "💾 Export Options"
])

with tab1:
    st.subheader("Analysis Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Column selection
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        selected_column = st.selectbox(
            "Select column to analyze:",
            options=numeric_cols
        )
        
        # Grouping columns
        grouping_cols = st.multiselect(
            "Select grouping columns:",
            options=df.columns,
            default=['hf_uid', 'year'] if all(col in df.columns for col in ['hf_uid', 'year']) else []
        )
    
    with col2:
        # Method selection with categorized options
        method_category = st.selectbox(
            "Select method category:",
            ["Median Methods", "Moving Average Methods", "Other Methods"]
        )
        
        if method_category == "Median Methods":
            correction_method = st.selectbox(
                "Select median method:",
                [
                    "Median (All Values)",
                    "Median (Excluding Outliers)",
                    "Rolling Median",
                    "Weighted Median"
                ]
            )
        elif method_category == "Moving Average Methods":
            correction_method = st.selectbox(
                "Select moving average method:",
                [
                    "Simple Moving Average",
                    "Exponential Moving Average",
                    "Double Moving Average",
                    "Triple Moving Average",
                    "Weighted Moving Average"
                ]
            )
        else:
            correction_method = st.selectbox(
                "Select other method:",
                [
                    "Winsorization",
                    "Mean (Including Outliers)",
                    "Mean (Excluding Outliers)"
                ]
            )
        
        # Advanced settings based on method
        threshold = st.slider(
            "Outlier detection threshold:",
            min_value=1.0,
            max_value=3.0,
            value=1.5,
            step=0.1
        )
        
        window_size = st.slider(
            "Window size:",
            min_value=2,
            max_value=12,
            value=3,
            help="Used for moving averages and rolling calculations"
        )

with tab2:
    if st.button("Run Analysis"):
        with st.spinner("Processing data..."):
            settings = {
                'column': selected_column,
                'threshold': threshold,
                'window': window_size,
                'correction_method': correction_method
            }
            
            grouped = df.groupby(grouping_cols)
            processed_df = grouped.apply(
                lambda x: process_group(x, settings)
            ).reset_index(drop=True)
            
            # Results display
            st.subheader("Results Overview")
            
            # Summary statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                n_outliers = (processed_df['outlier_status'] == 'Outlier').sum()
                st.metric("Outliers Detected", n_outliers)
                st.metric("Outlier Percentage", f"{(n_outliers/len(processed_df))*100:.1f}%")
            
            with col2:
                st.metric("Original Mean", f"{processed_df[selected_column].mean():.2f}")
                st.metric("Corrected Mean", f"{processed_df['corrected_values'].mean():.2f}")
            
            with col3:
                st.metric("Original Std", f"{processed_df[selected_column].std():.2f}")
                st.metric("Corrected Std", f"{processed_df['corrected_values'].std():.2f}")
            
            # Visualization
            fig = go.Figure()
            
            # Original values with outliers highlighted
            fig.add_trace(go.Scatter(
                x=processed_df.index,
                y=processed_df[selected_column],
                mode='markers',
                name='Original Values',
                marker=dict(
                    color=np.where(processed_df['outlier_status'] == 'Outlier', 'red', 'blue'),
                    size=np.where(processed_df['outlier_status'] == 'Outlier', 10, 6)
                )
            ))
            
            # Corrected values
            fig.add_trace(go.Scatter(
                x=processed_df.index,
                y=processed_df['corrected_values'],
                mode='lines',
                name='Corrected Values',
                line=dict(color='green', width=2)
            ))
            
            fig.update_layout(
                title=f"{selected_column} - Original vs Corrected Values using {correction_method}",
                xaxis_title="Index",
                yaxis_title="Value",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Store processed data
            st.session_state['processed_df'] = processed_df

with tab3:
    if 'processed_df' in st.session_state:
        st.subheader("Export Options")
        
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
        
        if st.button("Export Data"):
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
    else:
        st.info("Run the analysis first to enable export options")

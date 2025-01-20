import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import iqr
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(layout="wide", page_title="Interactive Outlier Tool")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .plot-container {
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

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

def process_group(group, settings):
    """Process a group of data with the specified settings"""
    column = settings['column']
    threshold = settings['threshold']
    window = settings['window']
    method = settings['correction_method']
    
    lower_bound, upper_bound = detect_outliers_scatterplot(group[column], threshold)
    
    is_outlier = (group[column] < lower_bound) | (group[column] > upper_bound)
    group['outlier_status'] = np.where(is_outlier, 'Outlier', 'Normal')
    
    if method == 'Mean (Including Outliers)':
        corrected_values = group[column].mean()
    elif method == 'Mean (Excluding Outliers)':
        corrected_values = group[column][~is_outlier].mean()
    elif method == 'Median':
        corrected_values = group[column].median()
    elif method == 'Moving Average':
        corrected_values = calculate_moving_avg(group[column], window)
    elif method == 'Moving Average (Excluding Outliers)':
        corrected_values = calculate_moving_avg_excluding_outliers(group[column], window, threshold)
    else:  # Winsorization
        corrected_values = group[column].clip(lower=lower_bound, upper=upper_bound)
    
    group['corrected_values'] = np.where(is_outlier, corrected_values, group[column])
    return group

# Main app
st.title("🔍 Interactive Outlier Detection and Correction Tool")
st.write("Upload your data and customize the outlier detection process")

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
            
            # Display basic info
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

# Create tabs for different operations
tab1, tab2, tab3 = st.tabs([
    "⚙️ Settings",
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
        # Method selection
        correction_method = st.selectbox(
            "Select correction method:",
            [
                "Mean (Including Outliers)",
                "Mean (Excluding Outliers)",
                "Median",
                "Moving Average",
                "Moving Average (Excluding Outliers)",
                "Winsorization"
            ]
        )
        
        # Advanced settings
        threshold = st.slider(
            "Outlier detection threshold:",
            min_value=1.0,
            max_value=3.0,
            value=1.5,
            step=0.1,
            help="Higher values are more permissive"
        )
        
        window_size = st.slider(
            "Moving average window size:",
            min_value=2,
            max_value=10,
            value=3,
            help="Larger windows create smoother results"
        )

with tab2:
    if st.button("Run Analysis"):
        with st.spinner("Processing data..."):
            # Store settings
            settings = {
                'column': selected_column,
                'threshold': threshold,
                'window': window_size,
                'correction_method': correction_method
            }
            
            # Process data
            grouped = df.groupby(grouping_cols)
            processed_df = grouped.apply(
                lambda x: process_group(x, settings)
            ).reset_index(drop=True)
            
            # Display results
            st.subheader("Results Overview")
            
            # Summary statistics
            col1, col2 = st.columns(2)
            with col1:
                n_outliers = (processed_df['outlier_status'] == 'Outlier').sum()
                st.metric("Number of Outliers", n_outliers)
                st.metric("Outlier Percentage", f"{(n_outliers/len(processed_df))*100:.1f}%")
            
            with col2:
                st.metric("Original Mean", f"{processed_df[selected_column].mean():.2f}")
                st.metric("Corrected Mean", f"{processed_df['corrected_values'].mean():.2f}")
            
            # Visualization
            st.subheader("Visualization")
            
            # Time series plot if date column exists
            fig = go.Figure()
            
            # Add original values
            fig.add_trace(go.Scatter(
                x=processed_df.index,
                y=processed_df[selected_column],
                mode='markers',
                name='Original Values',
                marker=dict(
                    color=np.where(processed_df['outlier_status'] == 'Outlier', 'red', 'blue')
                )
            ))
            
            # Add corrected values
            fig.add_trace(go.Scatter(
                x=processed_df.index,
                y=processed_df['corrected_values'],
                mode='lines',
                name='Corrected Values',
                line=dict(color='green')
            ))
            
            fig.update_layout(
                title=f"{selected_column} - Original vs Corrected Values",
                xaxis_title="Index",
                yaxis_title="Value",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Store processed data in session state
            st.session_state['processed_df'] = processed_df

with tab3:
    if 'processed_df' in st.session_state:
        st.subheader("Export Options")
        
        # Export format selection
        export_format = st.radio(
            "Select export format:",
            ["Excel", "CSV"]
        )
        
        # Filename customization
        default_filename = f"processed_data_{datetime.now().strftime('%Y%m%d')}"
        filename = st.text_input("Enter filename:", default_filename)
        
        # Column selection for export
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

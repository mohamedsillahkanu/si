import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def create_plots(df, hf_id, year):
    plot_labels = {
        "allout": "All Outpatients",
        "susp": "Suspected Cases",
        "test": "Tests Conducted",
        "conf": "Confirmed Cases",
        "maltreat": "Malaria Treatments",
        "pres": "Presumptive Treatment",
        "maladm": "Malaria Admissions",
        "maldth": "Malaria Deaths"
    }
    
    df_filtered = df[df['hf_uid'] == hf_id]
    df_filtered = df_filtered[df_filtered['year'] == year]
    
    if len(df_filtered) == 0:
        st.error(f"No data to display for facility {hf_id} in year {year}")
        return
    
    for var, var_label in plot_labels.items():
        if var not in df_filtered.columns or df_filtered[var].isna().all():
            st.warning(f"No data available for {var_label}")
            continue
            
        methods = [
            var,
            f"{var}_corrected_mean_include",
            f"{var}_corrected_mean_exclude",
            f"{var}_corrected_median_include",
            f"{var}_corrected_median_exclude",
            f"{var}_corrected_moving_avg_include",
            f"{var}_corrected_moving_avg_exclude",
            f"{var}_corrected_winsorised"
        ]
        
        # Get max y-value across all methods
        max_y = max([df_filtered[m].max() for m in methods if m in df_filtered.columns])
        
        fig = make_subplots(rows=4, cols=2, subplot_titles=methods)
        
        for i, method in enumerate(methods, 1):
            row = (i-1) // 2 + 1
            col = (i-1) % 2 + 1
            
            if method in df_filtered.columns:
                Q1 = df_filtered[method].quantile(0.25)
                Q3 = df_filtered[method].quantile(0.75)
                IQR = Q3 - Q1
                lower = max(0, Q1 - 1.5 * IQR)
                upper = Q3 + 1.5 * IQR
                
                # Split points into outliers and non-outliers
                mask = (df_filtered[method] >= lower) & (df_filtered[method] <= upper)
                non_outliers = df_filtered[mask]
                outliers = df_filtered[~mask]
                
                # Non-outlier points (blue)
                fig.add_trace(
                    go.Scatter(
                        x=non_outliers['month'],
                        y=non_outliers[method],
                        mode='markers',
                        name='Non-Outliers',
                        marker=dict(color='blue', size=8),
                        showlegend=(i == 1)
                    ),
                    row=row, col=col
                )
                
                # Handle outliers based on method type
                if not method.startswith(f"{var}_corrected"):
                    fig.add_trace(
                        go.Scatter(
                            x=outliers['month'],
                            y=outliers[method],
                            mode='markers',
                            name='Outliers',
                            marker=dict(color='red', size=8),
                            showlegend=(i == 1)
                        ),
                        row=row, col=col
                    )
                else:
                    corrected = df_filtered[df_filtered[f'{var}_category'] == 'Outlier']
                    fig.add_trace(
                        go.Scatter(
                            x=corrected['month'],
                            y=corrected[method],
                            mode='markers',
                            name='Corrected',
                            marker=dict(color='green', size=8),
                            showlegend=(i == 1)
                        ),
                        row=row, col=col
                    )
                
                # Add bounds
                fig.add_hline(y=lower, line=dict(color="green", dash="dash"), 
                            row=row, col=col, name="Lower Bound", showlegend=(i == 1))
                fig.add_hline(y=upper, line=dict(color="red", dash="dash"), 
                            row=row, col=col, name="Upper Bound", showlegend=(i == 1))
                
                # Update axes
                fig.update_xaxes(
                    title_text="Month",
                    ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    tickvals=[str(i).zfill(2) for i in range(1, 13)],
                    row=row, col=col
                )
                fig.update_yaxes(
                    title_text=var_label,
                    range=[0, max_y * 1.1],
                    row=row, col=col
                )
        
        fig.update_layout(
            height=1200,
            width=1000,
            title=f"{var_label} ({hf_id}) - Year {year}",
            showlegend=True
        )
        
        st.plotly_chart(fig)

st.title("Malaria Data Visualization")

uploaded_file = st.file_uploader("Upload outlier_analysis_data.csv", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    col1, col2 = st.columns(2)
    with col1:
        facility = st.selectbox("Select Facility ID", sorted(df['hf_uid'].unique()))
    with col2:
        year = st.selectbox("Select Year", sorted(df[df['hf_uid'] == facility]['year'].unique()))
        
    if st.button("Generate Plots"):
        create_plots(df, facility, year)

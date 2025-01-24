import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_variable_plots(df, hf_id, year):
    variables_labels = {
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
        
    for variable, variable_label in variables_labels.items():
        # Check if variable exists and has data
        if not any(col.startswith(variable) for col in df_filtered.columns) or df_filtered[variable].isna().all():
            st.warning(f"No data to display for {variable_label}")
            continue
        
        correction_methods = [
            variable,
            f"{variable}_corrected_mean_include",
            f"{variable}_corrected_mean_exclude",
            f"{variable}_corrected_median_include",
            f"{variable}_corrected_median_exclude",
            f"{variable}_corrected_moving_avg_include",
            f"{variable}_corrected_moving_avg_exclude",
            f"{variable}_corrected_winsorised"
        ]
        
        # Create subplots
        fig = make_subplots(rows=4, cols=2, subplot_titles=correction_methods)
        
        for i, method in enumerate(correction_methods, 1):
            row = (i-1) // 2 + 1
            col = (i-1) % 2 + 1
            
            if method in df_filtered.columns:
                # Calculate IQR bounds
                Q1 = df_filtered[method].quantile(0.25)
                Q3 = df_filtered[method].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = max(0, Q1 - 1.5 * IQR)
                upper_bound = Q3 + 1.5 * IQR
                
                # Non-outliers
                mask = (df_filtered[method] >= lower_bound) & (df_filtered[method] <= upper_bound)
                non_outliers = df_filtered[mask]
                outliers = df_filtered[~mask]
                
                # Base points
                fig.add_trace(
                    go.Scatter(
                        x=non_outliers['month'],
                        y=non_outliers[method],
                        mode='markers',
                        name='Non-Outliers',
                        marker=dict(color='blue'),
                        legendgroup='non_outliers',
                        showlegend=(i == 1)
                    ),
                    row=row, col=col
                )
                
                # Outliers or corrected points
                if not method.startswith(f"{variable}_corrected"):
                    fig.add_trace(
                        go.Scatter(
                            x=outliers['month'],
                            y=outliers[method],
                            mode='markers',
                            name='Outliers',
                            marker=dict(color='red'),
                            legendgroup='outliers',
                            showlegend=(i == 1)
                        ),
                        row=row, col=col
                    )
                else:
                    # Show corrected points
                    corrected_points = df_filtered[df_filtered[f'{variable}_category'] == 'Outlier']
                    fig.add_trace(
                        go.Scatter(
                            x=corrected_points['month'],
                            y=corrected_points[method],
                            mode='markers',
                            name='Corrected',
                            marker=dict(color='green'),
                            legendgroup='corrected',
                            showlegend=(i == 1)
                        ),
                        row=row, col=col
                    )
                
                # Add IQR bounds with annotations in legend
                fig.add_hline(
                    y=lower_bound, 
                    line=dict(color="green", dash="dash"), 
                    row=row, col=col,
                    name=f"Lower Bound ({lower_bound:.2f})",
                    showlegend=(i == 1)
                )
                fig.add_hline(
                    y=upper_bound, 
                    line=dict(color="red", dash="dash"), 
                    row=row, col=col,
                    name=f"Upper Bound ({upper_bound:.2f})",
                    showlegend=(i == 1)
                )

        fig.update_layout(
            height=1200,
            width=1000,
            title=f"{variable_label} ({hf_id}) - Year {year}",
            showlegend=True,
        )
        
        # Update axes for all subplots
        for i in range(8):
            fig.update_yaxes(
                title_text=variable_label,
                row=(i//2)+1, 
                col=(i%2)+1,
                tickmode='auto',
                nticks=10
            )
            fig.update_xaxes(
                title_text="Month",
                row=(i//2)+1,
                col=(i%2)+1,
                ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                tickvals=[str(i).zfill(2) for i in range(1, 13)]
            )

        st.plotly_chart(fig)

st.title("Malaria Data Visualization")

uploaded_file = st.file_uploader("Upload outlier_analysis_data.csv", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Get unique facility IDs and years
    facility_ids = sorted(df['hf_uid'].unique())
    selected_facility = st.selectbox("Select Facility ID", facility_ids)
    
    years = sorted(df[df['hf_uid'] == selected_facility]['year'].unique())
    selected_year = st.selectbox("Select Year", years)
    
    if st.button("Generate Plots"):
        create_variable_plots(df, selected_facility, selected_year)

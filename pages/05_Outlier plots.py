import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import io
import openpyxl

def load_data(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file)
    return df

def create_hfid_variable_subplots(df, variables, hfid, year, plot_labels):
    """
    Create subplots for HFID and variable with consistent y-axis scale.
    """
    hfid_df = df[(df['hf_uid'] == hfid) & (df['year'] == year)]
    if hfid_df.empty:
        st.error(f"No data available for HFID: {hfid} in Year: {year}")
        return

    for column in variables:
        fig, axes = plt.subplots(4, 2, figsize=(15, 18))
        axes = axes.flatten()

        correction_methods = [
            column,
            f'{column}_corrected_mean_include',
            f'{column}_corrected_mean_exclude',
            f'{column}_corrected_median_include',
            f'{column}_corrected_median_exclude',
            f'{column}_corrected_moving_avg_include',
            f'{column}_corrected_moving_avg_exclude',
            f'{column}_corrected_winsorised',
        ]

        max_y_value = float('-inf')
        min_y_value = float('inf')
        for method in correction_methods:
            if method in hfid_df.columns:
                max_y_value = max(max_y_value, hfid_df[method].max())
                min_y_value = min(min_y_value, hfid_df[method].min())

        for i, method in enumerate(correction_methods):
            if method in hfid_df.columns:
                Q1 = hfid_df[method].quantile(0.25)
                Q3 = hfid_df[method].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers = hfid_df[(hfid_df[method] < lower_bound) | (hfid_df[method] > upper_bound)]
                if f'{column}_category' in hfid_df.columns:
                    corrected_points = hfid_df[hfid_df[f'{column}_category'] == 'Outlier']
                else:
                    corrected_points = pd.DataFrame()

                if method == column:
                    axes[i].scatter(
                        hfid_df['month'], hfid_df[method],
                        alpha=0.7, color='blue', label='Non-Outlier'
                    )
                    if not outliers.empty:
                        axes[i].scatter(
                            outliers['month'], outliers[method],
                            color='red', label='Outlier', zorder=3
                        )
                else:
                    axes[i].scatter(
                        hfid_df['month'], hfid_df[method],
                        alpha=0.7, color='blue', label='Non-Outlier'
                    )
                    if not corrected_points.empty:
                        axes[i].scatter(
                            corrected_points['month'], corrected_points[method],
                            color='green', label='Corrected Outlier', zorder=4
                        )

                axes[i].axhline(lower_bound, color='green', linestyle='--', label='Lower Bound', linewidth=1)
                axes[i].axhline(upper_bound, color='red', linestyle='--', label='Upper Bound', linewidth=1)

                titles = {
                    column: "Outlier detection with raw data",
                    f'{column}_corrected_mean_include': "Outlier correction using mean (included outliers)",
                    f'{column}_corrected_mean_exclude': "Outlier correction using mean (excluded outliers)",
                    f'{column}_corrected_median_include': "Outlier correction using median (included outliers)",
                    f'{column}_corrected_median_exclude': "Outlier correction using median (excluded outliers)",
                    f'{column}_corrected_moving_avg_include': "Outlier correction using 3-months moving average (included)",
                    f'{column}_corrected_moving_avg_exclude': "Outlier correction using 3-months moving average (excluded)",
                    f'{column}_corrected_winsorised': "Outlier correction using winsorisation"
                }

                axes[i].set_title(titles.get(method, "Outlier analysis"))
                axes[i].set_xlabel('Month')
                axes[i].set_ylabel(plot_labels[column])
                axes[i].set_ylim(min_y_value, max_y_value)
            else:
                axes[i].text(0.5, 0.5, 'Data not available', ha='center', va='center', fontsize=12)
                axes[i].set_title("Missing Data")

        legend_elements = [
            mlines.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=8, label='Non-outlier'),
            mlines.Line2D([], [], color='red', marker='o', linestyle='None', markersize=8, label='Outlier'),
            mlines.Line2D([], [], color='green', marker='o', linestyle='None', markersize=8, label='Corrected outlier'),
            mlines.Line2D([], [], color='green', linestyle='--', label='Q1 bound'),
            mlines.Line2D([], [], color='red', linestyle='--', label='Q3 bound')
        ]

        fig.legend(
            handles=legend_elements,
            loc='upper center',
            bbox_to_anchor=(0.5, 1.03),
            ncol=5,
            title="Legend",
            fontsize=10
        )

        plt.tight_layout()
        plt.suptitle(f'{hfid}: Outlier detection and correction ({year})', fontsize=16, y=1.05)
        st.pyplot(fig)

def main():
    st.title("Outlier Detection and Correction Analysis")
    
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx', 'xls'])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        # Get unique HFIDs and years
        hfids = sorted(df['hf_uid'].unique())
        years = sorted(df['year'].unique())
        
        # User inputs
        col1, col2 = st.columns(2)
        with col1:
            selected_hfid = st.selectbox('Select HFID:', hfids)
        with col2:
            selected_year = st.selectbox('Select Year:', years)
            
        variables_to_process = ['allout', 'susp', 'test', 'conf', 'maltreat', 'pres', 'maladm', 'maldth']
        plot_labels = {
            'allout': 'All outpatients',
            'susp': 'Suspected cases',
            'test': 'Tests conducted',
            'conf': 'Confirmed cases',
            'maltreat': 'Malaria treatments',
            'pres': 'Presumtive treatment',
            'maladm': 'Malaria admissions',
            'maldth': 'Malaria deaths'
        }
        
        if st.button('Generate Plots'):
            create_hfid_variable_subplots(df, variables_to_process, selected_hfid, selected_year, plot_labels)

if __name__ == '__main__':
    main()

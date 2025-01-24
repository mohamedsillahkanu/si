import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import pandas as pd

# Function to create subplots for each HFID and variable
def create_hfid_variable_subplots(df, variables, hfid, year, plot_labels):
    """
    Create subplots for each HFID and variable with consistent y-axis scale within a figure.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.
    - variables (list): List of variables to plot.
    - hfid (str): Selected HFID.
    - year (int): Selected year.
    - plot_labels (dict): Custom labels for variables as keys.
    """
    hfid_df = df[(df['hf_uid'] == hfid) & (df['year'] == year)]
    if hfid_df.empty:
        st.warning(f"No data available for HFID: {hfid} in Year: {year}")
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
                corrected_points = hfid_df[hfid_df.get(f'{column}_category') == 'Outlier']

                axes[i].scatter(
                    hfid_df['month'], hfid_df[method], alpha=0.7, color='blue', label='Non-Outlier'
                )
                if not outliers.empty:
                    axes[i].scatter(
                        outliers['month'], outliers[method], color='red', label='Outlier', zorder=3
                    )
                if not corrected_points.empty:
                    axes[i].scatter(
                        corrected_points['month'], corrected_points[method], color='green', label='Corrected Outlier', zorder=4
                    )

                axes[i].axhline(lower_bound, color='green', linestyle='--', label='Lower Bound', linewidth=1)
                axes[i].axhline(upper_bound, color='red', linestyle='--', label='Upper Bound', linewidth=1)

                axes[i].set_title(f"{plot_labels[column]} - {method}")
                axes[i].set_xlabel('Month')
                axes[i].set_ylabel('Value')
                axes[i].set_ylim(min_y_value, max_y_value)
            else:
                axes[i].text(0.5, 0.5, 'Data not available', horizontalalignment='center',
                             verticalalignment='center', fontsize=12)
                axes[i].set_title("Missing Data")

        blue_marker = mlines.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=8, label='Non-Outlier')
        red_marker = mlines.Line2D([], [], color='red', marker='o', linestyle='None', markersize=8, label='Outlier')
        green_marker = mlines.Line2D([], [], color='green', marker='o', linestyle='None', markersize=8, label='Corrected Outlier')
        green_line = mlines.Line2D([], [], color='green', linestyle='--', label='Q1 bound')
        red_line = mlines.Line2D([], [], color='red', linestyle='--', label='Q3 bound')

        fig.legend(
            handles=[blue_marker, red_marker, green_marker, green_line, red_line],
            loc='upper center',
            bbox_to_anchor=(0.5, 1.03),
            ncol=5,
            title="Legend",
            fontsize=10
        )

        plt.tight_layout()
        st.pyplot(fig)

# Streamlit app setup
st.title("Outlier Detection and Correction Viewer")

# File upload
uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx", "xls"])

if uploaded_file:
    # Load the data based on file type
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # User inputs
        hfids = df['hf_uid'].unique() if not df.empty else []
        years = df['year'].unique() if not df.empty else []

        selected_hfid = st.selectbox("Select HFID", hfids)
        selected_year = st.selectbox("Select Year", years)

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

        if st.button("Generate Plots"):
            create_hfid_variable_subplots(df, variables_to_process, selected_hfid, selected_year, plot_labels)
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a dataset to get started.")

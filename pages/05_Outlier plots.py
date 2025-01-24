import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    return pd.read_excel(file)

def create_plots(df, variables, hfid, year):
    hfid_df = df[(df['hf_uid'] == hfid) & (df['Year'] == year)]
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

        for i, method in enumerate(correction_methods):
            if method in hfid_df.columns:
                Q1 = hfid_df[method].quantile(0.25)
                Q3 = hfid_df[method].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers = hfid_df[(hfid_df[method] < lower_bound) | 
                                 (hfid_df[method] > upper_bound)]

                # Plot non-outliers
                axes[i].scatter(hfid_df['Month'], hfid_df[method], 
                              alpha=0.7, color='blue', label='Normal')
                
                # Plot outliers
                if not outliers.empty:
                    axes[i].scatter(outliers['Month'], outliers[method], 
                                  color='red', label='Outlier', zorder=3)

                # Add bounds
                axes[i].axhline(lower_bound, color='green', linestyle='--', 
                              label='Lower Bound', linewidth=1)
                axes[i].axhline(upper_bound, color='red', linestyle='--', 
                              label='Upper Bound', linewidth=1)

                axes[i].set_title(f'Analysis: {method}')
                axes[i].set_xlabel('Month')
                axes[i].set_ylabel('Value')
            else:
                axes[i].text(0.5, 0.5, 'No data available', 
                           ha='center', va='center', fontsize=12)

        # Create unified legend
        legend_elements = [
            mlines.Line2D([], [], color='blue', marker='o', linestyle='None', 
                         label='Normal Points'),
            mlines.Line2D([], [], color='red', marker='o', linestyle='None', 
                         label='Outliers'),
            mlines.Line2D([], [], color='green', linestyle='--', 
                         label='Lower Bound'),
            mlines.Line2D([], [], color='red', linestyle='--', 
                         label='Upper Bound')
        ]

        fig.legend(handles=legend_elements, loc='upper center', 
                  bbox_to_anchor=(0.5, 1.02), ncol=4)

        plt.tight_layout()
        plt.suptitle(f'{column} Analysis - HFID: {hfid}, Year: {year}', 
                    fontsize=16, y=1.05)
        st.pyplot(fig)

def main():
    st.title("Outlier Analysis Dashboard")

    uploaded_file = st.file_uploader("Upload your data (CSV/Excel)", 
                                   type=['csv', 'xlsx', 'xls'])

    if uploaded_file:
        df = load_data(uploaded_file)
        
        col1, col2 = st.columns(2)
        with col1:
            hfid = st.selectbox('Select HFID:', sorted(df['hf_uid'].unique()))
        with col2:
            year = st.selectbox('Select Year:', sorted(df['Year'].unique()))

        variables = ['allout', 'susp', 'test', 'conf', 'maltreat']
        
        if st.button('Generate Analysis'):
            create_plots(df, variables, hfid, year)

if __name__ == '__main__':
    main()

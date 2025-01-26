import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_reporting(df):
   df['report'] = df[['allout', 'susp', 'test', 'conf', 'maltreat']].sum(axis=1, min_count=1)
   df['conf'] = pd.to_numeric(df['conf'], errors='coerce')
   df['report_conf'] = np.where(df['conf'] > 0, 1, 0)
   
   df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + 
                              df['month'].astype(str).str.zfill(2))
   
   df['First_month_hf_reported'] = df.groupby('hf_uid')['date'].transform('min')
   df['do_hf_expected_to_report_per_month'] = np.where(
       df['date'] >= df['First_month_hf_reported'], 1, 0)

   hf_metrics = df.groupby(['adm3', 'date']).agg(
       num_hf_reporting_conf=('report_conf', 'sum'),
       num_hf_expected_to_report=('do_hf_expected_to_report_per_month', 'sum')
   ).reset_index()

   hf_metrics['reporting_rate'] = (hf_metrics['num_hf_reporting_conf'] / 
                                 hf_metrics['num_hf_expected_to_report'] * 100).round(2)

   heatmap_data = hf_metrics.pivot(
       index='adm3',
       columns='date',
       values='reporting_rate'
   )
   heatmap_data.columns = pd.to_datetime(heatmap_data.columns).strftime('%Y-%m')

   return hf_metrics, heatmap_data

def main():
   st.title("Health Facility Reporting Analysis")
   
   uploaded_file = st.file_uploader("Upload data file:", type=['csv', 'xlsx', 'xls'])
   
   if uploaded_file:
       try:
           if uploaded_file.name.endswith('.csv'):
               df = pd.read_csv(uploaded_file)
           else:
               df = pd.read_excel(uploaded_file)

           metrics, heatmap = analyze_reporting(df)
           
           st.write("### Reporting Metrics")
           st.dataframe(metrics.head())
           
           st.write("### Reporting Rate Heatmap")
           fig, ax = plt.subplots(figsize=(15, 10))
           sns.heatmap(heatmap,
                      annot=False,
                      fmt=".1f",
                      cmap="viridis",
                      linewidths=0,
                      cbar_kws={'label': 'Reporting Rate (%)'},
                      yticklabels=False)
           
           plt.title('Monthly Reporting Rate by ADM3')
           plt.xlabel('Date')
           plt.ylabel('ADM3')
           plt.xticks(rotation=90)
           plt.tight_layout()
           
           st.pyplot(fig)
           
           # Download buttons
           metrics_csv = metrics.to_csv(index=False).encode('utf-8')
           st.download_button("Download Metrics CSV",
                            metrics_csv,
                            "reporting_metrics.csv",
                            "text/csv")
           
       except Exception as e:
           st.error(f"Error: {str(e)}")

if __name__ == "__main__":
   main()

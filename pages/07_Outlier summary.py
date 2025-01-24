import streamlit as st
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_outlier_charts(df, column, chart_type):
    if 'year' not in df.columns:
        st.write("The dataset must contain a 'year' column for this analysis.")
        return
        
    grouped = df.groupby(['year', column]).size().unstack(fill_value=0)
    years = grouped.index.tolist()
    categories = grouped.columns.tolist()
    
    # Proper category mapping
    color_map = {
        'Outlier': 'red',
        'Non-Outlier': 'blue'
    }
    colors = [color_map[cat] for cat in categories]
    
    if chart_type == "Bar Chart":
        fig, axes = plt.subplots(3, 3, figsize=(15, 15), sharex=True, sharey=True)
        fig.suptitle("Outliers and Non-Outliers Bar Chart by Year", fontsize=16)
        
        axes = axes.flatten()
        for i, year in enumerate(years):
            if i < len(axes):
                ax = axes[i]
                year_data = grouped.loc[year]
                bars = ax.bar(categories, year_data, color=colors)
                ax.set_title(f"Year: {year}")
                ax.set_ylabel("Count")
                ax.set_xlabel("Categories")
                ax.set_xticklabels(categories, rotation=45, ha='right')
                
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(height)}', ha='center', va='bottom')
                           
        for j in range(len(years), len(axes)):
            fig.delaxes(axes[j])
            
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        st.pyplot(fig)
        
    elif chart_type == "Pie Chart":
        fig, axes = plt.subplots(3, 3, figsize=(15, 15))
        fig.suptitle("Outliers and Non-Outliers Pie Chart by Year", fontsize=16)
        
        axes = axes.flatten()
        for i, year in enumerate(years):
            if i < len(axes):
                ax = axes[i]
                year_data = grouped.loc[year]
                wedges, texts, autotexts = ax.pie(year_data, labels=categories, 
                                                autopct='%1.1f%%', colors=colors)
                ax.set_title(f"Year: {year}")
                
                # Add count labels
                total = sum(year_data)
                labels = [f'{cat}\n({int(val)} cases)' for cat, val in zip(categories, year_data)]
                ax.legend(wedges, labels, title="Categories", 
                         loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
                
        for j in range(len(years), len(axes)):
            fig.delaxes(axes[j])
            
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        st.pyplot(fig)

def main():
    st.title("Outlier Analysis with Charts by Year")
    
    uploaded_file = st.file_uploader("Upload your dataset (CSV/Excel):", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
                
            if not df.empty:
                st.write("### Preview of the dataset:")
                st.write(df.head())
                
                category_columns = [col for col in df.columns 
                                  if '_category' in col and 
                                  df[col].isin(['Outlier', 'Non-Outlier']).any()]
                
                if category_columns:
                    selected_column = st.selectbox("Select column for analysis:", 
                                                 category_columns)
                    chart_type = st.radio("Select chart type:", 
                                        ["Bar Chart", "Pie Chart"])
                    generate_outlier_charts(df, selected_column, chart_type)
                else:
                    st.write("No suitable category columns found.")
            else:
                st.write("No data to preview.")
                
        except Exception as e:
            st.error(f"Error processing data: {str(e)}")

if __name__ == '__main__':
    main()

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def detect_outliers_iqr(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    return Q1 - 1.5 * IQR, Q3 + 1.5 * IQR

def create_outlier_categories(df, winsorized_col):
    lower_bound, upper_bound = detect_outliers_iqr(df[winsorized_col])
    category_col = f'{winsorized_col}_category'
    df[category_col] = np.where(
        (df[winsorized_col] < lower_bound) | (df[winsorized_col] > upper_bound),
        'Outlier', 'Non-Outlier'
    )
    return df, category_col

def generate_charts(df, column, chart_type):
    grouped = df.groupby(['year', column]).size().unstack(fill_value=0)
    years = grouped.index.tolist()
    categories = grouped.columns.tolist()
    colors = {'Outlier': 'red', 'Non-Outlier': 'blue'}
    colors_list = [colors[cat] for cat in categories]
    
    fig = plt.figure(figsize=(15, 15))
    fig.suptitle(f"Outliers Detection After Winsorization Method\n", fontsize=16, y=0.98)
    
    legend_elements = [plt.Rectangle((0,0),1,1, facecolor=color) for color in colors_list]
    fig.legend(legend_elements, categories, 
              loc='upper center', bbox_to_anchor=(0.5, 0.93),
              ncol=len(categories), title="Categories")
    
    gs = fig.add_gridspec(3, 3, hspace=0.5, wspace=0.3)
    axes = [fig.add_subplot(gs[i//3, i%3]) for i in range(9)]
    
    for i, year in enumerate(years):
        if i < len(axes):
            ax = axes[i]
            year_data = grouped.loc[year]
            
            if chart_type == "Bar Chart":
                bars = ax.bar(categories, year_data, color=colors_list)
                ax.set_xlabel("Categories")
                ax.set_ylabel("Count", labelpad=10)
                ax.set_xticklabels(categories, rotation=45, ha='right')
                
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{int(height)}', ha='center', va='bottom')
            else:
                wedges, _, autotexts = ax.pie(year_data, colors=colors_list,
                                            autopct='%1.1f%%')
                
            ax.set_title(f"Year: {year}")
    
    for j in range(len(years), len(axes)):
        fig.delaxes(axes[j])
        
    plt.tight_layout(rect=[0, 0.03, 1, 0.90])
    return fig

def main():
    st.title("Outlier Analysis After Winsorization")
    
    uploaded_file = st.file_uploader("Upload dataset (CSV/Excel):", type=["csv", "xlsx"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            
            winsorized_cols = [col for col in df.columns if '_winsorized' in col]
            
            for col in winsorized_cols:
                st.markdown(f"### Analysis for {col}")
                
                df, category_col = create_outlier_categories(df, col)
                
                # Bar Chart
                fig_bar = generate_charts(df, category_col, "Bar Chart")
                st.pyplot(fig_bar)
                plt.close()
                
                # Pie Chart
                fig_pie = generate_charts(df, category_col, "Pie Chart")
                st.pyplot(fig_pie)
                plt.close()
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == '__main__':
    main()

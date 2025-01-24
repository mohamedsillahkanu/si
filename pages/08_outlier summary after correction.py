import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def detect_outliers_iqr(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    return Q1 - 1.5 * IQR, Q3 + 1.5 * IQR

def generate_charts(df, winsorized_col, chart_type):
    # Calculate bounds for winsorized column
    lower_bound, upper_bound = detect_outliers_iqr(df[winsorized_col])
    
    # Create category
    df[f'{winsorized_col}_category'] = np.where(
        (df[winsorized_col] < lower_bound) | (df[winsorized_col] > upper_bound),
        'Outlier', 'Non-Outlier'
    )
    
    grouped = df.groupby(['hf_uid', 'year', f'{winsorized_col}_category']).size().reset_index()
    grouped.columns = ['hf_uid', 'year', 'category', 'count']
    
    hf_uids = sorted(df['hf_uid'].unique())
    years = sorted(df['year'].unique())
    
    fig = plt.figure(figsize=(15, 15))
    fig.suptitle(f"Outliers After Winsorization - {winsorized_col}\n", fontsize=16, y=0.98)
    
    categories = ['Outlier', 'Non-Outlier']
    colors = {'Outlier': 'red', 'Non-Outlier': 'blue'}
    colors_list = [colors[cat] for cat in categories]
    
    legend_elements = [plt.Rectangle((0,0),1,1, facecolor=color) for color in colors_list]
    fig.legend(legend_elements, categories, 
              loc='upper center', bbox_to_anchor=(0.5, 0.93),
              ncol=len(categories), title="Categories")
    
    gs = fig.add_gridspec(3, 3, hspace=0.5, wspace=0.3)
    axes = [fig.add_subplot(gs[i//3, i%3]) for i in range(9)]
    
    plot_idx = 0
    for hf_uid in hf_uids:
        for year in years:
            if plot_idx < len(axes):
                hf_data = grouped[(grouped['hf_uid'] == hf_uid) & (grouped['year'] == year)]
                
                if not hf_data.empty:
                    ax = axes[plot_idx]
                    
                    if chart_type == "Bar Chart":
                        data = {cat: hf_data[hf_data['category'] == cat]['count'].iloc[0] 
                               if not hf_data[hf_data['category'] == cat].empty else 0 
                               for cat in categories}
                        
                        bars = ax.bar(categories, data.values(), color=colors_list)
                        
                        for bar in bars:
                            height = bar.get_height()
                            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                                   f'{int(height)}', ha='center', va='bottom')
                                   
                        ax.set_xlabel("Categories")
                        ax.set_ylabel("Count", labelpad=10)
                        ax.set_xticklabels(categories, rotation=45, ha='right')
                        
                    else:  # Pie Chart
                        data = [hf_data[hf_data['category'] == cat]['count'].iloc[0] 
                               if not hf_data[hf_data['category'] == cat].empty else 0 
                               for cat in categories]
                        
                        if sum(data) > 0:  # Only create pie if there's data
                            wedges, _, autotexts = ax.pie(data, colors=colors_list,
                                                        autopct='%1.1f%%')
                    
                    ax.set_title(f"HF: {hf_uid}, Year: {year}")
                    plot_idx += 1
    
    for j in range(plot_idx, len(axes)):
        fig.delaxes(axes[j])
        
    plt.tight_layout(rect=[0, 0.03, 1, 0.90])
    return fig

def main():
    st.title("Outlier Analysis on Winsorized Data")
    
    uploaded_file = st.file_uploader("Upload dataset (CSV/Excel):", type=["csv", "xlsx"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            
            winsorized_cols = [col for col in df.columns if '_winsorized' in col]
            selected_col = st.selectbox("Select variable:", winsorized_cols)
            
            st.markdown("### Bar Chart")
            fig_bar = generate_charts(df, selected_col, "Bar Chart")
            st.pyplot(fig_bar)
            plt.close()
            
            st.markdown("### Pie Chart")
            fig_pie = generate_charts(df, selected_col, "Pie Chart")
            st.pyplot(fig_pie)
            plt.close()
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == '__main__':
    main()

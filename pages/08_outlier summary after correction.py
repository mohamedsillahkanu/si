import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def check_outliers_after_winsorization(df, column_base):
    """Compare winsorized values with bounds and mark outliers"""
    df[f'{column_base}_winsorized_category'] = 'Non-Outlier'
    
    # Mark values above upper bound
    df.loc[df[f'{column_base}_winsorised'] > df[f'{column_base}_upper_bound'], 
           f'{column_base}_winsorized_category'] = 'Outlier'
    
    # Mark values below lower bound
    df.loc[df[f'{column_base}_winsorised'] < df[f'{column_base}_lower_bound'], 
           f'{column_base}_winsorized_category'] = 'Outlier'
    
    return df

def generate_outlier_charts(df, column, chart_type):
    if 'year' not in df.columns:
        st.error("Dataset must contain a 'year' column.")
        return
    
    column_base = column.replace('_winsorized_category', '')
    df = check_outliers_after_winsorization(df, column_base)
        
    grouped = df.groupby(['year', f'{column_base}_winsorized_category']).size().unstack(fill_value=0)
    years = grouped.index.tolist()
    categories = grouped.columns.tolist()
    
    colors = {'Outlier': 'red', 'Non-Outlier': 'blue'}
    colors_list = [colors[cat] for cat in categories]
    
    if chart_type == "Bar Chart":
        fig = plt.figure(figsize=(15, 15))
        
        fig.suptitle("Outliers Detection After Correction with Winsorized Method\n", fontsize=16, y=0.98)
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
                bars = ax.bar(categories, year_data, color=colors_list)
                ax.set_title(f"Year: {year}")
                ax.set_ylabel("Count", labelpad=10)
                ax.set_xlabel("Categories")
                ax.set_xticklabels(categories, rotation=45, ha='right')
                
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{int(height)}', ha='center', va='bottom')
                           
        for j in range(len(years), len(axes)):
            fig.delaxes(axes[j])
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.90])
        
    elif chart_type == "Pie Chart":
        fig = plt.figure(figsize=(15, 15))
        
        fig.suptitle("Outliers Detection After Correction with Winsorized Method\n", fontsize=16, y=0.98)
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
                wedges, _, autotexts = ax.pie(year_data, colors=colors_list,
                                            autopct='%1.1f%%')
                ax.set_title(f"Year: {year}")
                
        for j in range(len(years), len(axes)):
            fig.delaxes(axes[j])
            
        plt.tight_layout(rect=[0, 0.03, 1, 0.90])
    
    st.pyplot(fig)

def main():
    st.title("Outlier Analysis After Winsorization")
    uploaded_file = st.file_uploader("Upload dataset (CSV/Excel):", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
            
            if not df.empty:
                st.write("### Data Preview:")
                st.write(df.head())
                
                # Get columns that have winsorized values
                base_columns = [col.replace('_winsorised', '') 
                              for col in df.columns if '_winsorised' in col]
                
                if base_columns:
                    selected_column = st.selectbox("Select column:", base_columns)
                    chart_type = st.radio("Select chart type:", ["Bar Chart", "Pie Chart"])
                    
                    if st.button("Generate Analysis"):
                        generate_outlier_charts(df, selected_column, chart_type)
                else:
                    st.write("No winsorized columns found in dataset.")
            else:
                st.write("Empty dataset.")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == '__main__':
    main()

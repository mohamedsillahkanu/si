import streamlit as st
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to generate bar and pie charts for Outliers and Non-Outliers with sub-values by year
def generate_outlier_charts(df, column):
    # Group data by year and count the sub-values for Outliers and Non-Outliers
    if 'year' not in df.columns:
        st.write("The dataset must contain a 'year' column for this analysis.")
        return

    grouped = df.groupby('year')[column].value_counts().unstack(fill_value=0)
    years = grouped.index.tolist()
    categories = grouped.columns.tolist()

    # Define colors for the categories
    colors = ['lightgreen' if 'Outlier' in cat else 'lightblue' for cat in categories]

    # Create subplots
    fig, axes = plt.subplots(3, 3, figsize=(15, 15), sharex=True, sharey=True)
    fig.suptitle("Outliers and Non-Outliers Analysis by Year", fontsize=16)

    # Flatten axes for easier iteration
    axes = axes.flatten()

    for i, year in enumerate(years):
        if i < len(axes):
            ax = axes[i]
            year_data = grouped.loc[year]
            ax.bar(categories, year_data, color=colors)
            ax.set_title(f"Year: {year}")
            ax.set_ylabel("Count")
            ax.set_xlabel("Categories")
            ax.set_xticklabels(categories, rotation=45, ha='right')

    # Hide any unused subplots
    for j in range(len(years), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    st.pyplot(fig)

# Streamlit app setup
st.title("Outlier Analysis with Charts by Year")

uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel):", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    if df.empty:
        st.write("No data to preview.")
    else:
        st.write("### Preview of the uploaded dataset:")
        st.write(df.head())

        # Select columns with '_category' containing Outliers and Non-Outliers
        category_columns = [col for col in df.columns if '_category' in col and set(["Outlier", "Non-Outlier"]).intersection(set(df[col].dropna().unique()))]

        if category_columns:
            selected_column = st.selectbox("Select column for outlier analysis:", category_columns)
            generate_outlier_charts(df, selected_column)
        else:
            st.write("No columns with '_category' containing Outlier and Non-Outlier found in the dataset.")

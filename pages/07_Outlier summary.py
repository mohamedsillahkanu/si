import streamlit as st
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to generate bar and pie charts for Outliers and Non-Outliers with sub-values
def generate_outlier_charts(df, column):
    # Count the sub-values for Outliers and Non-Outliers
    grouped_counts = df[column].value_counts()

    # Extract counts for each category
    categories = grouped_counts.index.tolist()
    counts = grouped_counts.values.tolist()

    # Bar chart for Outliers and Non-Outliers with sub-values
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(categories, counts, color=['red' if 'Outliers' in cat else 'blue' for cat in categories])
    ax1.set_title("Outliers and Non-Outliers with Sub-Values")
    ax1.set_ylabel("Count")
    ax1.set_xlabel("Categories")
    ax1.set_xticklabels(categories, rotation=90, ha='right')
    st.pyplot(fig1)

    # Pie chart for Outliers and Non-Outliers with sub-values
    fig2, ax2 = plt.subplots()
    ax2.pie(counts, labels=categories, autopct="%1.1f%%", colors=['red' if 'Outliers' in cat else 'blue' for cat in categories])
    ax2.set_title("Proportion of Outliers and Non-Outliers with Sub-Values")
    st.pyplot(fig2)

# Streamlit app setup
st.title("Outlier Analysis with Charts")

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
        category_columns = [col for col in df.columns if '_category' in col and set(["Outliers", "Non-Outliers"]).intersection(set(df[col].dropna().unique()))]

        if category_columns:
            selected_column = st.selectbox("Select column for outlier analysis:", category_columns)
            generate_outlier_charts(df, selected_column)
        else:
            st.write("No columns with '_category' containing Outliers and Non-Outliers found in the dataset.")

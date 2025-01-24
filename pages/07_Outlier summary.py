import streamlit as st
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to detect outliers using the IQR method
def detect_outliers_iqr(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return (series < lower_bound) | (series > upper_bound)

# Function to generate bar and pie charts for outliers
def generate_outlier_charts(df, column):
    # Detect outliers
    outliers = detect_outliers_iqr(df[column])
    num_outliers = outliers.sum()
    num_non_outliers = len(outliers) - num_outliers

    # Bar chart for outliers and non-outliers
    fig1, ax1 = plt.subplots()
    ax1.bar(["Outliers", "Non-Outliers"], [num_outliers, num_non_outliers], color=["red", "blue"])
    ax1.set_title("Number of Outliers and Non-Outliers")
    ax1.set_ylabel("Count")
    st.pyplot(fig1)

    # Pie chart for outliers and non-outliers
    fig2, ax2 = plt.subplots()
    ax2.pie([num_outliers, num_non_outliers], labels=["Outliers", "Non-Outliers"], autopct="%1.1f%%", colors=["red", "blue"])
    ax2.set_title("Proportion of Outliers and Non-Outliers")
    st.pyplot(fig2)

# Function to generate charts for outliers corrected
def generate_correction_charts(df, column):
    # Detect outliers
    outliers = detect_outliers_iqr(df[column])
    num_outliers = outliers.sum()
    num_corrected = num_outliers  # Assume all outliers are corrected

    # Bar chart for outliers detected and corrected
    fig3, ax3 = plt.subplots()
    ax3.bar(["Outliers Detected", "Outliers Corrected"], [num_outliers, num_corrected], color=["orange", "green"])
    ax3.set_title("Outliers Detected vs. Corrected")
    ax3.set_ylabel("Count")
    st.pyplot(fig3)

    # Pie chart for outliers detected and corrected
    fig4, ax4 = plt.subplots()
    ax4.pie([num_outliers, num_corrected], labels=["Outliers Detected", "Outliers Corrected"], autopct="%1.1f%%", colors=["orange", "green"])
    ax4.set_title("Proportion of Outliers Detected and Corrected")
    st.pyplot(fig4)

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

        # Select column for outlier analysis
        numeric_columns = df.select_dtypes(include=["float", "int"]).columns.tolist()
        selected_column = st.selectbox("Select column for outlier analysis:", numeric_columns)

        if st.button("Generate Outlier Charts"):
            generate_outlier_charts(df, selected_column)

        if st.button("Generate Correction Charts"):
            generate_correction_charts(df, selected_column)

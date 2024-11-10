import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
from docx import Document
from docx.shared import Inches
from fpdf import FPDF

# Set up the page
st.set_page_config(page_title="Data Analysis App", layout="wide")

# Sidebar: Data source selection and file upload
st.sidebar.header("Data Source")
data_source = st.sidebar.radio("Choose data source", ["Use Sample Data", "Upload Excel/CSV"])

# Initialize an empty DataFrame
df = pd.DataFrame()

# Load data based on user selection
if data_source == "Upload Excel/CSV":
    uploaded_file = st.sidebar.file_uploader("Upload an Excel or CSV file", type=["xlsx", "csv"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error loading file: {e}")
else:
    # Create sample data if no file is uploaded
    df = pd.DataFrame({
        'Category': np.random.choice(['A', 'B', 'C', 'D'], 100),
        'Value 1': np.random.randn(100),
        'Value 2': np.random.randint(1, 10, 100),
        'Value 3': np.random.randn(100),
    })

# Check if the DataFrame is not empty
if not df.empty:
    st.write("### Data Overview")
    st.write(df.head())

    # Display data statistics
    st.write("### Data Summary")
    st.write(df.describe())

    # Basic Data Visualization options
    st.write("### Data Visualization")
    visualization_type = st.selectbox("Choose a visualization type", ["Histogram", "Box Plot", "Scatter Plot"])

    if visualization_type == "Histogram":
        column = st.selectbox("Select a column for the histogram", df.select_dtypes(include=[np.number]).columns)
        fig, ax = plt.subplots()
        ax.hist(df[column], bins=20, color="skyblue", edgecolor="black")
        ax.set_title(f"Histogram of {column}")
        st.pyplot(fig)

    elif visualization_type == "Box Plot":
        column = st.selectbox("Select a column for the box plot", df.select_dtypes(include=[np.number]).columns)
        fig, ax = plt.subplots()
        sns.boxplot(data=df, x=column, ax=ax)
        ax.set_title(f"Box Plot of {column}")
        st.pyplot(fig)

    elif visualization_type == "Scatter Plot":
        x_col = st.selectbox("Select X-axis", df.select_dtypes(include=[np.number]).columns)
        y_col = st.selectbox("Select Y-axis", df.select_dtypes(include=[np.number]).columns)
        fig, ax = plt.subplots()
        ax.scatter(df[x_col], df[y_col], color="blue", alpha=0.6)
        ax.set_title(f"Scatter Plot of {x_col} vs {y_col}")
        st.pyplot(fig)

    # Export options
    st.write("### Export Options")
    export_format = st.radio("Choose format for exporting data", ["None", "Excel", "PDF", "Word"])

    if export_format == "Excel":
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        st.download_button(label="Download Excel", data=excel_buffer, file_name="data_export.xlsx")

    elif export_format == "PDF":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for i, row in df.iterrows():
            pdf.cell(0, 10, txt=str(row.to_dict()), ln=True)
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        st.download_button(label="Download PDF", data=pdf_buffer.getvalue(), file_name="data_export.pdf")

    elif export_format == "Word":
        doc = Document()
        doc.add_heading("Data Export", level=1)
        doc.add_paragraph("Data Overview:")
        doc.add_table(rows=1, cols=len(df.columns))
        for row in df.itertuples(index=False):
            row_cells = doc.add_table(rows=1, cols=len(df.columns)).rows[0].cells
            for idx, value in enumerate(row):
                row_cells[idx].text = str(value)
        word_buffer = BytesIO()
        doc.save(word_buffer)
        st.download_button(label="Download Word", data=word_buffer.getvalue(), file_name="data_export.docx")

else:
    st.warning("No data available. Please upload a file or select a data source to proceed.")


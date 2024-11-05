import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import zipfile
from io import BytesIO
import re
from docx import Document
from docx.shared import Inches

# Sidebar for Data Management
st.sidebar.title("Data Management")
data_management_option = st.sidebar.radio(
    "Choose an option:",
    ["Outlier Detection and Correction"]
)

# Initialize session state variables
if 'df' not in st.session_state:
    st.session_state.df = None
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = None

# Function to filter dataframe based on categorical columns and their unique values
def filter_dataframe(df, categorical_columns, values):
    condition = pd.Series([True] * len(df))  # Initialize a condition with True values
    for col, val in zip(categorical_columns, values):
        condition &= (df[col].astype(str) == str(val))  # Convert to string for comparison
    return df[condition]

# Function to detect outliers using Scatterplot with Q1 and Q3 lines
def detect_outliers_scatterplot(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[col] < lower_bound) | (df[col] > upper_bound)], lower_bound, upper_bound

# Main App
st.title("Outlier Detection and Correction")

if data_management_option == "Outlier Detection and Correction":
    st.header("Select Columns for Outlier Detection")

    # Ensure dataset is uploaded before proceeding
    if st.session_state.df is None:
        st.warning("No dataset available. Please upload your dataset.")
        uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
        
        # Check for uploaded file
        if uploaded_file:
            try:
                # Read uploaded file and convert Year and Month columns to datetime format
                if uploaded_file.name.endswith(".csv"):
                    st.session_state.df = pd.read_csv(uploaded_file)
                else:
                    st.session_state.df = pd.read_excel(uploaded_file)

                # Check if required columns exist before proceeding
                if 'Year' not in st.session_state.df.columns or 'Month' not in st.session_state.df.columns:
                    st.error("The uploaded dataset must contain 'Year' and 'Month' columns.")
                    st.session_state.df = None  # Reset dataframe state
                else:
                    st.session_state.df['year_mon'] = pd.to_datetime(
                        st.session_state.df['Year'].astype(str) + '-' + st.session_state.df['Month'].astype(str),
                        format='%Y-%m'
                    )
                    st.success("Dataset uploaded successfully!")
                    st.dataframe(st.session_state.df)

            except Exception as e:
                st.error(f"Error processing the uploaded file: {str(e)}")
                st.session_state.df = None  # Reset dataframe state

    # Only proceed if dataframe is loaded successfully
    if st.session_state.df is not None:
        # User selects adm1, adm3, Year, Month, hf
        try:
            adm1 = st.selectbox("Select adm1:", st.session_state.df['adm1'].unique())
            adm3_options = st.session_state.df[st.session_state.df['adm1'] == adm1]['adm3'].unique()
            adm3 = st.selectbox("Select adm3:", adm3_options)
            Year_options = st.session_state.df[
                (st.session_state.df['adm1'] == adm1) &
                (st.session_state.df['adm3'] == adm3)
            ]['Year'].unique()
            Year = st.selectbox("Select Year:", Year_options)
            Month_options = st.session_state.df[
                (st.session_state.df['adm1'] == adm1) &
                (st.session_state.df['adm3'] == adm3) &
                (st.session_state.df['Year'] == Year)
            ]['Month'].unique()
            Months = st.multiselect("Select Month(s):", Month_options)
            hf_options = st.session_state.df[
                (st.session_state.df['adm1'] == adm1) &
                (st.session_state.df['adm3'] == adm3) &
                (st.session_state.df['Year'] == Year) &
                (st.session_state.df['Month'].isin(Months))
            ]['hf'].unique()
            hf = st.multiselect("Select hf:", hf_options)

            # Filter data based on selected values
            filtered_df = st.session_state.df[
                (st.session_state.df['adm1'] == adm1) &
                (st.session_state.df['adm3'] == adm3) &
                (st.session_state.df['Year'] == Year) &
                (st.session_state.df['Month'].isin(Months)) &
                (st.session_state.df['hf'].isin(hf))
            ]

            # User selects the numeric column for outlier detection and correction
            numeric_column = st.selectbox("Select a Numeric Column for Outlier Detection:", filtered_df.select_dtypes(include='number').columns)

            if numeric_column and not filtered_df.empty:
                st.write("Outliers will be detected and visualized for the selected categorical values.")

                if st.button("Generate Outlier Report"):
                    st.info("Generating outlier report...")
                    # Placeholder for the report generation process

            elif filtered_df.empty:
                st.warning("No data available after filtering. Please adjust your filter selections.")

        except KeyError as e:
            st.error(f"Missing required columns: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


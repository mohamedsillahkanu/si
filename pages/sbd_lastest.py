import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit App Title
st.title("📊 Excel Data Extraction & Visualization")

# Upload Excel File
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    # Read Excel File
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # Display Extracted Data
    st.subheader("📋 Extracted Data")
    st.dataframe(df)

    # Let User Select a Column for Visualization
    column_to_plot = st.selectbox("Select a column to visualize", df.columns)

    # Let User Select Chart Type
    chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart"])

    # Count Unique Values for the Selected Column
    value_counts = df[column_to_plot].value_counts()

    # Generate Chart
    fig, ax = plt.subplots(figsize=(6, 4))
    
    if chart_type == "Bar Chart":
        value_counts.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title(f"Bar Chart of {column_to_plot}")
        ax.set_ylabel("Count")
    else:
        value_counts.plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=90, colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"])
        ax.set_title(f"Pie Chart of {column_to_plot}")
        ax.set_ylabel("")  # Hide y-label for pie chart

    # Display Chart
    st.pyplot(fig)

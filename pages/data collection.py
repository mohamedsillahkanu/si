import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# Define the local Excel file
excel_file = "data.xlsx"

# Initialize the Excel file if it doesn't exist
if not os.path.exists(excel_file):
    pd.DataFrame(columns=["Name", "Age", "Gender", "Department", "Region"]).to_excel(excel_file, index=False)

# Set page configuration
st.set_page_config(page_title="Enhanced Dashboard App", page_icon="📊", layout="centered")

# Custom CSS for design
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #F0F8FF; /* Light blue background */
    }
    [data-testid="stSidebar"] {
        background-color: #D3E0FF; /* Sidebar matches main background */
    }
    .css-1d391kg p {
        font-size: 1.2rem; /* Larger font for text */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Tabs for navigation
tabs = st.tabs(["📋 Data Collection", "📊 Dashboard", "⬇️ Download Data"])

# 📋 Data Collection Tab
with tabs[0]:
    st.title("📋 Data Collection Form")
    st.write("Enter the details below to collect data.")

    # Form for data collection
    name = st.text_input("Name", placeholder="Enter your full name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1, format="%d")
    gender = st.radio("Gender", options=["Male", "Female", "Other"])
    department = st.selectbox("Department", options=["HR", "Finance", "IT", "Marketing", "Operations"])
    region = st.selectbox("Region", options=["North", "South", "East", "West", "Central"])

    if st.button("Submit Data"):
        if name:
            # Read existing data
            existing_data = pd.read_excel(excel_file)

            # Add new data
            new_data = pd.DataFrame({
                "Name": [name],
                "Age": [age],
                "Gender": [gender],
                "Department": [department],
                "Region": [region]
            })
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)

            # Save updated data
            updated_data.to_excel(excel_file, index=False)
            st.success("Data submitted successfully!")
        else:
            st.error("Please enter a name.")

# 📊 Dashboard Tab
with tabs[1]:
    st.title("📊 Data Dashboard")
    st.write("Visualize the collected data with interactive charts.")

    try:
        # Load data
        df = pd.read_excel(excel_file)

        # Create subplots
        fig, axs = plt.subplots(3, 2, figsize=(12, 15))

        # Chart 1: Gender Pie Chart
        gender_counts = df["Gender"].value_counts()
        axs[0, 0].pie(
            gender_counts,
            labels=gender_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#4CAF50", "#FFC107", "#2196F3"],
        )
        axs[0, 0].set_title("Gender Distribution")

        # Chart 2: Gender Bar Chart
        axs[0, 1].bar(gender_counts.index, gender_counts, color=["#4CAF50", "#FFC107", "#2196F3"])
        axs[0, 1].set_title("Gender Count")
        axs[0, 1].set_xlabel("Gender")
        axs[0, 1].set_ylabel("Count")

        # Chart 3: Department Pie Chart
        dept_counts = df["Department"].value_counts()
        axs[1, 0].pie(
            dept_counts,
            labels=dept_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#FF5733", "#33FF57", "#3357FF", "#FF33FF", "#FFC300"],
        )
        axs[1, 0].set_title("Department Distribution")

        # Chart 4: Department Bar Chart
        axs[1, 1].bar(dept_counts.index, dept_counts, color=["#FF5733", "#33FF57", "#3357FF", "#FF33FF", "#FFC300"])
        axs[1, 1].set_title("Department Count")
        axs[1, 1].set_xlabel("Department")
        axs[1, 1].set_ylabel("Count")

        # Chart 5: Region Pie Chart
        region_counts = df["Region"].value_counts()
        axs[2, 0].pie(
            region_counts,
            labels=region_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#E91E63", "#9C27B0", "#03A9F4", "#FF9800", "#8BC34A"],
        )
        axs[2, 0].set_title("Region Distribution")

        # Chart 6: Region Bar Chart
        axs[2, 1].bar(region_counts.index, region_counts, color=["#E91E63", "#9C27B0", "#03A9F4", "#FF9800", "#8BC34A"])
        axs[2, 1].set_title("Region Count")
        axs[2, 1].set_xlabel("Region")
        axs[2, 1].set_ylabel("Count")

        # Adjust layout
        plt.tight_layout()
        st.pyplot(fig)

    except Exception as e:
        st.info("No data available to display. Please submit data first.")

# ⬇️ Download Data Tab
with tabs[2]:
    st.title("⬇️ Download Collected Data")
    if os.path.exists(excel_file):
        with open(excel_file, "rb") as file:
            st.download_button(
                label="Download Data as Excel",
                data=file,
                file_name="collected_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    else:
        st.info("No data available for download.")

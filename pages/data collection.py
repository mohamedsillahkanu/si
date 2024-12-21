import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# Define the local Excel file
excel_file = "data.xlsx"

# Initialize the Excel file if it doesn't exist
if not os.path.exists(excel_file):
    pd.DataFrame(columns=["Name", "Age", "Gender"]).to_excel(excel_file, index=False)

# Set page configuration
st.set_page_config(page_title="Data Collection and Dashboard App", page_icon="📊", layout="centered")

# Custom CSS for a better design
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #F0F8FF; /* Light blue background */
    }
    [data-testid="stSidebar"] {
        background-color: #D3E0FF; /* Slightly darker sidebar */
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

    if st.button("Submit Data"):
        if name:
            # Read existing data
            existing_data = pd.read_excel(excel_file)

            # Add new data
            new_data = pd.DataFrame({"Name": [name], "Age": [age], "Gender": [gender]})
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

        # Display data summary
        st.subheader("Summary Statistics")
        st.write(df.describe(include="all"))

        # Gender distribution
        st.subheader("Gender Distribution")
        gender_counts = df["Gender"].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(
            gender_counts,
            labels=gender_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#4CAF50", "#FFC107", "#2196F3"],
        )
        ax1.axis("equal")  # Equal aspect ratio ensures a circular pie chart.
        st.pyplot(fig1)

        # Age distribution
        st.subheader("Age Distribution")
        fig2, ax2 = plt.subplots()
        ax2.hist(df["Age"], bins=10, color="#FF5733", edgecolor="black")
        ax2.set_title("Age Distribution")
        ax2.set_xlabel("Age")
        ax2.set_ylabel("Frequency")
        st.pyplot(fig2)

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

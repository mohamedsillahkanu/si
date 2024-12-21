import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(page_title="Offline Data Collection Form", layout="centered")

# Title and description
st.title("Data Collection Form")
st.write("Fill out the form below to submit your data.")

# Create input fields
name = st.text_input("Full Name", placeholder="Enter your name")
age = st.number_input("Age", min_value=0, max_value=120, step=1, format="%d")
gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
comments = st.text_area("Comments", placeholder="Enter your comments")

# Initialize a DataFrame
data_file = "collected_data.csv"
if not os.path.exists(data_file):
    pd.DataFrame(columns=["Name", "Age", "Gender", "Comments"]).to_csv(data_file, index=False)

# Submit button
if st.button("Submit"):
    # Validate inputs
    if not name:
        st.error("Name is required.")
    elif age == 0:
        st.error("Age must be greater than 0.")
    else:
        # Save the data to a CSV file
        new_data = pd.DataFrame({"Name": [name], "Age": [age], "Gender": [gender], "Comments": [comments]})
        existing_data = pd.read_csv(data_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data.to_csv(data_file, index=False)

        st.success("Data submitted successfully!")
        st.write("Thank you for your submission.")



st.title("📋 Data Collection Form")
st.write("📝 Fill out the form to submit your data.")

if st.checkbox("Show Collected Data"):
    df = pd.read_csv(data_file)
    st.dataframe(df)


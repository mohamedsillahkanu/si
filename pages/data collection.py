import streamlit as st
import pandas as pd
import os
from github import Github

# Define the Excel file
excel_file = "data.xlsx"

# GitHub credentials
GITHUB_TOKEN = "your_personal_access_token"
GITHUB_REPO = "username/repository_name"  # Replace with your GitHub repo
GITHUB_FILE_PATH = "data.xlsx"  # Path in the repository

# Initialize the Excel file if it doesn't exist
if not os.path.exists(excel_file):
    pd.DataFrame(columns=["Name", "Age", "Gender"]).to_excel(excel_file, index=False)

# Streamlit form for data collection
st.title("Data Collection Form")
name = st.text_input("Name")
age = st.number_input("Age", min_value=0, max_value=120, step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])

if st.button("Submit"):
    if name:
        # Append new data to the Excel file
        new_data = pd.DataFrame({"Name": [name], "Age": [age], "Gender": [gender]})
        existing_data = pd.read_excel(excel_file)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data.to_excel(excel_file, index=False)

        st.success("Data submitted successfully!")
    else:
        st.error("Please enter a name.")

# Push updated Excel file to GitHub
def push_to_github(file_path, repo_name, token, commit_message):
    """Pushes a file to a GitHub repository."""
    g = Github(token)
    repo = g.get_repo(repo_name)

    # Get the file from the repository
    try:
        contents = repo.get_contents(file_path)
        # Update the file
        with open(file_path, "rb") as file:
            repo.update_file(
                contents.path,
                commit_message,
                file.read(),
                contents.sha,
            )
    except:
        # Create the file if it doesn't exist
        with open(file_path, "rb") as file:
            repo.create_file(
                file_path,
                commit_message,
                file.read(),
            )

if st.button("Sync to GitHub"):
    try:
        push_to_github(excel_file, GITHUB_REPO, GITHUB_TOKEN, "Update data file")
        st.success("Data synced to GitHub successfully!")
    except Exception as e:
        st.error(f"Failed to sync data to GitHub: {e}")

if st.checkbox("Show Collected Data"):
    df = pd.read_excel(excel_file)
    st.dataframe(df)


import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load data from file
def load_data():
    try:
        data = pd.read_csv('user_data.csv')
    except FileNotFoundError:
        data = pd.DataFrame(columns=['Name', 'Age'])
    return data

# Function to save data to file
def save_data(data):
    data.to_csv('user_data.csv', index=False)

# Streamlit App
st.title("Automatic Dashboard with Streamlit")

# Sidebar with Data Entry Form
st.sidebar.header("Data Entry Form")

# Use st.text_input and st.number_input directly in the sidebar
name = st.sidebar.text_input("Enter Name:")
age = st.sidebar.number_input("Enter Age:", step=1, value=0)

submit_button = st.sidebar.button("Submit Data")
clear_button = st.sidebar.button("Clear")

# Clear the form
if clear_button:
    name = ""
    age = 0

# Load existing data
data_container = load_data()

# Add submitted data to the container
if submit_button:
    new_data = {"Name": name, "Age": int(age)}  # Ensure age is treated as a whole number
    data_container = pd.concat([data_container, pd.DataFrame([new_data])], ignore_index=True)
    save_data(data_container)

    # Clear the input fields after submitting data
    name = ""
    age = 0

# Display a table using Pandas in the sidebar
# Format the 'Age' column as integers
st.sidebar.table(data_container.style.format({"Age": "{:.0f}"}))

# Main section for Data Dashboard
st.header("Data Dashboard")

# Display an interactive bar chart for Name distribution using Plotly Express
if not data_container.empty:
    st.header("Name Distribution")

    # Calculate the sum of occurrences for each name
    name_counts = data_container['Name'].value_counts().reset_index()
    name_counts.columns = ['Name', 'Count']

    # Plot the bar chart using Plotly Express
    fig = px.bar(name_counts, x='Name', y='Count', title='Name Distribution')
    st.plotly_chart(fig)

import streamlit as st
import pandas as pd

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
age = st.sidebar.number_input("Enter Age:")
    
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
    new_data = {"Name": name, "Age": age}
    data_container = pd.concat([data_container, pd.DataFrame([new_data])], ignore_index=True)
    save_data(data_container)

    # Clear the input fields after submitting data
    name = ""
    age = 0

# Main section for Data Dashboard
st.header("Data Dashboard")

# Display a table using Pandas in the main section
st.dataframe(data_container)

# Display an interactive bar chart for Age distribution
if not data_container.empty:
    st.header("Age Distribution")
    age_counts = data_container['Age'].value_counts()
    st.bar_chart(age_counts)

# Display an interactive pie chart for Name distribution
if not data_container.empty:
    st.header("Name Distribution")
    name_counts = data_container['Name'].value_counts()
    st.pie_chart(name_counts)

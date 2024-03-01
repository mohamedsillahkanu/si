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

# Layout using columns
col1, col2 = st.columns([2, 3])

# Data Entry Form on the left
with col1:
    st.header("Data Entry Form")
    name = st.text_input("Enter Name:")
    age = st.number_input("Enter Age:")
    submit_button = st.button("Submit Data")
    clear_button = st.button("Clear")

# Load existing data
data_container = load_data()

# Add submitted data to the container
if submit_button:
    new_data = {"Name": name, "Age": age}
    data_container = pd.concat([data_container, pd.DataFrame([new_data])], ignore_index=True)
    save_data(data_container)

# Clear the form
if clear_button:
    name = ""
    age = 0

# Dashboard on the right
with col2:
    st.header("Data Dashboard")
    st.dataframe(data_container)

    # Display an interactive bar chart using Plotly Express
    if not data_container.empty:
        fig = px.bar(data_container, x='Name', y='Age', labels={'Age': 'Age'}, title='Age Distribution')
        st.plotly_chart(fig, use_container_width=True)

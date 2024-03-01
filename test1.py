#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Data container to store submitted data
data_container = []

# Streamlit App
st.title("Automatic Dashboard with Streamlit")

# Data Entry Form
st.header("Data Entry Form")

name = st.text_input("Enter Name:")
age = st.number_input("Enter Age:")
submit_button = st.button("Submit Data")

# Add submitted data to the container
if submit_button:
    data_container.append({"Name": name, "Age": age})

# Display the Data
st.header("Data Dashboard")

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(data_container)

# Display the DataFrame
st.dataframe(df)

# Display a bar chart
if not df.empty:
    fig, ax = plt.subplots()
    df.plot(kind='bar', x='Name', y='Age', ax=ax)
    ax.set_ylabel('Age')
    st.pyplot(fig)

# Other interactive elements can be added here based on your needs

# This line triggers a rerun of the script when data_container changes
st.experimental_rerun()

# To run the script: streamlit run your_script_name.py


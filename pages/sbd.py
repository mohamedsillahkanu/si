import streamlit as st
import pandas as pd
import os
import numpy as np
from PIL import Image
from pyzbar.pyzbar import decode
import cv2
import tempfile

# File to store data
data_file = 'data_collection.csv'

# Initialize data storage
if not os.path.exists(data_file):
    df = pd.DataFrame(columns=['Barcode', 'Name', 'Age', 'Gender'])
    df.to_csv(data_file, index=False)
else:
    df = pd.read_csv(data_file)

# Set up Streamlit app
st.title("Offline Data Collection App")
st.write("This is an offline data collection application. Please enter the required details below.")

# Barcode Scanning Function
def scan_barcode(uploaded_file):
    """Uses the uploaded image to scan a barcode."""
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    barcodes = decode(image_np)
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        return barcode_data
    return ""

# Barcode Input
uploaded_file = st.file_uploader("Upload an image to scan barcode", type=['jpg', 'jpeg', 'png'])
if uploaded_file is not None:
    barcode = scan_barcode(uploaded_file)
    if barcode:
        st.success(f"Scanned Barcode: {barcode}")
    else:
        st.error("No barcode detected. Please try again with a clearer image.")
else:
    barcode = st.text_input("Enter Barcode Manually:")

# User Input
name = st.text_input("Name:")
age = st.number_input("Age:", min_value=1, max_value=100, step=1)
gender = st.radio("Gender:", ('Male', 'Female', 'Other'))

# Check if barcode has already been scanned
if barcode:
    if barcode in df['Barcode'].values:
        st.error("This barcode has already been scanned. Please use a different barcode.")
    else:
        # Add data to DataFrame and save
        if st.button("Submit"):
            new_data = {'Barcode': barcode, 'Name': name, 'Age': age, 'Gender': gender}
            df = df.append(new_data, ignore_index=True)
            df.to_csv(data_file, index=False)
            st.success("Data successfully recorded.")

# Display the data collected so far
st.write("### Data Collected:")
st.dataframe(df)

# Distribution and Restriction
st.write("### Note:")
st.write("- This app is intended for offline use. Data is stored locally in a CSV file.")
st.write("- Each barcode can only be scanned once to avoid duplication.")

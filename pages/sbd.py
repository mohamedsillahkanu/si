import streamlit as st
import pandas as pd
import os
from streamlit.components.v1 import html
import cv2
import tempfile
import numpy as np
import base64

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
def scan_barcode():
    """Uses the device camera to scan a barcode."""
    cap = cv2.VideoCapture(0)
    barcode = None

    st.text("Opening camera...")
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to open camera.")
            break

        # Display the frame in Streamlit
        frame_placeholder = st.image(frame, channels="BGR")
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        # Attempt to detect barcode
        detector = cv2.QRCodeDetector()
        barcode, points, _ = detector.detectAndDecode(frame)
        if barcode:
            break

    cap.release()
    cv2.destroyAllWindows()

    if barcode:
        return barcode
    else:
        return ""

# Barcode Input
if st.button("Scan Barcode"):
    barcode = scan_barcode()
else:
    barcode = st.text_input("Enter or Scan Barcode:")

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

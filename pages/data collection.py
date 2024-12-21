import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Email configuration
SMTP_SERVER = "smtp.gmail.com"  # For Gmail. Use appropriate server for other email providers.
SMTP_PORT = 587
EMAIL_ADDRESS = "sillahmohamedkanu@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "mohamed1995"  # Replace with your email password
TO_EMAIL = "sillahkanuseries@gmail.com"  # Replace with recipient email

# Define local file
excel_file = "data.xlsx"

# Initialize the Excel file if it doesn't exist
if not os.path.exists(excel_file):
    pd.DataFrame(columns=["Name", "Age", "Gender"]).to_excel(excel_file, index=False)

# Streamlit UI
st.set_page_config(page_title="Data Sync App", page_icon="📧", layout="centered")
st.title("📧 Data Collection and Email Sync App")

# Tabs for navigation
tabs = st.tabs(["📋 Data Collection Form", "📊 View Data", "⬇️ Download File", "📤 Sync to Email"])

# 📋 Data Collection Form
with tabs[0]:
    st.header("📋 Submit Your Data")
    name = st.text_input("Enter Name", placeholder="Full Name")
    age = st.number_input("Enter Age", min_value=0, max_value=120, step=1, format="%d")
    gender = st.radio("Select Gender", options=["Male", "Female", "Other"])

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

# 📊 View Data
with tabs[1]:
    st.header("📊 Collected Data")
    try:
        df = pd.read_excel(excel_file)
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error reading data: {e}")

# ⬇️ Download File
with tabs[2]:
    st.header("⬇️ Download Collected Data")
    with open(excel_file, "rb") as file:
        st.download_button(
            label="Download Excel File",
            data=file,
            file_name="collected_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

# 📤 Sync to Email
with tabs[3]:
    st.header("📤 Sync Data to Email")
    if st.button("Send Email"):
        try:
            # Create the email
            msg = MIMEMultipart()
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = TO_EMAIL
            msg["Subject"] = "Collected Data - Excel File"

            body = "Please find attached the collected data."
            msg.attach(MIMEText(body, "plain"))

            # Attach the Excel file
            with open(excel_file, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(excel_file)}",
            )
            msg.attach(part)

            # Connect to the SMTP server and send the email
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
            server.quit()

            st.success("Email sent successfully!")
        except Exception as e:
            st.error(f"Failed to send email: {e}")

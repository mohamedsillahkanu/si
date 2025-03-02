import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit App
st.title("📊 Text Data Extraction & Visualization")

# Upload file
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

if uploaded_file:
    # Read the uploaded file
    content = uploaded_file.read().decode("utf-8")

    # Extract values using string operations
    data = {
        "District": content.split("District: ")[1].split("\n")[0] if "District:" in content else None,
        "Chiefdom": content.split("Chiefdom: ")[1].split("\n")[0] if "Chiefdom:" in content else None,
        "PHU Name": content.split("PHU name: ")[1].split("\n")[0] if "PHU name:" in content else None,
        "Community Name": content.split("Community name: ")[1].split("\n")[0] if "Community name:" in content else None,
        "School Name": content.split("Name of school: ")[1] if "Name of school:" in content else None
    }

    # Convert to DataFrame
    df = pd.DataFrame([data])

    # Display Extracted Data
    st.subheader("📋 Extracted Data")
    st.dataframe(df)

    # Visualization Selection
    chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart"])

    # Prepare Data for Visualization
    value_counts = df.T[0].value_counts()

    # Generate Charts
    fig, ax = plt.subplots(figsize=(6, 4))
    
    if chart_type == "Bar Chart":
        value_counts.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("Bar Chart of Extracted Data")
        ax.set_ylabel("Count")
    else:
        value_counts.plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=90, colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"])
        ax.set_title("Pie Chart of Extracted Data")
        ax.set_ylabel("")  # Hide y-label for pie chart

    # Display Chart
    st.pyplot(fig)

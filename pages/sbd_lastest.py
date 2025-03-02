import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# Streamlit App
st.title("📊 Text Data Extraction & Visualization")

# Upload file
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    # Read the uploaded Excel file
    df_original = pd.read_excel(uploaded_file)
    
    # Create empty lists to store extracted data
    districts = []
    chiefdoms = []
    phu_names = []
    community_names = []
    school_names = []
    
    # Process each row in the "Scan QR code" column
    for qr_text in df_original["Scan QR code"]:
        if pd.isna(qr_text):
            # Handle empty cells
            districts.append(None)
            chiefdoms.append(None)
            phu_names.append(None)
            community_names.append(None)
            school_names.append(None)
            continue
            
        # Extract values using regex patterns
        district_match = re.search(r"District:\s*([^\n]+)", str(qr_text))
        district = district_match.group(1).strip() if district_match else None
        districts.append(district)
        
        chiefdom_match = re.search(r"Chiefdom:\s*([^\n]+)", str(qr_text))
        chiefdom = chiefdom_match.group(1).strip() if chiefdom_match else None
        chiefdoms.append(chiefdom)
        
        phu_match = re.search(r"PHU name:\s*([^\n]+)", str(qr_text))
        phu_name = phu_match.group(1).strip() if phu_match else None
        phu_names.append(phu_name)
        
        community_match = re.search(r"Community name:\s*([^\n]+)", str(qr_text))
        community_name = community_match.group(1).strip() if community_match else None
        community_names.append(community_name)
        
        school_match = re.search(r"Name of school:\s*([^\n]+)", str(qr_text))
        school_name = school_match.group(1).strip() if school_match else None
        school_names.append(school_name)
    
    # Create a new DataFrame with extracted values
    extracted_df = pd.DataFrame({
        "District": districts,
        "Chiefdom": chiefdoms,
        "PHU Name": phu_names,
        "Community Name": community_names,
        "School Name": school_names
    })
    
    # Display Original Data Sample
    st.subheader("📄 Original Data Sample")
    st.dataframe(df_original.head())
    
    # Display Extracted Data
    st.subheader("📋 Extracted Data")
    st.dataframe(extracted_df)
    
    # Visualization of extracted data
    st.subheader("📊 Data Visualization")
    
    # Choose field to visualize
    field_to_visualize = st.selectbox(
        "Select Field to Visualize", 
        ["District", "Chiefdom", "PHU Name", "Community Name", "School Name"]
    )
    
    # Count values in the selected field
    value_counts = extracted_df[field_to_visualize].value_counts()
    
    # Visualization Selection
    chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart"])
    
    if not value_counts.empty:
        # Generate Charts
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if chart_type == "Bar Chart":
            value_counts.plot(kind="bar", ax=ax, color="skyblue")
            ax.set_title(f"Distribution of {field_to_visualize}")
            ax.set_ylabel("Count")
            plt.xticks(rotation=45, ha="right")
        else:
            # For pie chart, limit to top 10 values if there are many
            if len(value_counts) > 10:
                st.info(f"Showing top 10 of {len(value_counts)} unique values in pie chart")
                value_counts = value_counts.nlargest(10)
                
            value_counts.plot(
                kind="pie", 
                ax=ax, 
                autopct="%1.1f%%", 
                startangle=90,
                colors=plt.cm.tab20.colors
            )
            ax.set_title(f"Distribution of {field_to_visualize}")
            ax.set_ylabel("")
        
        plt.tight_layout()
        # Display Chart
        st.pyplot(fig)
    else:
        st.warning(f"No data available for {field_to_visualize}")

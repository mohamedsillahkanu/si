import streamlit as st
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt

# Streamlit App
st.title("📊 Text Data Extraction & Visualization")

# Upload file
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    # Read the uploaded Excel file
    df_original = pd.read_excel(uploaded_file)
    
    # Create empty lists to store extracted data
    districts, chiefdoms, phu_names, community_names, school_names = [], [], [], [], []
    
    # Process each row in the "Scan QR code" column
    for qr_text in df_original["Scan QR code"]:
        if pd.isna(qr_text):
            districts.append(None)
            chiefdoms.append(None)
            phu_names.append(None)
            community_names.append(None)
            school_names.append(None)
            continue
            
        # Extract values using regex patterns
        district_match = re.search(r"District:\s*([^\n]+)", str(qr_text))
        districts.append(district_match.group(1).strip() if district_match else None)
        
        chiefdom_match = re.search(r"Chiefdom:\s*([^\n]+)", str(qr_text))
        chiefdoms.append(chiefdom_match.group(1).strip() if chiefdom_match else None)
        
        phu_match = re.search(r"PHU name:\s*([^\n]+)", str(qr_text))
        phu_names.append(phu_match.group(1).strip() if phu_match else None)
        
        community_match = re.search(r"Community name:\s*([^\n]+)", str(qr_text))
        community_names.append(community_match.group(1).strip() if community_match else None)
        
        school_match = re.search(r"Name of school:\s*([^\n]+)", str(qr_text))
        school_names.append(school_match.group(1).strip() if school_match else None)
    
    # Create a new DataFrame with extracted values
    extracted_df = pd.DataFrame({
        "District": districts,
        "Chiefdom": chiefdoms,
        "PHU Name": phu_names,
        "Community Name": community_names,
        "School Name": school_names
    })
    
    # Add all other columns from the original DataFrame
    for column in df_original.columns:
        if column != "Scan QR code":  # Skip the QR code column since we've already processed it
            extracted_df[column] = df_original[column]
    
    # Display Original Data Sample
    st.subheader("📄 Original Data Sample")
    st.dataframe(df_original.head())
    
    # Display Extracted Data
    st.subheader("📋 Extracted Data")
    st.dataframe(extracted_df)
    
    # Visualization and filtering section
    st.subheader("🔍 Data Filtering and Visualization")
    
    # Create a sidebar for filtering options
    st.sidebar.header("Filter Options")
    
    # Create radio buttons to select which level to group by
    grouping_selection = st.sidebar.radio(
        "Select the level for grouping:",
        ["District", "Chiefdom", "PHU Name", "Community Name", "School Name"],
        index=0  # Default to 'District'
    )
    
    # Display the corresponding select boxes based on grouping selection
    if grouping_selection == "District":
        districts_filtered = sorted(extracted_df["District"].dropna().unique())
        selected_district = st.sidebar.selectbox("Select District", districts_filtered)
        # Filter data based on the selected district
        filtered_df = extracted_df[extracted_df["District"] == selected_district]
        # Further group by 'Chiefdom'
        chiefdoms_filtered = sorted(filtered_df["Chiefdom"].dropna().unique())
        selected_chiefdom = st.sidebar.selectbox("Select Chiefdom", chiefdoms_filtered)
        filtered_df = filtered_df[filtered_df["Chiefdom"] == selected_chiefdom]

    elif grouping_selection == "Chiefdom":
        chiefdoms_filtered = sorted(extracted_df["Chiefdom"].dropna().unique())
        selected_chiefdom = st.sidebar.selectbox("Select Chiefdom", chiefdoms_filtered)
        # Filter data based on selected chiefdom
        filtered_df = extracted_df[extracted_df["Chiefdom"] == selected_chiefdom]
        # Further group by 'District'
        districts_filtered = sorted(filtered_df["District"].dropna().unique())
        selected_district = st.sidebar.selectbox("Select District", districts_filtered)
        filtered_df = filtered_df[filtered_df["District"] == selected_district]
    
    elif grouping_selection == "PHU Name":
        phu_filtered = sorted(extracted_df["PHU Name"].dropna().unique())
        selected_phu = st.sidebar.selectbox("Select PHU Name", phu_filtered)
        filtered_df = extracted_df[extracted_df["PHU Name"] == selected_phu]
        # Further group by 'District' and 'Chiefdom'
        districts_filtered = sorted(filtered_df["District"].dropna().unique())
        selected_district = st.sidebar.selectbox("Select District", districts_filtered)
        filtered_df = filtered_df[filtered_df["District"] == selected_district]
        chiefdoms_filtered = sorted(filtered_df["Chiefdom"].dropna().unique())
        selected_chiefdom = st.sidebar.selectbox("Select Chiefdom", chiefdoms_filtered)
        filtered_df = filtered_df[filtered_df["Chiefdom"] == selected_chiefdom]
        
    elif grouping_selection == "Community Name":
        community_filtered = sorted(extracted_df["Community Name"].dropna().unique())
        selected_community = st.sidebar.selectbox("Select Community Name", community_filtered)
        filtered_df = extracted_df[extracted_df["Community Name"] == selected_community]
        # Further group by 'District', 'Chiefdom', and 'PHU Name'
        districts_filtered = sorted(filtered_df["District"].dropna().unique())
        selected_district = st.sidebar.selectbox("Select District", districts_filtered)
        filtered_df = filtered_df[filtered_df["District"] == selected_district]
        chiefdoms_filtered = sorted(filtered_df["Chiefdom"].dropna().unique())
        selected_chiefdom = st.sidebar.selectbox("Select Chiefdom", chiefdoms_filtered)
        filtered_df = filtered_df[filtered_df["Chiefdom"] == selected_chiefdom]
        phu_filtered = sorted(filtered_df["PHU Name"].dropna().unique())
        selected_phu = st.sidebar.selectbox("Select PHU Name", phu_filtered)
        filtered_df = filtered_df[filtered_df["PHU Name"] == selected_phu]

    elif grouping_selection == "School Name":
        school_filtered = sorted(extracted_df["School Name"].dropna().unique())
        selected_school = st.sidebar.selectbox("Select School Name", school_filtered)
        filtered_df = extracted_df[extracted_df["School Name"] == selected_school]
        # Further group by 'District', 'Chiefdom', 'PHU Name', and 'Community Name'
        districts_filtered = sorted(filtered_df["District"].dropna().unique())
        selected_district = st.sidebar.selectbox("Select District", districts_filtered)
        filtered_df = filtered_df[filtered_df["District"] == selected_district]
        chiefdoms_filtered = sorted(filtered_df["Chiefdom"].dropna().unique())
        selected_chiefdom = st.sidebar.selectbox("Select Chiefdom", chiefdoms_filtered)
        filtered_df = filtered_df[filtered_df["Chiefdom"] == selected_chiefdom]
        phu_filtered = sorted(filtered_df["PHU Name"].dropna().unique())
        selected_phu = st.sidebar.selectbox("Select PHU Name", phu_filtered)
        filtered_df = filtered_df[filtered_df["PHU Name"] == selected_phu]
        community_filtered = sorted(filtered_df["Community Name"].dropna().unique())
        selected_community = st.sidebar.selectbox("Select Community Name", community_filtered)
        filtered_df = filtered_df[filtered_df["Community Name"] == selected_community]

    # Check if data is available after filtering
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        st.write(f"### Filtered Data - {len(filtered_df)} records")
        st.dataframe(filtered_df)
        
        # Combine grouping columns into a single column for x-axis
        group_columns = ["District", "Chiefdom", "PHU Name", "Community Name", "School Name"][:len(filtered_df.columns) - 1]
        
        # Create a single column for x-axis by combining selected grouping columns
        filtered_df['Group'] = filtered_df[group_columns].apply(lambda row: ' | '.join(row.dropna().astype(str)), axis=1)
        
        # Group by the combined group column
        grouped_data = filtered_df.groupby("Group").agg({
            "ITN received": "sum",
            "ITN given": "sum"
        }).reset_index()

        # Create a bar chart
        fig, ax = plt.subplots(figsize=(12, 8))
        grouped_data.plot(kind="bar", x="Group", y=["ITN received", "ITN given"], ax=ax, color=["blue", "orange"])
        ax.set_title(f"📊 ITN Received vs. ITN Given by {' | '.join(group_columns)}")
        ax.set_xlabel("Group")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        # Summary Table
        st.subheader("📊 Summary Table")
        summary_df = grouped_data.copy()
        summary_df["Difference (ITN Received - ITN Given)"] = summary_df["ITN received"] - summary_df["ITN given"]
        st.dataframe(summary_df)

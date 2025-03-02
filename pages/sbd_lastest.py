import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

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

    # Copy all other columns from the original DataFrame
    for column in df_original.columns:
        if column != "Scan QR code":
            extracted_df[column] = df_original[column]
    
    # Display Original Data Sample
    st.subheader("📄 Original Data Sample")
    st.dataframe(df_original.head())
    
    # Display Extracted Data
    st.subheader("📋 Extracted Data")
    st.dataframe(extracted_df)
    
    # Visualization and filtering section
    st.subheader("🔍 Data Filtering and Visualization")
    
    # Sidebar filters
    st.sidebar.header("Filter Options")
    
    # Filter categories
    filter_categories = ["District", "Chiefdom", "PHU Name", "Community Name", "School Name"]
    filter_category = st.sidebar.selectbox("Filter by Category", filter_categories)
    
    # Check required columns
    required_columns = ["ITN received", "ITN given"]
    missing_columns = [col for col in required_columns if col not in extracted_df.columns]

    if missing_columns:
        st.warning(f"Missing required columns: {', '.join(missing_columns)}. Please ensure your data includes 'ITN received' and 'ITN given'.")
    else:
        # Apply filters
        filter_values = sorted(extracted_df[filter_category].dropna().unique().tolist())
        selected_filter_value = st.sidebar.selectbox(f"Select {filter_category}", filter_values)
        filtered_df = extracted_df[extracted_df[filter_category] == selected_filter_value]
        
        if filtered_df.empty:
            st.warning("No data available with the selected filters")
        else:
            st.write(f"### Filtered Data - {len(filtered_df)} records")
            st.dataframe(filtered_df)
            
            # Grouped bar chart
            st.subheader(f"📊 ITN Received vs. ITN Given for {filter_category}: {selected_filter_value}")

            # Determine grouping level
            hierarchy = {
                "District": "Chiefdom",
                "Chiefdom": "PHU Name",
                "PHU Name": "Community Name",
                "Community Name": "School Name"
            }
            group_by = hierarchy.get(filter_category, None)

            if group_by and group_by in filtered_df.columns:
                grouped_data = filtered_df.groupby(group_by).agg({
                    "ITN received": "sum",
                    "ITN given": "sum"
                }).reset_index()

                # Sort by ITN received
                grouped_data = grouped_data.sort_values("ITN received", ascending=False)

                # Adaptive figure height
                num_items = len(grouped_data)
                fig_height = max(6, 0.3 * num_items)

                # Create bar chart
                fig, ax = plt.subplots(figsize=(12, fig_height))
                x = np.arange(len(grouped_data))
                bar_width = 0.35

                ax.bar(x - bar_width/2, grouped_data["ITN received"], width=bar_width, label="ITN Received", color="skyblue")
                ax.bar(x + bar_width/2, grouped_data["ITN given"], width=bar_width, label="ITN Given", color="orange")

                # Labeling
                ax.set_xticks(x)
                ax.set_xticklabels(grouped_data[group_by], rotation=45, ha="right")
                ax.set_title(f"ITN Distribution by {group_by}")
                ax.set_ylabel("Count")
                ax.legend()

                # Display chart
                st.pyplot(fig)

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
    
    # Filter categories
    filter_categories = ["District", "Chiefdom", "PHU Name", "Community Name", "School Name"]
    
    # Create radio buttons for each grouping level
    grouping_selection = st.sidebar.radio(
        "Select the level for grouping:",
        filter_categories,
        index=0  # Default to 'District'
    )

    # Check if both required columns exist
    required_columns = ["ITN received", "ITN given"]
    missing_columns = [col for col in required_columns if col not in extracted_df.columns]
    
    if missing_columns:
        st.warning(f"Missing required columns: {', '.join(missing_columns)}. Please ensure your data includes both 'ITN received' and 'ITN given' columns.")
    else:
        # Apply filters based on selection
        filter_values = sorted(extracted_df[grouping_selection].dropna().unique().tolist())
        selected_filter_value = st.sidebar.selectbox(f"Select {grouping_selection}", filter_values)
        filtered_df = extracted_df[extracted_df[grouping_selection] == selected_filter_value]
        
        # Check if we have data after filtering
        if filtered_df.empty:
            st.warning("No data available with the selected filters")
        else:
            st.write(f"### Filtered Data - {len(filtered_df)} records")
            st.dataframe(filtered_df)
            
            # Define the grouping hierarchy
            grouping_hierarchy = {
                "District": ["District"],
                "Chiefdom": ["District", "Chiefdom"],
                "PHU Name": ["District", "Chiefdom", "PHU Name"],
                "Community Name": ["District", "Chiefdom", "PHU Name", "Community Name"],
                "School Name": ["District", "Chiefdom", "PHU Name", "Community Name", "School Name"]
            }

            # Determine the columns to group by based on the selected filter
            group_by_columns = grouping_hierarchy.get(grouping_selection, ["District"])

            # Perform the grouping
            grouped_data = filtered_df.groupby(group_by_columns).agg({
                "ITN received": "sum",
                "ITN given": "sum"
            }).reset_index()

            # Set x-axis labels based on the selected grouping level
            x_labels = grouped_data[group_by_columns].apply(lambda row: " | ".join(row.values.astype(str)), axis=1)

            # Sorting
            grouped_data = grouped_data.sort_values("ITN received", ascending=False)

            # Adjust figure height dynamically
            num_items = len(grouped_data)
            fig_height = max(8, 0.3 * num_items)

            # Create the bar chart
            fig, ax = plt.subplots(figsize=(14, fig_height))
            bar_width = 0.35
            x = np.arange(len(grouped_data))

            # Plot bars
            ax.bar(x - bar_width / 2, grouped_data["ITN received"], width=bar_width, label="ITN Received", color="blue")
            ax.bar(x + bar_width / 2, grouped_data["ITN given"], width=bar_width, label="ITN Given", color="orange")

            # Set labels and title
            ax.set_xlabel(grouping_selection)
            ax.set_ylabel("Count")
            ax.set_title(f"📊 ITN Received vs. ITN Given ({' | '.join(group_by_columns)})")
            ax.set_xticks(x)
            ax.set_xticklabels(x_labels, rotation=45, ha="right")

            # Add legend
            ax.legend()

            # Display the chart
            st.pyplot(fig)

            # Summary Table
            st.subheader("📊 Summary Table")
            summary_df = grouped_data.copy()
            summary_df["Difference (ITN Received - ITN Given)"] = summary_df["ITN received"] - summary_df["ITN given"]
            st.dataframe(summary_df)

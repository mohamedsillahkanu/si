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
    extracted_data = {
        "District": districts,
        "Chiefdom": chiefdoms,
        "PHU Name": phu_names,
        "Community Name": community_names,
        "School Name": school_names
    }
    
    # Add all other columns from the original DataFrame
    # First create the extracted DataFrame with the new columns
    extracted_df = pd.DataFrame(extracted_data)
    
    # Then copy all other columns from the original DataFrame
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
    filter_category = st.sidebar.selectbox("Filter by Category", filter_categories)
    
    # Check if both required columns exist
    required_columns = ["ITN received", "ITN given"]
    missing_columns = [col for col in required_columns if col not in extracted_df.columns]
    
    if missing_columns:
        st.warning(f"Missing required columns: {', '.join(missing_columns)}. Please ensure your data includes both 'ITN received' and 'ITN given' columns.")
    else:
        # Apply filters based on selection
        filter_values = sorted(extracted_df[filter_category].dropna().unique().tolist())
        selected_filter_value = st.sidebar.selectbox(f"Select {filter_category}", filter_values)
        filtered_df = extracted_df[extracted_df[filter_category] == selected_filter_value]
        
        # Check if we have data after filtering
        if filtered_df.empty:
            st.warning("No data available with the selected filters")
        else:
            st.write(f"### Filtered Data - {len(filtered_df)} records")
            st.dataframe(filtered_df)
            
            # Create grouped bar chart for ITN received and ITN given
            st.subheader(f"📊 ITN Received vs. ITN Given for {filter_category}: {selected_filter_value}")
            
            # Group data by the next level of hierarchy if available
            if filter_category == "District" and "Chiefdom" in filtered_df.columns:
                group_by = "Chiefdom"
            elif filter_category == "Chiefdom" and "PHU Name" in filtered_df.columns:
                group_by = "PHU Name"
            elif filter_category == "PHU Name" and "Community Name" in filtered_df.columns:
                group_by = "Community Name"
            elif filter_category == "Community Name" and "School Name" in filtered_df.columns:
                group_by = "School Name"
            else:
                # If no clear hierarchy, use the first available column that's not the filter category
                available_groups = [col for col in filter_categories if col != filter_category and col in filtered_df.columns]
                group_by = available_groups[0] if available_groups else "index"
            
            if group_by != "index":
                # Group by the selected column
                grouped_data = filtered_df.groupby(group_by).agg({
                    "ITN received": "sum",
                    "ITN given": "sum"
                }).reset_index()
                
                # Sort by ITN received in descending order
                grouped_data = grouped_data.sort_values("ITN received", ascending=False)
                
                # Determine if we need to adjust figure height based on number of items
                num_items = len(grouped_data)
                # Adjust figure height based on number of items (0.3 inches per item, minimum 8 inches)
                fig_height = max(8, 0.3 * num_items)
                
                # Create the visualization with adaptive height
                fig, ax = plt.subplots(figsize=(14, fig_height))
                
                # Set the width of the bars
                bar_width = 0.35
                
                # Set the positions of the bars on the x-axis
                x = np.arange(len(grouped_data))
                
                # Create the bars
                received_bars = ax.bar(x - bar_width/2, grouped_data["ITN received"], bar_width, 
                                        color="royalblue", label="ITN received")
                given_bars = ax.bar(x + bar_width/2, grouped_data["ITN given"], bar_width,
                                    color="lightcoral", label="ITN given")
                
                # Add count labels on top of each bar
                for i, bar in enumerate(received_bars):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                            f"{int(height)}", ha='center', va='bottom', fontsize=8)
                
                for i, bar in enumerate(given_bars):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                            f"{int(height)}", ha='center', va='bottom', fontsize=8)
                
                # Customize the chart
                ax.set_title(f"ITN Received vs. Given by {group_by} in {selected_filter_value}")
                ax.set_xlabel(group_by)
                ax.set_ylabel("Count")
                ax.set_xticks(x)
                
                # Adjust text size and rotation based on number of items
                if num_items > 30:
                    fontsize = 6
                elif num_items > 15:
                    fontsize = 8
                else:
                    fontsize = 10
                
                ax.set_xticklabels(grouped_data[group_by], rotation=90, ha="center", fontsize=fontsize)
                ax.legend()
                
                # Add grid lines for better readability
                ax.grid(axis='y', linestyle='--', alpha=0.7)
                
                # Adjust layout
                plt.tight_layout()
                st.pyplot(fig)
                
                # Show a table with the data
                st.write(f"#### Data Table - ITN Metrics by {group_by}")
                st.dataframe(grouped_data)
                
                # Calculate and show totals and percentages
                total_received = grouped_data["ITN received"].sum()
                total_given = grouped_data["ITN given"].sum()
                
                st.write("#### Summary")
                summary_data = {
                    "Metric": ["Total ITN Received", "Total ITN Given", "Utilization Rate (%)"],
                    "Value": [
                        f"{int(total_received):,}",
                        f"{int(total_given):,}",
                        f"{(total_given / total_received * 100) if total_received > 0 else 0:.2f}%"
                    ]
                }
                st.dataframe(pd.DataFrame(summary_data))
            else:
                st.warning(f"No suitable grouping column found for {filter_category}: {selected_filter_value}")

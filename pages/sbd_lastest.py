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
    
    # Find all columns for visualization (both numeric and categorical)
    columns_for_viz = [col for col in extracted_df.columns if col not in filter_categories]
    
    if not columns_for_viz:
        st.warning("No columns found for visualization")
    else:
        # Select which column to visualize
        selected_column = st.sidebar.selectbox("Select Column for Visualization", columns_for_viz)
        
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
            
            # Create visualization
            st.subheader(f"📊 Count of {selected_column} for {filter_category}: {selected_filter_value}")
            
            # Get counts based on the selected column
            if pd.api.types.is_numeric_dtypes(filtered_df[selected_column]):
                # For numeric columns, create bins
                counts = pd.cut(filtered_df[selected_column], bins=10).value_counts().sort_index()
                
                # Create the visualization
                fig, ax = plt.subplots(figsize=(12, 8))
                counts.plot(kind="bar", ax=ax, color="skyblue")
                ax.set_title(f"Distribution of {selected_column} for {filter_category}: {selected_filter_value}")
                ax.set_ylabel("Count")
                ax.set_xlabel(selected_column)
                
                # Add count labels on top of each bar
                for i, count in enumerate(counts):
                    ax.text(i, count + 0.1, str(count), ha='center')
                    
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                st.pyplot(fig)
            else:
                # For categorical columns
                counts = filtered_df[selected_column].value_counts().sort_values(ascending=False)
                
                # Limit to top 20 values if there are too many
                if len(counts) > 20:
                    st.info(f"Showing top 20 of {len(counts)} values")
                    counts = counts.nlargest(20)
                
                # Create the visualization
                fig, ax = plt.subplots(figsize=(12, 8))
                counts.plot(kind="bar", ax=ax, color="skyblue")
                ax.set_title(f"Count of {selected_column} for {filter_category}: {selected_filter_value}")
                ax.set_ylabel("Count")
                ax.set_xlabel(selected_column)
                
                # Add count labels on top of each bar
                for i, count in enumerate(counts):
                    ax.text(i, count + 0.1, str(count), ha='center')
                    
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                st.pyplot(fig)
                
            # Show a table with the count data
            st.write(f"#### Data Table - Counts for {selected_column}")
            if pd.api.types.is_numeric_dtypes(filtered_df[selected_column]):
                st.dataframe(counts.reset_index().rename(columns={0: "Count"}))
            else:
                st.dataframe(counts.reset_index().rename(columns={"index": selected_column, selected_column: "Count"}))

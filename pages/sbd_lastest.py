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
    filter_categories = ["All", "District", "Chiefdom", "PHU Name", "Community Name", "School Name"]
    filter_category = st.sidebar.selectbox("Filter by Category", filter_categories)
    
    # Find numeric columns for visualization
    numeric_columns = extracted_df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_columns:
        st.warning("No numeric columns found for visualization")
    else:
        # Select which numeric column to visualize
        numeric_column = st.sidebar.selectbox("Select Numeric Column for Visualization", numeric_columns)
        
        filtered_df = extracted_df.copy()
        
        # Apply filters based on selection
        if filter_category != "All":
            filter_values = sorted(extracted_df[filter_category].dropna().unique().tolist())
            selected_filter_value = st.sidebar.selectbox(f"Select {filter_category}", filter_values)
            filtered_df = extracted_df[extracted_df[filter_category] == selected_filter_value]
        
        # Check if we have data after filtering
        if filtered_df.empty:
            st.warning("No data available with the selected filters")
        else:
            st.write(f"### Filtered Data - {len(filtered_df)} records")
            st.dataframe(filtered_df)
            
            # Visualization based on selected filter and numeric column
            st.subheader(f"📊 Visualization of {numeric_column} by {filter_category}")
            
            if filter_category == "All":
                # Summary stats for the entire dataset
                avg_value = filtered_df[numeric_column].mean()
                st.write(f"Average {numeric_column}: {avg_value:.2f}")
                
                # Show distribution of the numeric column
                fig, ax = plt.subplots(figsize=(10, 6))
                filtered_df[numeric_column].hist(ax=ax, bins=20, color="skyblue", edgecolor="black")
                ax.set_title(f"Distribution of {numeric_column}")
                ax.set_xlabel(numeric_column)
                ax.set_ylabel("Frequency")
                st.pyplot(fig)
            else:
                # Group by the selected category
                grouped_data = filtered_df.groupby(filter_category)[numeric_column].mean().sort_values(ascending=False)
                
                # Check if we have data to visualize
                if grouped_data.empty:
                    st.warning(f"No data available for {filter_category} with values in {numeric_column}")
                else:
                    # Limit to top 20 values if there are too many
                    if len(grouped_data) > 20:
                        st.info(f"Showing top 20 of {len(grouped_data)} values")
                        grouped_data = grouped_data.nlargest(20)
                    
                    # Create the visualization
                    fig, ax = plt.subplots(figsize=(12, 8))
                    grouped_data.plot(kind="bar", ax=ax, color="skyblue")
                    ax.set_title(f"Average {numeric_column} by {filter_category}")
                    ax.set_ylabel(f"Average {numeric_column}")
                    ax.set_xlabel(filter_category)
                    plt.xticks(rotation=45, ha="right")
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Show a table with the data
                    st.write(f"#### Data Table - Average {numeric_column} by {filter_category}")
                    st.dataframe(grouped_data.reset_index())
                    
                    # Show additional statistics
                    st.write("#### Summary Statistics")
                    count_data = filtered_df.groupby(filter_category)[numeric_column].count()
                    summary_df = pd.DataFrame({
                        f"Average {numeric_column}": grouped_data,
                        "Count": count_data,
                        f"Min {numeric_column}": filtered_df.groupby(filter_category)[numeric_column].min(),
                        f"Max {numeric_column}": filtered_df.groupby(filter_category)[numeric_column].max()
                    }).reset_index()
                    st.dataframe(summary_df)

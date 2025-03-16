import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import tempfile
from matplotlib.colors import ListedColormap

# Page configuration
st.set_page_config(
    page_title="Criteria Map",
    page_icon="🗺️",
    layout="wide"
)

# App title
st.title("Multiple Criteria Map")
st.markdown("Areas meeting all criteria will be highlighted in gold, others in white")

# Function to handle shapefile components (without PRJ)
def process_shapefile_components(shp_file, shx_file, dbf_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save each component to the temp directory
        shp_path = os.path.join(temp_dir, "temp.shp")
        shx_path = os.path.join(temp_dir, "temp.shx")
        dbf_path = os.path.join(temp_dir, "temp.dbf")
        
        with open(shp_path, 'wb') as f:
            f.write(shp_file.read())
        
        with open(shx_path, 'wb') as f:
            f.write(shx_file.read())
        
        with open(dbf_path, 'wb') as f:
            f.write(dbf_file.read())
        
        # Read the shapefile
        gdf = gpd.read_file(shp_path)
        return gdf

# File uploaders for data
st.subheader("Upload Excel Data")
excel_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])

# File uploaders for shapefile components (only SHP, SHX, DBF)
st.subheader("Upload Shapefile Components")
col1, col2, col3 = st.columns(3)

with col1:
    shp_file = st.file_uploader("Upload .shp file", type=['shp'])

with col2:
    shx_file = st.file_uploader("Upload .shx file", type=['shx'])

with col3:
    dbf_file = st.file_uploader("Upload .dbf file", type=['dbf'])

# Process the uploaded files
if excel_file is not None:
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)
        st.success("Excel file successfully loaded!")
        
        # Preview the data
        st.subheader("Data Preview")
        st.dataframe(df.head(), use_container_width=True)
        
        # Process shapefile components if uploaded
        gdf = None
        if shp_file is not None and shx_file is not None and dbf_file is not None:
            try:
                gdf = process_shapefile_components(shp_file, shx_file, dbf_file)
                
                if gdf is not None:
                    st.success("Shapefile components successfully loaded!")
                    
                    # Preview the shapefile data
                    st.subheader("Shapefile Preview")
                    st.dataframe(gdf.head(), use_container_width=True)
                    
                    # Perform join between data and shapefile
                    try:
                        # Use the specified merge parameters
                        merged_gdf = gdf.merge(
                            df, 
                            how='left',
                            on=['FIRST_DNAM', 'FIRST'],
                            validate='1:1'
                        )
                        
                        # Check if merge was successful
                        if len(merged_gdf) > 0:
                            st.success(f"Successfully joined data with shapefile. {len(merged_gdf)} records in result.")
                            
                            # Set up multiple criteria
                            st.sidebar.subheader("Define Criteria")
                            
                            # Get all columns from the data
                            all_columns = merged_gdf.columns.tolist()
                            all_columns = [col for col in all_columns if col not in ['geometry']]
                            
                            # Container for criteria
                            criteria_list = []
                            
                            # Allow user to add multiple criteria
                            num_criteria = st.sidebar.number_input("Number of criteria:", min_value=1, max_value=5, value=1)
                            
                            for i in range(num_criteria):
                                st.sidebar.markdown(f"**Criterion {i+1}**")
                                
                                # Select column
                                col = st.sidebar.selectbox(
                                    f"Column {i+1}:",
                                    options=all_columns,
                                    key=f"col_{i}"
                                )
                                
                                # Check if column is numeric or categorical
                                if pd.api.types.is_numeric_dtype(merged_gdf[col]):
                                    # Numeric column
                                    op = st.sidebar.selectbox(
                                        f"Operator {i+1}:",
                                        options=["==", ">", "<", ">=", "<=", "!="],
                                        key=f"op_{i}"
                                    )
                                    
                                    # Get min and max values for the column
                                    min_val = float(merged_gdf[col].min())
                                    max_val = float(merged_gdf[col].max())
                                    
                                    # Value input
                                    val = st.sidebar.slider(
                                        f"Value {i+1}:",
                                        min_value=min_val,
                                        max_value=max_val,
                                        value=(max_val + min_val) / 2,
                                        key=f"val_{i}"
                                    )
                                    
                                else:
                                    # Categorical column
                                    op = "=="  # For categorical, we only use equals
                                    
                                    # Get unique values
                                    unique_vals = merged_gdf[col].dropna().unique().tolist()
                                    
                                    # Value selection
                                    val = st.sidebar.selectbox(
                                        f"Value {i+1}:",
                                        options=unique_vals,
                                        key=f"val_{i}"
                                    )
                                
                                # Add criterion to list
                                criteria_list.append((col, op, val))
                            
                            # Create description of all criteria
                            criteria_descriptions = []
                            for col, op, val in criteria_list:
                                criteria_descriptions.append(f"{col} {op} {val}")
                            
                            criteria_text = " AND ".join(criteria_descriptions)
                            
                            # Apply all criteria to create the condition
                            merged_gdf['condition_met'] = True  # Start with all True
                            
                            for col, op, val in criteria_list:
                                if op == "==":
                                    merged_gdf['condition_met'] = merged_gdf['condition_met'] & (merged_gdf[col] == val)
                                elif op == ">":
                                    merged_gdf['condition_met'] = merged_gdf['condition_met'] & (merged_gdf[col] > val)
                                elif op == "<":
                                    merged_gdf['condition_met'] = merged_gdf['condition_met'] & (merged_gdf[col] < val)
                                elif op == ">=":
                                    merged_gdf['condition_met'] = merged_gdf['condition_met'] & (merged_gdf[col] >= val)
                                elif op == "<=":
                                    merged_gdf['condition_met'] = merged_gdf['condition_met'] & (merged_gdf[col] <= val)
                                elif op == "!=":
                                    merged_gdf['condition_met'] = merged_gdf['condition_met'] & (merged_gdf[col] != val)
                            
                            # Count areas meeting the condition
                            met_count = merged_gdf['condition_met'].sum()
                            total_areas = len(merged_gdf)
                            
                            # Display condition information
                            st.subheader(f"Criteria: {criteria_text}")
                            st.write(f"{met_count} out of {total_areas} areas meet the criteria ({met_count/total_areas:.1%})")
                            
                            # Create a static map
                            st.subheader("Binary Criteria Map")
                            
                            # Set the figure size
                            fig, ax = plt.subplots(1, 1, figsize=(12, 8))
                            
                            # Create a binary colormap (white for False, gold for True)
                            binary_cmap = ListedColormap(['white', 'gold'])
                            
                            # Plot the map
                            merged_gdf.plot(
                                column='condition_met',
                                cmap=binary_cmap,
                                ax=ax,
                                legend=False,
                                edgecolor='black'
                            )
                            
                            # Remove axes
                            ax.set_axis_off()
                            
                            # Add a title with the criteria
                            plt.title(f"Areas meeting criteria: {criteria_text}", fontsize=12)
                            
                            # Add a custom legend with specified text
                            from matplotlib.patches import Patch
                            legend_elements = [
                                Patch(facecolor='gold', edgecolor='black', label='Criteria Met'),
                                Patch(facecolor='white', edgecolor='black', label='Criteria Not Met')
                            ]
                            ax.legend(handles=legend_elements, loc='lower right')
                            
                            # Display the map
                            st.pyplot(fig)
                            
                            # Display data table with condition results
                            st.subheader("Areas Meeting the Criteria")
                            condition_met_df = merged_gdf[merged_gdf['condition_met'] == True].drop(columns=['geometry', 'condition_met'])
                            if len(condition_met_df) > 0:
                                st.dataframe(condition_met_df, use_container_width=True)
                            else:
                                st.info("No areas meet the specified criteria.")
                            
                        else:
                            st.warning("No data in merged result. Please check your join columns.")
                    except Exception as e:
                        st.error(f"Error joining data with shapefile: {str(e)}")
                        st.info("Check if the specified columns 'FIRST_DNAM' and 'FIRST' exist in both datasets.")
                
            except Exception as e:
                st.error(f"Error processing shapefile components: {str(e)}")
        
    except Exception as e:
        st.error(f"Error processing Excel file: {str(e)}")

else:
    # Show instructions when no files are uploaded
    st.info("Please upload your Excel data file and shapefile components to begin.")
    
    # Add example of expected data format
    st.subheader("Expected Data Format")
    
    st.markdown("""
        Your Excel file should contain:
        - Data with geographic identifiers (region codes, country names, etc.)
        - Columns with values to use in your criteria (both categorical and numeric)
        
        The shapefile components should include:
        - .shp file (shape format containing the geometry)
        - .shx file (shape index format)
        - .dbf file (attribute format)
        
        Note: The application will merge your Excel data with the shapefile using 'FIRST_DNAM' and 'FIRST' columns.
    """)

# Add footer
st.markdown("---")
st.caption("Binary Criteria Map | Gold areas meet all your specified criteria")

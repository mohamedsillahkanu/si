import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import io
import tempfile
import os

st.set_page_config(page_title="Simple GeoAnalysis Tool", layout="wide")

# Initialize session state variables
if 'data' not in st.session_state:
    st.session_state.data = None
if 'shapefile' not in st.session_state:
    st.session_state.shapefile = None
if 'merged_data' not in st.session_state:
    st.session_state.merged_data = None
if 'map_image' not in st.session_state:
    st.session_state.map_image = None

# Helper function to save uploaded file
def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name

# Create a simple map
def create_map(gdf, category_column, colors, title="", legend_title=""):
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    
    # Calculate category counts for legend
    category_counts = gdf[category_column].value_counts()
    
    # Plot the map
    gdf.plot(ax=ax, color=gdf[category_column].map(colors))
    
    # Add borders
    gdf.boundary.plot(color='gray', linewidth=0.5, ax=ax)
    
    # District boundaries if FIRST_DNAM exists
    if 'FIRST_DNAM' in gdf.columns:
        district_boundaries = gdf.dissolve(by='FIRST_DNAM')
        district_boundaries.boundary.plot(
            ax=ax, color='black', linewidth=1.0, zorder=2
        )
    
    # Add legend with counts
    legend_elements = []
    for key in colors.keys():
        if key in category_counts:
            patch = Patch(
                facecolor=colors[key],
                edgecolor='black',
                linewidth=1,
                label=f"{key} ({category_counts.get(key, 0)})"
            )
            legend_elements.append(patch)
    
    ax.legend(
        handles=legend_elements,
        title=legend_title,
        loc='center left',
        bbox_to_anchor=(1, 0.5),
        fontsize=10,
        frameon=True,
        edgecolor='black',
        facecolor='white'
    )
    
    # Remove axes
    ax.axis('off')
    
    # Add title
    plt.title(title, pad=10, fontsize=14, fontweight='bold')
    plt.tight_layout(pad=0.5)
    
    return fig

# App title
st.title("Simple Geospatial Analysis Tool")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Data Upload", "Data Processing", "Create Map", "Export"])

# Tab 1: Data Upload
with tab1:
    st.header("Upload Your Data")
    
    # Data upload
    data_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "xls", "csv"])
    
    if data_file:
        try:
            if data_file.name.endswith('.csv'):
                df = pd.read_csv(data_file)
            else:
                df = pd.read_excel(data_file)
            
            st.session_state.data = df
            st.success(f"Successfully loaded data with {len(df)} rows and {len(df.columns)} columns.")
            st.write("Data Preview:")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Error loading data file: {e}")
    
    # Shapefile upload
    shapefile = st.file_uploader(
        "Upload shapefile components (.shp, .shx, .dbf)",
        type=["shp", "shx", "dbf", "prj"],
        accept_multiple_files=True
    )
    
    if shapefile:
        required_extensions = ['.shp', '.shx', '.dbf']
        uploaded_extensions = [os.path.splitext(file.name)[1].lower() for file in shapefile]
        
        if all(ext in uploaded_extensions for ext in required_extensions):
            temp_dir = tempfile.mkdtemp()
            
            # Save all components
            for file in shapefile:
                file_path = os.path.join(temp_dir, file.name)
                with open(file_path, 'wb') as f:
                    f.write(file.getvalue())
            
            # Find the .shp file
            shp_file = next(f for f in shapefile if f.name.endswith('.shp'))
            shp_path = os.path.join(temp_dir, shp_file.name)
            
            # Read the shapefile
            try:
                gdf = gpd.read_file(shp_path)
                st.session_state.shapefile = gdf
                st.success(f"Successfully loaded shapefile with {len(gdf)} features.")
                st.write("Shapefile Preview:")
                st.dataframe(gdf.head())
            except Exception as e:
                st.error(f"Error loading shapefile: {e}")
        else:
            st.warning("Please upload all required shapefile components (.shp, .shx, .dbf)")

# Tab 2: Data Processing
with tab2:
    st.header("Process Your Data")
    
    if st.session_state.data is None or st.session_state.shapefile is None:
        st.info("Please upload both data file and shapefile in the Data Upload tab.")
    else:
        df = st.session_state.data
        gdf = st.session_state.shapefile
        
        # Clean string columns
        st.subheader("Clean String Columns")
        
        string_columns = df.select_dtypes(include=['object']).columns.tolist()
        columns_to_clean = st.multiselect(
            "Select string columns to clean (strip whitespace):",
            string_columns
        )
        
        if columns_to_clean and st.button("Clean Selected Columns"):
            for col in columns_to_clean:
                df[col] = df[col].astype(str).str.strip()
            st.session_state.data = df
            st.success(f"Cleaned {len(columns_to_clean)} columns.")
        
        # String columns in shapefile
        shapefile_string_columns = gdf.select_dtypes(include=['object']).columns.tolist()
        shapefile_string_columns = [col for col in shapefile_string_columns if col != 'geometry']
        
        shapefile_columns_to_clean = st.multiselect(
            "Select shapefile string columns to clean:",
            shapefile_string_columns
        )
        
        if shapefile_columns_to_clean and st.button("Clean Shapefile Columns"):
            for col in shapefile_columns_to_clean:
                gdf[col] = gdf[col].astype(str).str.strip()
            st.session_state.shapefile = gdf
            st.success(f"Cleaned {len(shapefile_columns_to_clean)} shapefile columns.")
        
        # Merge datasets
        st.subheader("Merge Data with Shapefile")
        
        # Find common columns
        common_columns = list(set(df.columns) & set(gdf.columns))
        
        if common_columns:
            st.write(f"Found {len(common_columns)} common columns: {', '.join(common_columns)}")
            st.info("Will use common columns with left join and validate='1:1'")
            
            if st.button("Merge Data"):
                try:
                    merged_gdf = gdf.merge(
                        df,
                        on=common_columns,
                        how='left',
                        validate="1:1"
                    )
                    
                    st.session_state.merged_data = merged_gdf
                    st.success(f"Successfully merged data. Result has {len(merged_gdf)} features.")
                    st.write("Merged Data Preview:")
                    st.dataframe(merged_gdf.head())
                except Exception as e:
                    st.error(f"Error merging data: {e}")
        else:
            st.warning("No common columns found between data and shapefile.")
        
        # Create calculated fields if data is merged
        if st.session_state.merged_data is not None:
            st.subheader("Create Calculated Fields")
            
            merged_gdf = st.session_state.merged_data
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                new_column_name = st.text_input("New column name:")
                column1 = st.selectbox("First column:", [c for c in merged_gdf.columns if c != 'geometry'])
            
            with col2:
                operation = st.selectbox("Operation:", ["divide", "multiply", "add", "subtract"])
                
            with col3:
                column2 = st.selectbox("Second column:", [c for c in merged_gdf.columns if c != 'geometry'])
                scaling = st.number_input("Scaling factor (e.g., 1000):", value=1.0)
            
            if st.button("Calculate Field") and new_column_name and column1 and column2:
                try:
                    # Convert columns to numeric if needed
                    merged_gdf[column1] = pd.to_numeric(merged_gdf[column1], errors='coerce').fillna(0)
                    merged_gdf[column2] = pd.to_numeric(merged_gdf[column2], errors='coerce').fillna(0)
                    
                    # Perform calculation
                    if operation == "divide":
                        # Handle division by zero
                        result = np.where(
                            merged_gdf[column2] != 0,
                            merged_gdf[column1] / merged_gdf[column2],
                            0
                        ) * scaling
                    elif operation == "multiply":
                        result = merged_gdf[column1] * merged_gdf[column2] * scaling
                    elif operation == "add":
                        result = (merged_gdf[column1] + merged_gdf[column2]) * scaling
                    elif operation == "subtract":
                        result = (merged_gdf[column1] - merged_gdf[column2]) * scaling
                    
                    merged_gdf[new_column_name] = result
                    st.session_state.merged_data = merged_gdf
                    st.success(f"Created new column: {new_column_name}")
                except Exception as e:
                    st.error(f"Error calculating field: {e}")
            
            # Create categorical field
            st.subheader("Create Categorical Field")
            
            col1, col2 = st.columns(2)
            
            with col1:
                category_column_name = st.text_input("New category column name:")
                source_column = st.selectbox(
                    "Source column:",
                    [c for c in merged_gdf.columns if c != 'geometry']
                )
            
            with col2:
                threshold = st.text_input("Threshold value:")
                true_value = st.text_input("Value when true:", value="Yes")
                false_value = st.text_input("Value when false:", value="No")
            
            if st.button("Create Category") and category_column_name and source_column and threshold:
                try:
                    # Convert to numeric if possible
                    if threshold.replace('.', '', 1).isdigit():
                        threshold = float(threshold)
                    
                    # Convert source column to numeric if needed
                    if pd.api.types.is_numeric_dtype(merged_gdf[source_column]):
                        merged_gdf[source_column] = pd.to_numeric(merged_gdf[source_column], errors='coerce').fillna(0)
                    
                    # Create category
                    merged_gdf[category_column_name] = np.where(
                        merged_gdf[source_column] > threshold,
                        true_value,
                        false_value
                    )
                    
                    st.session_state.merged_data = merged_gdf
                    st.success(f"Created new category column: {category_column_name}")
                except Exception as e:
                    st.error(f"Error creating category: {e}")

# Tab 3: Create Map
with tab3:
    st.header("Create Map")
    
    if st.session_state.merged_data is None:
        st.info("Please process your data in the Data Processing tab first.")
    else:
        gdf = st.session_state.merged_data
        
        # Get categorical columns
        categorical_columns = [col for col in gdf.columns if col != 'geometry' and 
                              (gdf[col].dtype == 'object' or pd.api.types.is_categorical_dtype(gdf[col]))]
        
        # Select column for mapping
        map_column = st.selectbox("Select column for mapping:", categorical_columns)
        
        if map_column:
            # Get unique categories
            unique_categories = gdf[map_column].dropna().unique()
            
            # Map settings
            st.subheader("Map Settings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                map_title = st.text_input("Map title:")
                legend_title = st.text_input("Legend title:")
            
            # Color selection
            st.subheader("Color Selection")
            
            # Default colors
            default_colors = {
                'Yes': '#B0E0E6',  # Light blue
                'No': 'white'
            }
            
            colors = {}
            for category in unique_categories:
                default_color = default_colors.get(category, '#CCCCCC')
                color = st.color_picker(f"Color for {category}:", default_color)
                colors[category] = color
            
            # Generate map button
            if st.button("Generate Map"):
                try:
                    fig = create_map(
                        gdf,
                        map_column,
                        colors,
                        title=map_title,
                        legend_title=legend_title
                    )
                    
                    st.pyplot(fig)
                    
                    # Save map for download
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                    buf.seek(0)
                    st.session_state.map_image = buf
                    
                    st.success("Map generated successfully!")
                except Exception as e:
                    st.error(f"Error generating map: {e}")

# Tab 4: Export
with tab4:
    st.header("Export Results")
    
    if st.session_state.merged_data is None:
        st.info("Please process your data before exporting.")
    else:
        st.subheader("Download Processed Data")
        
        # Prepare data for download
        try:
            # Excel export
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                # Drop geometry column for Excel export
                data_for_excel = st.session_state.merged_data.drop(columns=['geometry'])
                data_for_excel.to_excel(writer, index=False, sheet_name='Data')
            output.seek(0)
            
            st.download_button(
                label="Download Excel File",
                data=output,
                file_name="processed_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Error preparing Excel download: {e}")
        
        # Download map if available
        if st.session_state.map_image is not None:
            st.subheader("Download Map")
            
            st.download_button(
                label="Download Map as PNG",
                data=st.session_state.map_image,
                file_name="map.png",
                mime="image/png"
            )
            
            st.image(st.session_state.map_image, caption="Generated Map")

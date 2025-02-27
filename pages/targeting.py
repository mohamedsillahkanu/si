import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import io
import tempfile
import os

st.set_page_config(page_title="Geospatial Analysis Tool", layout="wide")

# Custom CSS to improve the appearance
st.markdown("""
<style>
    .main {
        padding: 1rem;
    }
    .stButton button {
        width: 100%;
    }
    .stTitle {
        font-weight: bold;
        font-size: 24px;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def save_uploaded_file(uploaded_file):
    """Save the uploaded file to a temporary directory and return the path"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name

def apply_condition(df, condition):
    """Apply a condition to a dataframe"""
    column1 = condition['column1']
    operator = condition['operator']
    column2 = condition['column2']
    value = condition['value']
    
    # Convert to appropriate type if needed
    if value and value.replace('.', '', 1).isdigit():
        value = float(value)
    
    if operator == 'equals':
        return df[column1] == (df[column2] if column2 else value)
    elif operator == 'not equals':
        return df[column1] != (df[column2] if column2 else value)
    elif operator == 'greater than':
        return df[column1] > (df[column2] if column2 else value)
    elif operator == 'less than':
        return df[column1] < (df[column2] if column2 else value)
    elif operator == 'greater than or equal to':
        return df[column1] >= (df[column2] if column2 else value)
    elif operator == 'less than or equal to':
        return df[column1] <= (df[column2] if column2 else value)
    elif operator == 'contains':
        return df[column1].astype(str).str.contains(str(value), na=False)
    elif operator == 'does not contain':
        return ~df[column1].astype(str).str.contains(str(value), na=False)
    elif operator == 'is not null':
        return ~df[column1].isna()
    elif operator == 'is null':
        return df[column1].isna()
    elif operator == 'divide':
        # Handle division by zero
        return np.where(
            df[column2] != 0,
            df[column1] / df[column2],
            0
        )
    elif operator == 'multiply':
        return df[column1] * (df[column2] if column2 else value)
    elif operator == 'add':
        return df[column1] + (df[column2] if column2 else value)
    elif operator == 'subtract':
        return df[column1] - (df[column2] if column2 else value)

def create_map(gdf, category_column, colors, title, legend_title):
    """Create a map with the given parameters"""
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
    
    # Calculate category counts for legend
    category_counts = gdf[category_column].value_counts()
    
    # Plot the map
    gdf.plot(
        ax=ax,
        color=gdf[category_column].map(colors)
    )
    
    # Add borders
    gdf.boundary.plot(color='gray', linewidth=0.5, ax=ax)
    
    # District boundaries if FIRST_DNAM exists
    if 'FIRST_DNAM' in gdf.columns:
        district_boundaries = gdf.dissolve(by='FIRST_DNAM')
        district_boundaries.boundary.plot(
            ax=ax,
            color='black',
            linewidth=1.0,
            zorder=2
        )
    
    # Add legend with counts and borders
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
    
    # Add legend with frame
    ax.legend(
        handles=legend_elements,
        title=legend_title,
        loc='center left',
        bbox_to_anchor=(1, 0.5),
        fontsize=10,
        title_fontsize=12,
        frameon=True,
        edgecolor='black',
        facecolor='white'
    )
    
    # Remove axes
    ax.axis('off')
    
    # Add title
    plt.title(title,
              pad=10,
              fontsize=14,
              fontweight='bold')
    
    # Tight layout
    plt.tight_layout(pad=0.5)
    
    return fig

# App title
st.title("Interactive Geospatial Analysis and Mapping Tool")

# Initialize session state
if 'data_files' not in st.session_state:
    st.session_state.data_files = {}
if 'shapefile' not in st.session_state:
    st.session_state.shapefile = None
if 'conditions' not in st.session_state:
    st.session_state.conditions = []
if 'dataframes' not in st.session_state:
    st.session_state.dataframes = {}
if 'merged_df' not in st.session_state:
    st.session_state.merged_df = None
if 'merged_gdf' not in st.session_state:
    st.session_state.merged_gdf = None
if 'calculated_columns' not in st.session_state:
    st.session_state.calculated_columns = []
if 'join_keys' not in st.session_state:
    st.session_state.join_keys = []

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Upload Data", 
    "2. Data Preparation",
    "3. Define Conditions",
    "4. Create Map",
    "5. Export Results"
])

# Tab 1: Upload Data
with tab1:
    st.header("Upload Your Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload Data Files")
        data_file = st.file_uploader(
            "Upload Excel or CSV files",
            type=["xlsx", "xls", "csv"],
            key="data_file_uploader",
            accept_multiple_files=True
        )
        
        if data_file:
            for file in data_file:
                file_name = file.name
                if file_name not in st.session_state.data_files:
                    st.session_state.data_files[file_name] = file
                    
                    # Read the data
                    if file_name.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(file)
                    else:
                        df = pd.read_csv(file)
                    
                    st.session_state.dataframes[file_name] = df
            
            st.success(f"Uploaded {len(st.session_state.data_files)} data files.")
    
    with col2:
        st.subheader("Upload Shapefile")
        shapefile_container = st.container()
        
        with shapefile_container:
            shapefile = st.file_uploader(
                "Upload shapefile components (.shp, .shx, .dbf, .prj)",
                type=["shp", "shx", "dbf", "prj"],
                key="shapefile_uploader",
                accept_multiple_files=True
            )
            
            if shapefile:
                # Check if necessary components are uploaded
                required_extensions = ['.shp', '.shx', '.dbf']
                uploaded_extensions = [os.path.splitext(file.name)[1].lower() for file in shapefile]
                
                if all(ext in uploaded_extensions for ext in required_extensions):
                    # Create a temporary directory to store the shapefile components
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
                    except Exception as e:
                        st.error(f"Error loading shapefile: {e}")
                else:
                    st.warning("Please upload all required shapefile components (.shp, .shx, .dbf)")
    
    # Display data preview
    if st.session_state.dataframes:
        st.subheader("Data Preview")
        selected_data = st.selectbox(
            "Select data file to preview:",
            list(st.session_state.dataframes.keys())
        )
        
        if selected_data:
            st.write(st.session_state.dataframes[selected_data].head())
    
    # Display shapefile preview
    if st.session_state.shapefile is not None:
        st.subheader("Shapefile Preview")
        st.write(st.session_state.shapefile.head())

# Tab 2: Data Preparation
with tab2:
    st.header("Data Preparation")
    
    if not st.session_state.dataframes:
        st.info("Please upload data files in the 'Upload Data' tab first.")
    else:
        # String cleaning
        st.subheader("Clean String Columns")
        
        selected_data = st.selectbox(
            "Select data file for cleaning:",
            list(st.session_state.dataframes.keys()),
            key="cleaning_data_selector"
        )
        
        if selected_data:
            df = st.session_state.dataframes[selected_data]
            
            # Select string columns for cleaning
            string_columns = df.select_dtypes(include=['object']).columns.tolist()
            columns_to_clean = st.multiselect(
                "Select string columns to clean (strip whitespace):",
                string_columns
            )
            
            if columns_to_clean and st.button("Clean Selected Columns"):
                for col in columns_to_clean:
                    df[col] = df[col].astype(str).str.strip()
                st.session_state.dataframes[selected_data] = df
                st.success(f"Cleaned {len(columns_to_clean)} columns in {selected_data}.")
        
        # Data merging section
        st.subheader("Merge Data")
        
        if len(st.session_state.dataframes) >= 2:
            col1, col2 = st.columns(2)
            
            with col1:
                base_data = st.selectbox(
                    "Select base dataset:",
                    list(st.session_state.dataframes.keys()),
                    key="base_data_selector"
                )
            
            with col2:
                merge_data = st.selectbox(
                    "Select dataset to merge with base:",
                    [f for f in list(st.session_state.dataframes.keys()) if f != base_data],
                    key="merge_data_selector"
                )
            
            if base_data and merge_data:
                df1 = st.session_state.dataframes[base_data]
                df2 = st.session_state.dataframes[merge_data]
                
                # Find common columns
                common_columns = list(set(df1.columns) & set(df2.columns))
                
                if common_columns:
                    st.write(f"Found {len(common_columns)} common columns: {', '.join(common_columns)}")
                    
                    # Use all common columns as join keys by default
                    st.info("Using all common columns for merging with left join and validate='1:1'")
                    
                    if st.button("Merge Datasets"):
                        try:
                            merged_df = df1.merge(
                                df2,
                                on=common_columns,  # Use all common columns automatically
                                how='left',         # Use left join by default
                                validate="1:1",     # Enforce 1:1 relationship
                                suffixes=('', f'_{merge_data}')
                            )
                            
                            st.session_state.merged_df = merged_df
                            st.session_state.join_keys = common_columns
                            st.success(f"Successfully merged datasets. Result has {len(merged_df)} rows and {len(merged_df.columns)} columns.")
                            
                            st.write("Preview of merged data:")
                            st.write(merged_df.head())
                        except Exception as e:
                            st.error(f"Error merging datasets: {e}")
                else:
                    st.warning("No common columns found between selected datasets.")
        else:
            st.info("Upload at least two datasets to perform merging.")
        
        # Data type conversion
        if st.session_state.merged_df is not None:
            st.subheader("Convert Data Types")
            
            numeric_columns = st.multiselect(
                "Select columns to convert to numeric:",
                st.session_state.merged_df.columns.tolist(),
                key="numeric_columns_selector"
            )
            
            if numeric_columns and st.button("Convert to Numeric"):
                merged_df = st.session_state.merged_df.copy()
                
                for col in numeric_columns:
                    merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')
                    merged_df[col] = merged_df[col].fillna(0)
                
                st.session_state.merged_df = merged_df
                st.success(f"Converted {len(numeric_columns)} columns to numeric and filled NA with 0.")
        
        # Merge with shapefile
        if st.session_state.merged_df is not None and st.session_state.shapefile is not None:
            st.subheader("Merge with Shapefile")
            
            gdf = st.session_state.shapefile
            
            # Find common columns
            common_columns = list(set(st.session_state.merged_df.columns) & set(gdf.columns))
            
            if common_columns:
                st.write(f"Found {len(common_columns)} common columns between data and shapefile: {', '.join(common_columns)}")
                
                # Use all common columns by default
                st.info("Using all common columns for merging with shapefile using left join and validate='1:1'")
                
                if st.button("Merge with Shapefile"):
                    try:
                        # Clean string columns in shapefile if they're join keys
                        for key in common_columns:
                            if gdf[key].dtype == 'object':
                                gdf[key] = gdf[key].astype(str).str.strip()
                        
                        # Merge
                        merged_gdf = gdf.merge(
                            st.session_state.merged_df,
                            on=common_columns,  # Use all common columns
                            how='left',         # Use left join
                            validate="1:1"      # Enforce 1:1 relationship
                        )
                        
                        st.session_state.merged_gdf = merged_gdf
                        st.success(f"Successfully merged data with shapefile. Result has {len(merged_gdf)} features.")
                        
                        st.write("Preview of merged geodataframe:")
                        st.write(merged_gdf.head())
                    except Exception as e:
                        st.error(f"Error merging with shapefile: {e}")
            else:
                st.warning("No common columns found between data and shapefile.")

# Tab 3: Define Conditions
with tab3:
    st.header("Define Conditions and Calculate Fields")
    
    if st.session_state.merged_df is None:
        st.info("Please prepare your data in the 'Data Preparation' tab first.")
    else:
        merged_df = st.session_state.merged_df.copy() if st.session_state.merged_gdf is None else st.session_state.merged_gdf.copy()
        
        # Create calculated fields
        st.subheader("Create Calculated Fields")
        
        with st.form("calculated_field_form"):
            st.write("Define a calculated field based on existing columns")
            
            new_column_name = st.text_input("New column name:", key="new_column_name")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                column1 = st.selectbox(
                    "First column:",
                    merged_df.columns.tolist(),
                    key="calc_column1"
                )
            
            with col2:
                operator = st.selectbox(
                    "Operation:",
                    ["divide", "multiply", "add", "subtract"],
                    key="calc_operator"
                )
            
            with col3:
                use_column = st.radio(
                    "Use second column or constant value?",
                    ["Column", "Value"],
                    key="calc_use_column"
                )
                
                if use_column == "Column":
                    column2 = st.selectbox(
                        "Second column:",
                        merged_df.columns.tolist(),
                        key="calc_column2"
                    )
                    value = None
                else:
                    column2 = None
                    value = st.text_input("Constant value:", key="calc_value")
            
            # Optional scaling factor
            scaling_factor = st.number_input(
                "Apply scaling factor to result (e.g., 1000 for per thousand):",
                value=1.0,
                step=1.0,
                key="calc_scaling"
            )
            
            submit_calc = st.form_submit_button("Create Calculated Field")
        
        if submit_calc and new_column_name and column1:
            try:
                # Create the condition dictionary
                condition = {
                    'column1': column1,
                    'operator': operator,
                    'column2': column2,
                    'value': value
                }
                
                # Apply the calculation
                result = apply_condition(merged_df, condition)
                
                # Apply scaling factor
                if scaling_factor != 1.0:
                    result = result * scaling_factor
                
                # Add the result as a new column
                merged_df[new_column_name] = result
                
                # Update the data
                if st.session_state.merged_gdf is not None:
                    st.session_state.merged_gdf[new_column_name] = result
                else:
                    st.session_state.merged_df[new_column_name] = result
                
                # Add to calculated columns
                st.session_state.calculated_columns.append(new_column_name)
                
                st.success(f"Created new column: {new_column_name}")
                
                # Show histogram of the new column
                fig, ax = plt.subplots(figsize=(10, 4))
                merged_df[new_column_name].plot(kind='hist', ax=ax)
                plt.title(f"Distribution of {new_column_name}")
                st.pyplot(fig)
                
                # Show summary statistics
                st.write("Summary statistics:")
                st.write(merged_df[new_column_name].describe())
            except Exception as e:
                st.error(f"Error creating calculated field: {e}")
        
        # Create categorical fields based on conditions
        st.subheader("Create Categorical Fields")
        
        with st.form("categorical_field_form"):
            st.write("Define a categorical field based on conditions")
            
            category_column_name = st.text_input("New category column name:", key="category_column_name")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                source_column = st.selectbox(
                    "Source column:",
                    [col for col in merged_df.columns.tolist()] + 
                    st.session_state.calculated_columns,
                    key="cat_source_column"
                )
            
            with col2:
                condition_type = st.selectbox(
                    "Condition type:",
                    ["greater than", "less than", "equals", "not equals",
                     "greater than or equal to", "less than or equal to"],
                    key="cat_condition_type"
                )
            
            with col3:
                threshold_value = st.text_input("Threshold value:", key="cat_threshold")
            
            # Values for true and false conditions
            col1, col2 = st.columns(2)
            
            with col1:
                true_value = st.text_input("Value when condition is true:", value="Yes", key="cat_true_value")
            
            with col2:
                false_value = st.text_input("Value when condition is false:", value="No", key="cat_false_value")
            
            submit_cat = st.form_submit_button("Create Categorical Field")
        
        if submit_cat and category_column_name and source_column and threshold_value:
            try:
                # Create the condition dictionary
                condition = {
                    'column1': source_column,
                    'operator': condition_type,
                    'column2': None,
                    'value': threshold_value
                }
                
                # Apply the condition
                mask = apply_condition(merged_df, condition)
                
                # Create the categorical column
                merged_df[category_column_name] = np.where(mask, true_value, false_value)
                
                # Update the data
                if st.session_state.merged_gdf is not None:
                    st.session_state.merged_gdf[category_column_name] = np.where(mask, true_value, false_value)
                else:
                    st.session_state.merged_df[category_column_name] = np.where(mask, true_value, false_value)
                
                st.success(f"Created new categorical column: {category_column_name}")
                
                # Show value counts
                st.write("Value counts:")
                st.write(merged_df[category_column_name].value_counts())
            except Exception as e:
                st.error(f"Error creating categorical field: {e}")

# Tab 4: Create Map
with tab4:
    st.header("Create and Customize Map")
    
    if st.session_state.merged_gdf is None:
        st.info("Please merge your data with the shapefile in the 'Data Preparation' tab first.")
    else:
        gdf = st.session_state.merged_gdf.copy()
        
        st.subheader("Map Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Select category column for mapping
            category_columns = [col for col in gdf.columns if gdf[col].dtype == 'object' or pd.api.types.is_categorical_dtype(gdf[col])]
            
            map_column = st.selectbox(
                "Select category column for mapping:",
                category_columns,
                key="map_column"
            )
            
            map_title = st.text_input("Map title:", key="map_title")
            legend_title = st.text_input("Legend title:", key="legend_title")
        
        with col2:
            # Color customization
            if map_column:
                unique_categories = gdf[map_column].dropna().unique()
                
                st.write("Customize colors for each category:")
                
                color_dict = {}
                for i, category in enumerate(unique_categories):
                    # Default colors
                    default_colors = ['#B0E0E6', '#FF9999', '#FFCC99', '#99CC99', '#9999FF']
                    default_color = default_colors[i % len(default_colors)]
                    
                    color = st.color_picker(
                        f"Color for {category}:",
                        default_color,
                        key=f"color_{category}"
                    )
                    color_dict[category] = color
        
        # Generate map button
        if map_column and st.button("Generate Map"):
            try:
                fig = create_map(
                    gdf,
                    map_column,
                    color_dict,
                    map_title,
                    legend_title
                )
                
                st.pyplot(fig)
                
                # Save map to session state for download
                buf = io.BytesIO()
                fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                buf.seek(0)
                st.session_state.map_image = buf
                
                st.success("Map generated successfully! Go to the 'Export Results' tab to download it.")
            except Exception as e:
                st.error(f"Error generating map: {e}")

# Tab 5: Export Results
with tab5:
    st.header("Export Results")
    
    if st.session_state.merged_df is None:
        st.info("Please prepare your data first.")
    else:
        st.subheader("Download Processed Data")
        
        file_format = st.radio(
            "Select file format:",
            ["Excel (.xlsx)", "CSV (.csv)"],
            key="download_format"
        )
        
        if st.button("Prepare Download Link"):
            try:
                if file_format == "Excel (.xlsx)":
                    output = io.BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    
                    if st.session_state.merged_gdf is not None:
                        # Save geodataframe without geometry column
                        gdf_no_geom = st.session_state.merged_gdf.drop(columns=['geometry'])
                        gdf_no_geom.to_excel(writer, index=False, sheet_name='Data')
                    else:
                        st.session_state.merged_df.to_excel(writer, index=False, sheet_name='Data')
                    
                    writer.close()
                    output.seek(0)
                    
                    # Create download button
                    st.download_button(
                        label="Download Excel File",
                        data=output,
                        file_name="processed_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    if st.session_state.merged_gdf is not None:
                        # Save geodataframe without geometry column
                        gdf_no_geom = st.session_state.merged_gdf.drop(columns=['geometry'])
                        csv = gdf_no_geom.to_csv(index=False)
                    else:
                        csv = st.session_state.merged_df.to_csv(index=False)
                    
                    # Create download button
                    st.download_button(
                        label="Download CSV File",
                        data=csv,
                        file_name="processed_data.csv",
                        mime="text/csv"
                    )
            except Exception as e:
                st.error(f"Error preparing download: {e}")
        
        # Download map
        if hasattr(st.session_state, 'map_image'):
            st.subheader("Download Generated Map")
            
            st.download_button(
                label="Download Map as PNG",
                data=st.session_state.map_image,
                file_name="generated_map.png",
                mime="image/png"
            )
            
            st.write("Preview:")
            st.image(st.session_state.map_image, caption="Generated Map")

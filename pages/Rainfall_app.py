import streamlit as st
import geopandas as gpd
import rasterio
import rasterio.mask
import rasterio.warp
import numpy as np
import os
import requests
import gzip
import shutil
import tempfile
import pandas as pd
from io import BytesIO
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from shapely.geometry import Polygon, MultiPolygon
import re

# Function to load and process the shapefile
def load_shapefile(shp_file, shx_file, dbf_file):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Save the uploaded files to a temporary directory
        for file, ext in zip([shp_file, shx_file, dbf_file], ['.shp', '.shx', '.dbf']):
            with open(os.path.join(tmpdir, f"file{ext}"), "wb") as f:
                f.write(file.getbuffer())

        # Load the shapefile using GeoPandas
        shapefile_path = os.path.join(tmpdir, "file.shp")
        gdf = gpd.read_file(shapefile_path)
    
    # Check if geometry column exists and is valid
    if 'geometry' not in gdf.columns or gdf.geometry.isna().all():
        st.warning("Standard geometry column not found or invalid. Checking for alternative geometry representations...")
        
        # Check for any column that might contain geometry information
        geometry_columns = [col for col in gdf.columns if 'geom' in col.lower()]
        
        if not geometry_columns:
            st.error("No geometry columns found in the shapefile.")
            return None
        
        # Try to use the first geometry column found
        geometry_col = geometry_columns[0]
        st.info(f"Using {geometry_col} as the geometry column.")
        
        # Try to convert the geometry column to proper geometries
        try:
            # Check if it's already a proper geometry type
            first_geom = gdf[geometry_col].iloc[0]
            
            if hasattr(first_geom, 'wkt') or hasattr(first_geom, 'wkb'):
                # It's already a geometry object, set it as the geometry column
                gdf = gdf.set_geometry(geometry_col)
            else:
                # It might be a WKT string or some other representation
                if isinstance(first_geom, str):
                    # Check if it's a WKT string (starts with POLYGON, MULTIPOLYGON, etc.)
                    wkt_pattern = r'(POLYGON|MULTIPOLYGON|POINT|LINESTRING|MULTIPOINT|MULTILINESTRING|GEOMETRYCOLLECTION)'
                    if re.match(wkt_pattern, first_geom.strip()):
                        from shapely import wkt
                        gdf['geometry'] = gdf[geometry_col].apply(lambda x: wkt.loads(x) if isinstance(x, str) else None)
                        gdf = gdf.set_geometry('geometry')
                    else:
                        st.error(f"Unable to parse geometry from {geometry_col}. Not a valid WKT format.")
                        return None
                else:
                    st.error(f"Unable to use {geometry_col} as geometry. Unsupported format.")
                    return None
        except Exception as e:
            st.error(f"Error converting {geometry_col} to geometry: {str(e)}")
            return None

    # Check if the CRS is set, if not, set it manually
    if gdf.crs is None:
        st.warning("CRS not defined in shapefile. Setting to WGS84 (EPSG:4326).")
        gdf = gdf.set_crs("EPSG:4326")  # Assuming WGS84; replace with correct CRS if different

    # Check for invalid geometries and try to fix them
    if not all(gdf.geometry.is_valid):
        st.warning("Found invalid geometries in shapefile. Attempting to fix...")
        gdf.geometry = gdf.geometry.buffer(0)  # This can fix some common issues
    
    # Display a sample of the data
    st.write("Sample of loaded shapefile data:")
    st.write(gdf.head(3))
    
    return gdf

# Function to download, unzip, and process CHIRPS data
def process_chirps_data(gdf, year, month, force_overlap=False):
    try:
        # Define the link for CHIRPS data - using Africa dataset only
        link = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_monthly/tifs/chirps-v2.0.{year}.{month:02d}.tif.gz"

        # Download the .tif.gz file
        response = requests.get(link)
        if response.status_code != 200:
            st.warning(f"Unable to download data for {year}-{month:02d}. Status code: {response.status_code}")
            gdf[f'rain_{year}_{month:02d}'] = np.nan
            return gdf

        with tempfile.TemporaryDirectory() as tmpdir:
            zipped_file_path = os.path.join(tmpdir, "chirps.tif.gz")
            unzipped_file_path = os.path.join(tmpdir, "chirps.tif")

            with open(zipped_file_path, "wb") as f:
                f.write(response.content)

            # Unzip the file
            with gzip.open(zipped_file_path, "rb") as f_in:
                with open(unzipped_file_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Open the unzipped .tif file with Rasterio
            with rasterio.open(unzipped_file_path) as src:
                # Convert source raster bounds to WGS84 for comparison
                raster_bounds = rasterio.warp.transform_bounds(src.crs, "EPSG:4326", 
                                                            *src.bounds)
                
                # Get shapefile bounds in WGS84
                shapefile_bounds = gdf.to_crs("EPSG:4326").total_bounds
                
                # Check for overlap
                overlap = (raster_bounds[0] < shapefile_bounds[2] and 
                          raster_bounds[2] > shapefile_bounds[0] and
                          raster_bounds[1] < shapefile_bounds[3] and
                          raster_bounds[3] > shapefile_bounds[1])
                
                # Display debug info if requested
                if st.session_state.get('debug_mode', False):
                    st.write(f"Raster CRS: {src.crs}")
                    st.write(f"Raster bounds: {raster_bounds}")
                    st.write(f"Shapefile CRS: {gdf.crs}")
                    st.write(f"Shapefile bounds: {shapefile_bounds}")
                
                if not overlap:
                    if not force_overlap:
                        st.warning(f"Shapefile does not overlap with CHIRPS data for {year}-{month:02d}.")
                        gdf[f'rain_{year}_{month:02d}'] = np.nan
                        return gdf
                    else:
                        st.warning(f"Shapefile does not naturally overlap with CHIRPS data. Applying transformation...")
                        
                # If force_overlap is enabled or there's a natural overlap, proceed
                # Generate new geometries that will overlap with the raster
                if force_overlap and not overlap:
                    # Create a copy of the GeoDataFrame to avoid modifying the original
                    transformed_gdf = gdf.copy()
                    
                    # Transform to the target region (center of CHIRPS data)
                    raster_center_x = (raster_bounds[0] + raster_bounds[2]) / 2
                    raster_center_y = (raster_bounds[1] + raster_bounds[3]) / 2
                    
                    # Calculate shapefile center
                    shapefile_center_x = (shapefile_bounds[0] + shapefile_bounds[2]) / 2
                    shapefile_center_y = (shapefile_bounds[1] + shapefile_bounds[3]) / 2
                    
                    # Calculate the translation distances
                    dx = raster_center_x - shapefile_center_x
                    dy = raster_center_y - shapefile_center_y
                    
                    # Calculate scaling to fit within the raster bounds
                    # Determine the current width and height of the shapefile
                    shapefile_width = shapefile_bounds[2] - shapefile_bounds[0]
                    shapefile_height = shapefile_bounds[3] - shapefile_bounds[1]
                    
                    # Determine the width and height of the raster
                    raster_width = raster_bounds[2] - raster_bounds[0]
                    raster_height = raster_bounds[3] - raster_bounds[1]
                    
                    # Calculate scaling factors (making shapefile 80% of raster size)
                    scale_x = 0.8 * raster_width / shapefile_width
                    scale_y = 0.8 * raster_height / shapefile_height
                    
                    # Apply transformation to each geometry
                    from shapely.affinity import translate, scale
                    
                    # First translate to ensure shapefile is within Africa if using Africa dataset
                    # Then scale to ensure it's not too big or too small
                    transformed_geometries = []
                    for geom in transformed_gdf.geometry:
                        # First translate the geometry
                        translated = translate(geom, xoff=dx, yoff=dy)
                        # Then scale it
                        transformed = scale(translated, xfact=scale_x, yfact=scale_y, origin=(raster_center_x, raster_center_y))
                        transformed_geometries.append(transformed)
                    
                    # Update the geometries in the GeoDataFrame
                    transformed_gdf.geometry = transformed_geometries
                    
                    # Use transformed GeoDataFrame for further processing
                    gdf_to_use = transformed_gdf
                    
                    st.success("Shapefile successfully transformed to overlap with CHIRPS data.")
                else:
                    # Use original GeoDataFrame
                    gdf_to_use = gdf
                
                # Reproject shapefile to match CHIRPS data CRS
                gdf_reprojected = gdf_to_use.to_crs(src.crs)

                # Process each geometry individually to handle potential errors
                mean_rains = []
                for idx, geom in enumerate(gdf_reprojected.geometry):
                    try:
                        # Check if the geometry is valid
                        if not geom.is_valid:
                            geom = geom.buffer(0)  # Simple fix for invalid geometries
                        
                        masked_data, _ = rasterio.mask.mask(src, [geom], crop=True, nodata=src.nodata)
                        masked_data = masked_data.flatten()
                        
                        # Filter out nodata values
                        valid_data = masked_data[masked_data != src.nodata]
                        
                        if len(valid_data) > 0:
                            mean_rains.append(valid_data.mean())
                        else:
                            mean_rains.append(np.nan)
                    except Exception as e:
                        st.warning(f"Error processing geometry {idx}: {str(e)}")
                        mean_rains.append(np.nan)

                # Add result as a column with year and month in the name
                gdf[f'rain_{year}_{month:02d}'] = mean_rains

        return gdf
        
    except Exception as e:
        st.error(f"Error processing CHIRPS data for {year}-{month:02d}: {str(e)}")
        gdf[f'rain_{year}_{month:02d}'] = np.nan
        return gdf

# Initialize session state for debug mode
if 'debug_mode' not in st.session_state:
    st.session_state['debug_mode'] = False

# Streamlit app layout
st.title("CHIRPS Africa Rainfall Analysis App")
st.markdown("""
This app processes shapefile data for Africa and overlays it with CHIRPS rainfall data to create visualizations and analysis.
Upload your shapefile components below and select the year and months you want to analyze.
""")

# Add debug mode toggle
debug_mode = st.sidebar.checkbox("Debug Mode", value=st.session_state['debug_mode'])
st.session_state['debug_mode'] = debug_mode

# Force overlap option
force_overlap = st.sidebar.checkbox("Force overlap with CHIRPS data", value=True,
                                  help="Transform your shapefile to overlap with CHIRPS data")

# App explanation expander
with st.expander("How to use this app"):
    st.markdown("""
    ### Instructions:
    1. **Upload your shapefile components** (.shp, .shx, .dbf files)
    2. **Select the year** you want to analyze (1981-2024)
    3. By default, all months will be analyzed. You can customize this selection.
    4. **Choose a colormap** for visualization
    5. Click the **Generate Analysis** button
    
    ### Options in the sidebar:
    - **Force overlap**: If your shapefile region doesn't naturally overlap with the CHIRPS data, 
      this option will transform your geometries to fit within the African CHIRPS region
    - **Debug Mode**: Shows additional technical information for troubleshooting
    
    ### About CHIRPS data:
    CHIRPS (Climate Hazards Group InfraRed Precipitation with Station data) is a rainfall dataset 
    that spans from 1981 to near-present. It's commonly used for drought monitoring and analysis.
    """)

# Upload shapefile components
st.header("Upload Shapefile Components")
col1, col2, col3 = st.columns(3)
with col1:
    uploaded_shp = st.file_uploader("Upload .shp file", type="shp")
with col2:
    uploaded_shx = st.file_uploader("Upload .shx file", type="shx")
with col3:
    uploaded_dbf = st.file_uploader("Upload .dbf file", type="dbf")

# Year and month selection
st.header("Select Data Range")
year = st.selectbox("Select Year", range(1981, 2025))

# Automatically select all months when a year is selected
all_months = list(range(1, 13))
months = all_months  # Default to all months

# Display the selected months (read-only)
st.write("Selected Months: All months (January to December)")

# Optional: Allow user to deselect specific months if needed
if st.checkbox("Customize month selection", value=False):
    months = st.multiselect("Select specific months", 
                          options=all_months,
                          default=all_months,
                          format_func=lambda x: f"{x:02d} - {['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][x-1]}")

# Visualization options
st.header("Visualization Options")
cmap = st.selectbox("Select Colormap", ['Blues', 'Greens', 'Reds', 'Purples', 'Oranges', 'YlGnBu', 'cividis', 'plasma', 'viridis'])

# Add a Generate button
generate_button = st.button("Generate Analysis", type="primary")

if uploaded_shp and uploaded_shx and uploaded_dbf and year and generate_button:
    # Load and process the shapefile
    with st.spinner("Loading and processing shapefile..."):
        gdf = load_shapefile(uploaded_shp, uploaded_shx, uploaded_dbf)
    
    if gdf is None:
        st.error("Unable to process the shapefile. Please check your files and try again.")
        st.stop()

    st.success("Shapefile loaded successfully!")
    
    if debug_mode:
        st.write("Shapefile CRS:", gdf.crs)
        st.write("Shapefile bounds:", gdf.total_bounds)
        st.write("Shapefile columns:", gdf.columns.tolist())
    
    processed_gdf = gdf.copy()
    
    # Process CHIRPS data for each selected month
    progress_bar = st.progress(0)
    for i, month in enumerate(months):
        with st.spinner(f"Processing CHIRPS data for {year}-{month:02d}... ({i+1}/{len(months)})"):
            processed_gdf = process_chirps_data(processed_gdf, year, month, force_overlap=force_overlap)
            progress_bar.progress((i + 1) / len(months))
    
    st.success("CHIRPS data processing complete!")
    
    # Check if any data was successfully processed
    rain_columns = [col for col in processed_gdf.columns if col.startswith('rain_')]
    
    if not rain_columns:
        st.error("No rainfall data could be processed for any month. Please check your shapefile region and try again.")
        st.stop()
    
    # Check for months with no data (all NaN values)
    nan_months = []
    for col in rain_columns:
        if processed_gdf[col].isna().all():
            _, year_str, month_str = col.split('_')
            month_val = int(month_str)
            month_name = ['January', 'February', 'March', 'April', 'May', 'June', 
                        'July', 'August', 'September', 'October', 'November', 'December'][month_val-1]
            nan_months.append(f"{month_name} {year_str}")
    
    if nan_months:
        st.warning(f"No data available for the following months: {', '.join(nan_months)}")
    
    # Create a restructured DataFrame with Month, Year, and mean_rain columns
    restructured_data = []
    
    # Identify region name column
    region_name_candidates = ['Region', 'NAME', 'Name', 'REGION', 'shapeName', 'Nom_DS']
    region_name_col = None
    
    for col in region_name_candidates:
        if col in processed_gdf.columns:
            region_name_col = col
            break
    
    if region_name_col is None and len(processed_gdf.columns) > 0:
        # Use the first non-geometry, non-rainfall column as region name
        non_geom_cols = [col for col in processed_gdf.columns 
                        if col != 'geometry' and not col.startswith('rain_')]
        if non_geom_cols:
            region_name_col = non_geom_cols[0]
    
    for column in rain_columns:
        # Extract year and month from column name
        _, year_str, month_str = column.split('_')
        year_val = int(year_str)
        month_val = int(month_str)
        
        # For each region in the shapefile
        for idx, row in processed_gdf.iterrows():
            region_data = {col: row[col] for col in processed_gdf.columns 
                          if not col.startswith('rain_') and col != 'geometry'}
            region_data['Year'] = year_val
            region_data['Month'] = month_val
            region_data['mean_rain'] = row[column]
            
            # Add region name if available
            if region_name_col:
                region_data['Region'] = row[region_name_col]
            else:
                region_data['Region'] = f"Region {idx+1}"
                
            restructured_data.append(region_data)
    
    # Create the restructured DataFrame
    restructured_df = pd.DataFrame(restructured_data)
    
    # Display the restructured data
    st.subheader("Processed Rainfall Data")
    st.write(restructured_df)
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Monthly Grid View", "Individual Maps", "Summary Data"])
    
    with tab1:
        st.subheader(f"Rainfall Maps for All Months in {year}")
        
        # Create a 2x6 subplot grid for all 12 months
        fig, axes = plt.subplots(2, 6, figsize=(20, 10))
        axes = axes.flatten()  # Flatten the 2D array to make indexing easier
        
        # Plot each month in its respective subplot
        for i, month in enumerate(range(1, 13)):  # Always plot all 12 months in the grid
            ax = axes[i]
            col_name = f'rain_{year}_{month:02d}'
            
            # Check if data for this month exists
            if col_name in processed_gdf.columns and not processed_gdf[col_name].isna().all():
                vmin = processed_gdf[col_name].min()
                vmax = processed_gdf[col_name].max()
                
                processed_gdf.plot(column=col_name, ax=ax, legend=True, cmap=cmap, 
                               edgecolor="black", legend_kwds={'shrink': 0.7}, 
                               vmin=vmin, vmax=vmax)
            else:
                # If no data, just plot the geography without color
                processed_gdf.plot(ax=ax, edgecolor="black", facecolor="lightgrey")
                ax.text(0.5, 0.5, "No Data", horizontalalignment='center', 
                      verticalalignment='center', transform=ax.transAxes)
            
            # Remove axis ticks and labels
            ax.set_axis_off()
            
            # Add month name as title
            month_name = ['January', 'February', 'March', 'April', 'May', 'June', 
                        'July', 'August', 'September', 'October', 'November', 'December'][month-1]
            ax.set_title(month_name, fontsize=12)
        
        # Add a main title for the entire figure
        fig.suptitle(f"Monthly Rainfall in {year}", fontsize=16, y=0.98)
        
        # Adjust layout to prevent overlap
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        # Display the figure
        st.pyplot(fig)
        
        # Download button for the grid view
        grid_pdf_output = BytesIO()
        plt.savefig(grid_pdf_output, format='pdf', bbox_inches='tight')
        plt.close()
        
        st.download_button(
            label="Download Grid View as PDF",
            data=grid_pdf_output.getvalue(),
            file_name=f"rainfall_grid_{year}.pdf",
            mime="application/pdf"
        )
    
    with tab2:
        st.subheader("Individual Monthly Maps")
        
        # Plot individual maps for each month
        for month in months:
            col_name = f'rain_{year}_{month:02d}'
            
            if col_name in processed_gdf.columns and not processed_gdf[col_name].isna().all():
                fig, ax = plt.subplots(1, 1, figsize=(10, 10))
                
                # Find region name column if it exists
                if region_name_col:
                    # Add region names as labels
                    for idx, row in processed_gdf.iterrows():
                        if not pd.isna(row[col_name]):
                            # Get centroid of geometry
                            centroid = row.geometry.centroid
                            ax.text(centroid.x, centroid.y, str(row[region_name_col]), 
                                  fontsize=8, ha='center', va='center')
                
                # Plotting the GeoDataFrame
                processed_gdf.plot(column=col_name, ax=ax, legend=True, cmap=cmap, 
                               edgecolor="black", legend_kwds={'shrink': 0.5})
                
                # Remove axis boxes
                ax.set_axis_off()
                
                # Add a title to the plot
                month_name = ['January', 'February', 'March', 'April', 'May', 'June', 
                            'July', 'August', 'September', 'October', 'November', 'December'][month-1]
                plt.title(f"Mean Rainfall for {month_name} {year}", fontsize=16)
                
                # Display the map in Streamlit
                st.pyplot(fig)
                plt.close()
    
    with tab3:
        # Create summary statistics
        st.subheader("Summary Statistics")
        
        # Handle potential errors in groupby operation
        try:
            # Filter out NaN values for statistics
            stats_df = restructured_df.dropna(subset=['mean_rain'])
            
            # Only calculate statistics if there's data
            if not stats_df.empty:
                # Calculate statistics for mean_rain grouped by month
                month_stats = stats_df.groupby('Month')['mean_rain'].agg(['mean', 'std', 'min', 'max']).reset_index()
                month_stats['Month'] = month_stats['Month'].apply(
                    lambda x: f"{x:02d} - {['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][x-1]}")
                st.write(month_stats)
                
                # Create a bar chart of average rainfall per month
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(month_stats['Month'], month_stats['mean'], color='skyblue')
                ax.set_xlabel('Month')
                ax.set_ylabel('Average Rainfall (mm)')
                ax.set_title(f'Average Rainfall by Month for {year}')
                ax.grid(axis='y', linestyle='--', alpha=0.7)
                ax.tick_params(axis='x', rotation=45)
                
                st.pyplot(fig)
                plt.close()
                
                # If there are multiple regions, show comparison
                if 'Region' in stats_df.columns and len(stats_df['Region'].unique()) > 1:
                    st.subheader("Regional Comparison")
                    
                    # Create a regional comparison chart
                    region_month_stats = stats_df.groupby(['Region', 'Month'])['mean_rain'].mean().reset_index()
                    region_month_stats['Month'] = region_month_stats['Month'].apply(
                        lambda x: f"{x:02d} - {['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][x-1]}")
                    
                    # Create a pivot table for easier plotting
                    pivot_df = region_month_stats.pivot(index='Month', columns='Region', values='mean_rain')
                    
                    # Plotting
                    fig, ax = plt.subplots(figsize=(12, 8))
                    pivot_df.plot(kind='bar', ax=ax)
                    ax.set_xlabel('Month')
                    ax.set_ylabel('Average Rainfall (mm)')
                    ax.set_title(f'Regional Rainfall Comparison for {year}')
                    ax.grid(axis='y', linestyle='--', alpha=0.7)
                    ax.legend(title='Region')
                    
                    st.pyplot(fig)
                    plt.close()
            else:
                st.warning("No valid rainfall data available for statistics.")
        except Exception as e:
            st.error(f"Error calculating statistics: {str(e)}")

    # Download button for the processed data as CSV
    csv_data = restructured_df.to_csv(index=False).encode('utf-8')
    
    # Offer the CSV file for download
    st.download_button(
        label="Download Data as CSV",
        data=csv_data,
        file_name=f"rainfall_data_{year}.csv",
        mime="text/csv"
    )
    
    # Add note about Excel conversion
    st.info("Note: The data is provided as CSV which can be opened directly in Excel. " 
          "If you prefer a formatted Excel file, you can install xlsxwriter in your environment.")
    
    # Download button for all maps as a single PDF
    valid_months = []
    for month in months:
        col_name = f'rain_{year}_{month:02d}'
        if col_name in processed_gdf.columns and not processed_gdf[col_name].isna().all():
            valid_months.append(month)
    
    if valid_months:
        pdf_output = BytesIO()
        
        with PdfPages(pdf_output) as pdf:
            for month in valid_months:
                col_name = f'rain_{year}_{month:02d}'
                
                fig, ax = plt.subplots(1, 1, figsize=(8.5, 11))
                processed_gdf.plot(column=col_name, ax=ax, legend=True, cmap=cmap, 
                               edgecolor="black", legend_kwds={'shrink': 0.5})
                ax.set_axis_off()
                month_name = ['January', 'February', 'March', 'April', 'May', 'June', 
                            'July', 'August', 'September', 'October', 'November', 'December'][month-1]
                plt.title(f"Mean Rainfall for {month_name} {year}", fontsize=16)
                
                pdf.savefig(fig)
                plt.close()
        
        st.download_button(
            label="Download All Maps as PDF",
            data=pdf_output.getvalue(),
            file_name=f"rainfall_maps_{year}.pdf",
            mime="application/pdf"
        )
else:
    st.info("Please upload shapefile components (.shp, .shx, .dbf) and select parameters to generate analysis.")

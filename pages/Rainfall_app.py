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

    # Check if the CRS is set, if not, set it manually
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")  # Assuming WGS84; replace with correct CRS if different

    return gdf

# Function to download, unzip, and process CHIRPS data
def process_chirps_data(gdf, year, month, region="africa"):
    try:
        # Define the link for CHIRPS data
        if region == "africa":
            link = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_monthly/tifs/chirps-v2.0.{year}.{month:02d}.tif.gz"
        else:
            link = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/tifs/chirps-v2.0.{year}.{month:02d}.tif.gz"

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
                
                if not overlap:
                    st.warning(f"Shapefile does not overlap with CHIRPS data for {year}-{month:02d}.")
                    if region == "africa":
                        st.info("Trying global dataset instead...")
                        return process_chirps_data(gdf, year, month, region="global")
                    else:
                        gdf[f'rain_{year}_{month:02d}'] = np.nan
                        return gdf
                
                # Display debug info if requested
                if st.session_state.get('debug_mode', False):
                    st.write(f"Raster CRS: {src.crs}")
                    st.write(f"Raster bounds: {src.bounds}")
                    st.write(f"Shapefile CRS: {gdf.crs}")
                    st.write(f"Shapefile bounds: {shapefile_bounds}")
                
                # Reproject shapefile to match CHIRPS data CRS
                gdf_reprojected = gdf.to_crs(src.crs)

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
st.title("CHIRPS Data Analysis and Map Generation")

# Add debug mode toggle
debug_mode = st.sidebar.checkbox("Debug Mode", value=st.session_state['debug_mode'])
st.session_state['debug_mode'] = debug_mode

# Region selection
region = st.sidebar.selectbox("Select Region", ["Africa", "Global"], 
                             help="Africa dataset is lighter and faster if your region is in Africa")

# Upload shapefile components
uploaded_shp = st.file_uploader("Upload .shp file", type="shp")
uploaded_shx = st.file_uploader("Upload .shx file", type="shx")
uploaded_dbf = st.file_uploader("Upload .dbf file", type="dbf")

# Year selection (single)
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

# Colormap selection
cmap = st.selectbox("Select Colormap", ['Blues', 'Greens', 'Reds', 'Purples', 'Oranges', 'YlGnBu', 'cividis', 'plasma', 'viridis'])

# Add a Generate button
generate_button = st.button("Generate Analysis", type="primary")

if uploaded_shp and uploaded_shx and uploaded_dbf and year and generate_button:
    # Load and process the shapefile
    with st.spinner("Loading and processing shapefile..."):
        gdf = load_shapefile(uploaded_shp, uploaded_shx, uploaded_dbf)

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
            processed_gdf = process_chirps_data(processed_gdf, year, month, 
                                               region="africa" if region == "Africa" else "global")
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
    
    for column in rain_columns:
        # Extract year and month from column name
        _, year_str, month_str = column.split('_')
        year_val = int(year_str)
        month_val = int(month_str)
        
        # For each region in the shapefile
        for idx, row in processed_gdf.iterrows():
            region_data = {col: row[col] for col in processed_gdf.columns if not col.startswith('rain_') and col != 'geometry'}
            region_data['Year'] = year_val
            region_data['Month'] = month_val
            region_data['mean_rain'] = row[column]
            restructured_data.append(region_data)
    
    # Create the restructured DataFrame
    restructured_df = pd.DataFrame(restructured_data)
    
    # Display the restructured data
    st.write("Restructured Data (Month, Year, mean_rain format):")
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

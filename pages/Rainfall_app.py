import streamlit as st
import geopandas as gpd
import rasterio
import rasterio.mask
import numpy as np
import os
import requests
import gzip
import shutil
import tempfile
import pandas as pd
from io import BytesIO
from matplotlib import pyplot as plt

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
def process_chirps_data(gdf, year, month):
    # Define the link for CHIRPS data
    link = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_monthly/tifs/chirps-v2.0.{year}.{month:02d}.tif.gz"

    # Download the .tif.gz file
    response = requests.get(link)
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
            # Reproject shapefile to match CHIRPS data CRS
            gdf = gdf.to_crs(src.crs)

            # Mask the CHIRPS data using the shapefile geometry
            out_image, out_transform = rasterio.mask.mask(src, gdf.geometry, crop=True)

            # Flatten the masked array and calculate mean excluding masked values
            mean_rains = []
            for geom in gdf.geometry:
                masked_data, _ = rasterio.mask.mask(src, [geom], crop=True)
                masked_data = masked_data.flatten()
                masked_data = masked_data[masked_data != src.nodata]  # Exclude nodata values
                mean_rains.append(masked_data.mean())

            # Add result as a column with year and month in the name
            gdf[f'rain_{year}_{month:02d}'] = mean_rains

    return gdf

# Streamlit app layout
st.title("CHIRPS Data Analysis and Map Generation")

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
    
    processed_gdf = gdf.copy()
    
    # Process CHIRPS data for each selected month
    for month in months:
        with st.spinner(f"Processing CHIRPS data for {year}-{month:02d}..."):
            processed_gdf = process_chirps_data(processed_gdf, year, month)
    
    st.success("CHIRPS data processed successfully!")

    # Get the rainfall columns
    rain_columns = [col for col in processed_gdf.columns if col.startswith('rain_')]
    
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
    tab1, tab2, tab3 = st.tabs(["Monthly Grid View", "Individual Maps", "Combined Data"])
    
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
            if col_name in processed_gdf.columns:
                processed_gdf.plot(column=col_name, ax=ax, legend=True, cmap=cmap, 
                             edgecolor="black", legend_kwds={'shrink': 0.7})
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
    
    with tab1:
        # Plot individual maps for each month
        for month in months:
            col_name = f'rain_{year}_{month:02d}'
            
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
    
    with tab2:
        # Create summary statistics
        st.subheader("Summary Statistics")
        
        # Calculate statistics for mean_rain grouped by month
        month_stats = restructured_df.groupby('Month')['mean_rain'].agg(['mean', 'std', 'min', 'max']).reset_index()
        month_stats['Month'] = month_stats['Month'].apply(lambda x: f"{x:02d} - {['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][x-1]}")
        st.write(month_stats)
        
        # Create a bar chart of average rainfall per month
        avg_rain = month_stats['mean'].tolist()
        month_labels = month_stats['Month'].tolist()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(month_labels, avg_rain, color='skyblue')
        ax.set_xlabel('Month')
        ax.set_ylabel('Average Rainfall (mm)')
        ax.set_title(f'Average Rainfall by Month for {year}')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.tick_params(axis='x', rotation=45)
        
        st.pyplot(fig)

    # Download button for the processed data as CSV instead of Excel
    # (To avoid xlsxwriter dependency issues)
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
    if len(months) > 0:
        # Create a PDF with all maps
        from matplotlib.backends.backend_pdf import PdfPages
        
        pdf_output = BytesIO()
        
        with PdfPages(pdf_output) as pdf:
            for month in months:
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

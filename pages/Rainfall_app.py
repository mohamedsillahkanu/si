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

# Month selection (multiple)
months = st.multiselect("Select Months", 
                      options=list(range(1, 13)),
                      default=[1],
                      format_func=lambda x: f"{x:02d} - {['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][x-1]}")

# Colormap selection
cmap = st.selectbox("Select Colormap", ['Blues', 'Greens', 'Reds', 'Purples', 'Oranges', 'YlGnBu', 'cividis', 'plasma', 'viridis'])

if uploaded_shp and uploaded_shx and uploaded_dbf and year and months:
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
    
    # Display the data without geometry column
    display_df = processed_gdf.drop(columns=['geometry'])
    st.write(display_df)

    # Create tabs for different visualizations
    tab1, tab2 = st.tabs(["Individual Maps", "Combined Data"])
    
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
        
        # Calculate statistics for each rainfall column
        stats_df = pd.DataFrame()
        for col in rain_columns:
            stats_df[col] = [
                processed_gdf[col].mean(),
                processed_gdf[col].std(),
                processed_gdf[col].min(),
                processed_gdf[col].max()
            ]
        
        stats_df.index = ['Mean', 'Std Dev', 'Min', 'Max']
        st.write(stats_df)
        
        # Create a bar chart of average rainfall per month
        avg_rain = [processed_gdf[col].mean() for col in rain_columns]
        month_labels = [f"{month:02d}" for month in months]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(month_labels, avg_rain, color='skyblue')
        ax.set_xlabel('Month')
        ax.set_ylabel('Average Rainfall (mm)')
        ax.set_title(f'Average Rainfall by Month for {year}')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        st.pyplot(fig)

    # Download button for the processed data as Excel
    output_excel = BytesIO()
    
    # Create a DataFrame without the geometry column for Excel export
    export_df = processed_gdf.drop(columns=['geometry'])
    
    # Write to Excel with formatting
    with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
        export_df.to_excel(writer, sheet_name=f'Rainfall_{year}', index=False)
        
        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets[f'Rainfall_{year}']
        
        # Add a header format
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1})
        
        # Write the column headers with the header format
        for col_num, value in enumerate(export_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
        # Set the column width based on the longest string in each column
        for i, col in enumerate(export_df.columns):
            max_len = max(
                export_df[col].astype(str).map(len).max(),
                len(str(col))
            ) + 2
            worksheet.set_column(i, i, max_len)
        
        # Add a number format for the rainfall data columns
        num_format = workbook.add_format({'num_format': '0.00'})
        for i, col in enumerate(export_df.columns):
            if col.startswith('rain_'):
                worksheet.set_column(i, i, None, num_format)
    
    # Offer the Excel file for download
    st.download_button(
        label="Download Data as Excel",
        data=output_excel.getvalue(),
        file_name=f"rainfall_data_{year}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
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

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
from io import BytesIO
from matplotlib import pyplot as plt
import pandas as pd

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

            gdf['mean_rain'] = mean_rains

    return gdf

# Streamlit app layout
st.title("CHIRPS Data Analysis and Map Generation")

# Upload shapefile components
uploaded_shp = st.file_uploader("Upload .shp file", type="shp")
uploaded_shx = st.file_uploader("Upload .shx file", type="shx")
uploaded_dbf = st.file_uploader("Upload .dbf file", type="dbf")

# Year and month selection
years = st.multiselect("Select Years", range(1981, 2025))
months = st.multiselect("Select Months", range(1, 13))

# Ensure that the shapefile and other inputs are provided
if uploaded_shp and uploaded_shx and uploaded_dbf and years and months:
    # Load and process the shapefile
    with st.spinner("Loading and processing shapefile..."):
        gdf = load_shapefile(uploaded_shp, uploaded_shx, uploaded_dbf)

    st.success("Shapefile loaded successfully!")

    # Display the GeoDataFrame
    st.write("Here is a preview of your shapefile:")
    st.dataframe(gdf)

    # Let user select which text column to use
    text_columns = gdf.select_dtypes(include=['object']).columns
    if len(text_columns) == 0:
        st.error("No text columns found in the shapefile. Please upload a valid shapefile.")
    else:
        text_column = st.selectbox("Select a text column to use for naming:", text_columns)

        # Initialize a list to collect DataFrames
        all_data = []

        # Process CHIRPS data for each year and month
        for year in years:
            for month in months:
                with st.spinner(f"Processing CHIRPS data for {year}-{month:02d}..."):
                    df = process_chirps_data(gdf, year, month)
                    df['Year'] = year
                    df['Month'] = month
                    all_data.append(df)

        # Concatenate all DataFrames into a single DataFrame
        combined_df = pd.concat(all_data, ignore_index=True)

        st.success("CHIRPS data processed successfully!")

        # Display the mean rainfall data
        st.write(combined_df[['geometry', 'mean_rain', 'Year', 'Month', text_column]])

        # Line plot for each unique value in the text column
        st.subheader(f"Line Plots for Each {text_column}")

        # Create separate figures for each unique value in the detected text column
        for name in combined_df[text_column].unique():
            name_data = combined_df[combined_df[text_column] == name]
            mean_rain_by_month = name_data.groupby(['Year', 'Month'])['mean_rain'].mean().reset_index()

            fig, ax = plt.subplots(figsize=(12, 8))
            for year in years:
                year_data = mean_rain_by_month[mean_rain_by_month['Year'] == year]
                ax.plot(year_data['Month'], year_data['mean_rain'], marker='o', label=f'Year {year}')
            
            ax.set_title(f"Mean Rainfall over Months for {name}")
            ax.set_xlabel('Month')
            ax.set_ylabel('mean_rain')
            ax.legend(loc='best')
            ax.annotate(name, xy=(0.5, 1.05), xycoords='axes fraction', ha='center', fontsize=14, fontweight='bold')
            st.pyplot(fig)

        # Optionally, add download functionality for each line plot
        if years and months:
            st.subheader("Download Line Plot Images")

            for name in combined_df[text_column].unique():
                name_data = combined_df[combined_df[text_column] == name]
                mean_rain_by_month = name_data.groupby(['Year', 'Month'])['mean_rain'].mean().reset_index()

                fig, ax = plt.subplots(figsize=(12, 8))
                for year in years:
                    year_data = mean_rain_by_month[mean_rain_by_month['Year'] == year]
                    ax.plot(year_data['Month'], year_data['mean_rain'], marker='o', label=f'Year {year}')
                
                ax.set_title(f"Mean Rainfall over Months for {name}")
                ax.set_xlabel('Month')
                ax.set_ylabel('mean_rain')
                ax.legend(loc='best')
                ax.annotate(name, xy=(0.5, 1.05), xycoords='axes fraction', ha='center', fontsize=14, fontweight='bold')

                # Save the plot to a BytesIO object for downloading
                line_plot_output = BytesIO()
                fig.savefig(line_plot_output, format='png')
                st.download_button(label=f"Download Line Plot for {name}",
                                   data=line_plot_output.getvalue(),
                                   file_name=f"line_plot_{name}.png",
                                   mime="image/png")

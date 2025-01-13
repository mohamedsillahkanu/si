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

# Function to check if a file exists on GitHub
def check_file_exists(url):
    response = requests.head(url)
    return response.status_code == 200

# Function to download and load shapefiles from GitHub
def download_shapefile(github_link, admin_level):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Download shapefile components from GitHub
        components = ['.shp', '.shx', '.dbf']
        for ext in components:
            url = f"{github_link}/admin_{admin_level}{ext}"
            response = requests.get(url)
            with open(os.path.join(tmpdir, f"file{ext}"), "wb") as f:
                f.write(response.content)

        # Load the shapefile using GeoPandas
        shapefile_path = os.path.join(tmpdir, "file.shp")
        gdf = gpd.read_file(shapefile_path)

    # Check if CRS is set, if not, set it manually
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")  # Assuming WGS84; replace with correct CRS if different

    return gdf

# Function to process CHIRPS data
def process_chirps_data(gdf, year, month):
    link = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_monthly/tifs/chirps-v2.0.{year}.{month:02d}.tif.gz"
    response = requests.get(link)
    with tempfile.TemporaryDirectory() as tmpdir:
        zipped_file_path = os.path.join(tmpdir, "chirps.tif.gz")
        unzipped_file_path = os.path.join(tmpdir, "chirps.tif")

        with open(zipped_file_path, "wb") as f:
            f.write(response.content)

        with gzip.open(zipped_file_path, "rb") as f_in:
            with open(unzipped_file_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        with rasterio.open(unzipped_file_path) as src:
            gdf = gdf.to_crs(src.crs)
            mean_rains = []
            for geom in gdf.geometry:
                masked_data, _ = rasterio.mask.mask(src, [geom], crop=True)
                masked_data = masked_data.flatten()
                masked_data = masked_data[masked_data != src.nodata]
                mean_rains.append(masked_data.mean())

            gdf['mean_rain'] = mean_rains
    return gdf

# Streamlit app layout
st.title("Dynamic CHIRPS Data Analysis and Map Generation")

# Country and admin level dropdowns
country = st.selectbox("Select Country", ["Sierra Leone", "Guinea"])
admin_level = None
github_links = {
    "Sierra Leone": "https://github.com/yourrepo/sierra_leone_shapefiles",
    "Guinea": "https://raw.githubusercontent.com/mohamedsillahkanu/si/6d9453ea42ce867562ee71a3f59d8aa5dcc23b7b/shapefiles/Guinea"
}

if country:
    admin_level = st.selectbox("Select Admin Level", [1, 2, 3])
    github_link = github_links[country]

    # Validate admin level
    shapefile_url = f"{github_link}/admin_{admin_level}.shp"
    if check_file_exists(shapefile_url):
        # Load and process the shapefile
        with st.spinner("Loading and processing shapefile..."):
            gdf = download_shapefile(github_link, admin_level)
        st.success(f"{country} shapefile for Admin Level {admin_level} loaded successfully!")

        # Year and month selection
        year = st.selectbox("Select Year", range(1981, 2025))
        month = st.selectbox("Select Month", range(1, 13))

        # Colormap selection
        cmap = st.selectbox("Select Colormap", ['Blues', 'Greens', 'Reds', 'Purples', 'Oranges', 'YlGnBu', 'cividis', 'plasma', 'viridis'])

        # Process CHIRPS data
        with st.spinner("Processing CHIRPS data..."):
            gdf = process_chirps_data(gdf, year, month)
        st.success("CHIRPS data processed successfully!")

        # Display the mean rainfall data
        st.write(gdf[['geometry', 'mean_rain']])

        # Plot the map
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        gdf.plot(column='mean_rain', ax=ax, legend=True, cmap=cmap, edgecolor="black", legend_kwds={'shrink': 0.5})
        ax.set_axis_off()
        plt.title(f"Mean Rainfall for {year}-{month:02d}", fontsize=16)
        st.pyplot(fig)

        # Download buttons
        output_csv = BytesIO()
        gdf.to_csv(output_csv)
        st.download_button(label="Download Mean Rainfall Data",
                           data=output_csv.getvalue(),
                           file_name=f"mean_rainfall_{year}_{month:02d}.csv",
                           mime="text/csv")

        image_output = BytesIO()
        fig.savefig(image_output, format='png')
        st.download_button(label="Download Map Image",
                           data=image_output.getvalue(),
                           file_name=f"mean_rainfall_{year}_{month:02d}.png",
                           mime="image/png")
    else:
        st.error(f"{country} does not have Admin Level {admin_level}. Please select another.")

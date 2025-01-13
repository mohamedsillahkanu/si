import streamlit as st
import geopandas as gpd
import rasterio
import rasterio.mask
import requests
import tempfile
from io import BytesIO
from matplotlib import pyplot as plt

# Function to check if a file exists on GitHub
def check_file_exists(url):
    response = requests.head(url)
    return response.status_code == 200

# Function to download and load shapefiles from GitHub
def download_shapefile(github_link, country_code, admin_level):
    with tempfile.TemporaryDirectory() as tmpdir:
        file_base = f"gadm41_{country_code}_{admin_level}"
        components = ['.shp', '.shx', '.dbf']

        # Download each component of the shapefile
        for ext in components:
            url = f"{github_link}/{file_base}{ext}"
            st.write(f"Attempting to download: {url}")  # Debugging output
            response = requests.get(url)
            if response.status_code == 200:
                with open(os.path.join(tmpdir, f"{file_base}{ext}"), "wb") as f:
                    f.write(response.content)
            else:
                st.error(f"Failed to download {url}. HTTP Status Code: {response.status_code}")
                raise FileNotFoundError(f"File {file_base}{ext} not found at {url}.")

        # Load the shapefile using GeoPandas
        shapefile_path = os.path.join(tmpdir, f"{file_base}.shp")
        try:
            gdf = gpd.read_file(shapefile_path)
        except Exception as e:
            st.error(f"Error loading shapefile: {e}")
            raise e

    # Check CRS; set if missing
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")  # Assuming WGS84

    return gdf

# Function to process CHIRPS rainfall data
def process_chirps_data(gdf, year, month):
    link = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_monthly/tifs/chirps-v2.0.{year}.{month:02d}.tif.gz"
    response = requests.get(link)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Save the .tif.gz file
        zipped_file_path = f"{tmpdir}/chirps.tif.gz"
        with open(zipped_file_path, "wb") as f:
            f.write(response.content)

        # Unzip the file
        unzipped_file_path = f"{tmpdir}/chirps.tif"
        with rasterio.open(zipped_file_path, "r") as zipped_src:
            with rasterio.open(unzipped_file_path, "wb") as unzipped_dst:
                unzipped_dst.write(zipped_src.read())

        # Open the unzipped .tif file
        with rasterio.open(unzipped_file_path) as src:
            # Reproject the shapefile to match CHIRPS CRS
            gdf = gdf.to_crs(src.crs)
            mean_rains = []

            for geom in gdf.geometry:
                # Mask the CHIRPS data using shapefile geometry
                masked_data, _ = rasterio.mask.mask(src, [geom], crop=True)
                masked_data = masked_data.flatten()
                masked_data = masked_data[masked_data != src.nodata]  # Remove nodata values
                mean_rains.append(masked_data.mean())

            gdf["mean_rain"] = mean_rains

    return gdf

# Streamlit app layout
st.title("CHIRPS Rainfall Data Analysis and Map Generation")

# Define GitHub links and country codes
github_links = {
    "Sierra Leone": {
        "link": "https://raw.githubusercontent.com/mohamedsillahkanu/si/554bb45b390b5b2fb1de04540f1c8202a3510456/shapefiles/Sierra%20Leone",
        "code": "SLE"
    },
    "Guinea": {
        "link": "https://raw.githubusercontent.com/mohamedsillahkanu/si/6d9453ea42ce867562ee71a3f59d8aa5dcc23b7b/shapefiles/Guinea",
        "code": "GIN"
    }
}

# Country and admin level selection
country = st.selectbox("Select Country", list(github_links.keys()))
admin_level = st.selectbox("Select Admin Level", [1, 2, 3])

# Year and month selection
year = st.selectbox("Select Year", range(1981, 2025))
month = st.selectbox("Select Month", range(1, 13))

if country and admin_level:
    github_link = github_links[country]["link"]
    country_code = github_links[country]["code"]

    file_base = f"gadm41_{country_code}_{admin_level}"
    shapefile_url = f"{github_link}/{file_base}.shp"

    if check_file_exists(shapefile_url):
        with st.spinner("Downloading and loading shapefile..."):
            try:
                gdf = download_shapefile(github_link, country_code, admin_level)
                st.success(f"{country} Admin Level {admin_level} shapefile loaded successfully!")
            except FileNotFoundError as e:
                st.error(str(e))
                st.stop()

        with st.spinner("Processing CHIRPS rainfall data..."):
            try:
                gdf = process_chirps_data(gdf, year, month)
                st.success("CHIRPS rainfall data processed successfully!")
            except Exception as e:
                st.error(f"Error processing CHIRPS data: {str(e)}")
                st.stop()

        # Display results
        st.write(gdf[["geometry", "mean_rain"]])

        # Plot the map
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        gdf.plot(column="mean_rain", ax=ax, legend=True, cmap="Blues", edgecolor="black")
        ax.set_axis_off()
        plt.title(f"Mean Rainfall for {country} (Admin Level {admin_level}) - {year}-{month:02d}", fontsize=16)
        st.pyplot(fig)

        # Download options
        csv_data = BytesIO()
        gdf.to_csv(csv_data)
        st.download_button(
            label="Download Rainfall Data as CSV",
            data=csv_data.getvalue(),
            file_name=f"rainfall_{country_code}_{admin_level}_{year}_{month:02d}.csv",
            mime="text/csv"
        )
    else:
        st.error(f"The shapefile for {country} Admin Level {admin_level} does not exist. Please select another.")

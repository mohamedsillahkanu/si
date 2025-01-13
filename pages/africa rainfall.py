import streamlit as st
import geopandas as gpd
import rasterio
import os
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
        # Define the file name format
        file_base = f"gadm41_{country_code}_{admin_level}"
        components = ['.shp', '.shx', '.dbf']

        # Download each component of the shapefile
        for ext in components:
            url = f"{github_link}/{file_base}{ext}"
            response = requests.get(url)
            if response.status_code == 200:
                with open(os.path.join(tmpdir, f"{file_base}{ext}"), "wb") as f:
                    f.write(response.content)
            else:
                raise FileNotFoundError(f"File {file_base}{ext} not found on GitHub.")

        # Load the shapefile using GeoPandas
        shapefile_path = os.path.join(tmpdir, f"{file_base}.shp")
        gdf = gpd.read_file(shapefile_path)

    # Check CRS; set if missing
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")  # Assuming WGS84

    return gdf

# Streamlit app layout
st.title("Dynamic CHIRPS Data Analysis and Map Generation")

# Define GitHub links and country codes
github_links = {
    "Sierra Leone": {"link": "https://raw.githubusercontent.com/mohamedsillahkanu/si/6d9453ea42ce867562ee71a3f59d8aa5dcc23b7b/shapefiles/", "code": "SLE"},
    "Guinea": {"link": "https://raw.githubusercontent.com/mohamedsillahkanu/si/6d9453ea42ce867562ee71a3f59d8aa5dcc23b7b/shapefiles/Guinea", "code": "GIN"}
}

# Country and admin level selection
country = st.selectbox("Select Country", list(github_links.keys()))
admin_level = st.selectbox("Select Admin Level", [1, 2, 3])

if country and admin_level:
    github_link = github_links[country]["link"]
    country_code = github_links[country]["code"]

    # Validate the existence of the shapefile
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

        # Display the GeoDataFrame
        st.write(gdf)

        # Simple visualization
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        gdf.plot(ax=ax, edgecolor="black")
        ax.set_axis_off()
        plt.title(f"{country} - Admin Level {admin_level}")
        st.pyplot(fig)

        # Download GeoDataFrame as CSV
        csv_data = BytesIO()
        gdf.to_csv(csv_data)
        st.download_button(
            label="Download Shapefile Data as CSV",
            data=csv_data.getvalue(),
            file_name=f"{file_base}.csv",
            mime="text/csv"
        )
    else:
        st.error(f"The shapefile for {country} Admin Level {admin_level} does not exist. Please select another.")

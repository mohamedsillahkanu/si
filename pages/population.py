import streamlit as st
import geopandas as gpd
import rasterio
import rasterio.mask
import numpy as np
import os
import tempfile
from io import BytesIO
from matplotlib import pyplot as plt
import requests

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

# Function to process raster data
def process_raster_data(gdf, raster_path):
    # Ensure the raster file exists
    if not os.path.exists(raster_path):
        raise FileNotFoundError(f"Raster file not found: {raster_path}")

    # Validate the file size
    file_size = os.path.getsize(raster_path)
    if file_size == 0:
        raise ValueError(f"Raster file is empty: {raster_path}")

    try:
        with rasterio.open(raster_path) as src:
            # Reproject shapefile to match raster data CRS
            gdf = gdf.to_crs(src.crs)

            # Mask the raster data using the shapefile geometry
            mean_values = []
            for geom in gdf.geometry:
                masked_data, _ = rasterio.mask.mask(src, [geom], crop=True)
                masked_data = masked_data.flatten()
                masked_data = masked_data[masked_data != src.nodata]  # Exclude nodata values
                mean_values.append(masked_data.mean())

            gdf['mean_value'] = mean_values

    except rasterio.errors.RasterioIOError as e:
        raise RuntimeError(f"Failed to open or process the raster file: {e}")

    return gdf

# Streamlit app layout
st.title("SLE Population Data Analysis and Map Generation")

# Upload shapefile components
uploaded_shp = st.file_uploader("Upload .shp file", type="shp")
uploaded_shx = st.file_uploader("Upload .shx file", type="shx")
uploaded_dbf = st.file_uploader("Upload .dbf file", type="dbf")

# Option to download the raster or upload manually
raster_path = "https://github.com/mohamedsillahkanu/si/raw/7740ae4363176a51346ba54459add49a3102aa52/SLE_population_v2_0_gridded.tif"
uploaded_raster = st.file_uploader("Upload the raster file (.tif) or use the default linked file", type="tif")

if uploaded_shp and uploaded_shx and uploaded_dbf:
    # Load and process the shapefile
    with st.spinner("Loading and processing shapefile..."):
        gdf = load_shapefile(uploaded_shp, uploaded_shx, uploaded_dbf)

    st.success("Shapefile loaded successfully!")

    if uploaded_raster:
        # Save uploaded raster file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tif") as tmp_raster:
            tmp_raster.write(uploaded_raster.read())
            raster_file_path = tmp_raster.name
        st.success(f"Raster file uploaded successfully to {raster_file_path}")
    else:
        # Download the raster file from the URL
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".tif") as tmp_raster:
                raster_response = requests.get(raster_path, timeout=30)
                raster_response.raise_for_status()
                tmp_raster.write(raster_response.content)
                raster_file_path = tmp_raster.name
            st.success(f"Raster file downloaded successfully to {raster_file_path}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to download raster file: {e}")
            st.stop()

    # Debugging: Check raster file path and size
    if os.path.exists(raster_file_path):
        file_size = os.path.getsize(raster_file_path)
        st.write(f"Raster file path: {raster_file_path}")
        st.write(f"File size: {file_size} bytes")
    else:
        st.error(f"Raster file not found: {raster_file_path}")
        st.stop()

    # Process the raster data
    try:
        with st.spinner("Processing raster data..."):
            gdf = process_raster_data(gdf, raster_file_path)
        st.success("Raster data processed successfully!")
    except Exception as e:
        st.error(f"An error occurred while processing the raster data: {e}")
        st.stop()

    # Display the mean population data
    st.write(gdf[['geometry', 'mean_value']])

    # Colormap selection
    cmap = st.selectbox("Select Colormap", ['Blues', 'Greens', 'Reds', 'Purples', 'Oranges', 'YlGnBu', 'cividis', 'plasma', 'viridis'])

    # Plot the map
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    gdf.plot(column='mean_value', ax=ax, legend=True, cmap=cmap, edgecolor="black", legend_kwds={'shrink': 0.5})
    ax.set_axis_off()
    plt.title("Mean Population Data", fontsize=16)
    st.pyplot(fig)

    # Download button for the processed data
    output_csv = BytesIO()
    gdf.to_csv(output_csv)
    st.download_button(label="Download Mean Population Data",
                       data=output_csv.getvalue(),
                       file_name="mean_population_data.csv",
                       mime="text/csv")

    # Download button for the image
    image_output = BytesIO()
    fig.savefig(image_output, format='png')
    st.download_button(label="Download Map Image",
                       data=image_output.getvalue(),
                       file_name="mean_population_data.png",
                       mime="image/png")
else:
    st.info("Please upload all components of the shapefile to proceed.")

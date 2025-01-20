import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import numpy as np

st.title("Interactive Health Facility Map Generator")

# Upload shapefiles
st.header("Upload Shapefiles")
shp_file = st.file_uploader("Upload .shp file", type=["shp"], key="shp")
shx_file = st.file_uploader("Upload .shx file", type=["shx"], key="shx")
dbf_file = st.file_uploader("Upload .dbf file", type=["dbf"], key="dbf")

# Upload data file (Excel or CSV)
st.header("Upload Data File")
data_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "xls", "csv"], key="data")

# Check if all shapefile components and data file are uploaded
if shp_file and shx_file and dbf_file and data_file:
    # Read shapefile
    with open("temp.shp", "wb") as f:
        f.write(shp_file.read())
    with open("temp.shx", "wb") as f:
        f.write(shx_file.read())
    with open("temp.dbf", "wb") as f:
        f.write(dbf_file.read())
    shapefile = gpd.read_file("temp.shp")

    # Read data file
    file_extension = data_file.name.split(".")[-1].lower()
    if file_extension in ["xlsx", "xls"]:
        coordinates_data = pd.read_excel(data_file)
    elif file_extension == "csv":
        coordinates_data = pd.read_csv(data_file)

    # User selects longitude and latitude columns
    st.header("Select Coordinate Columns")
    longitude_column = st.selectbox("Select Longitude Column", coordinates_data.columns, key="longitude")
    latitude_column = st.selectbox("Select Latitude Column", coordinates_data.columns, key="latitude")

    # Convert selected columns to numeric
    coordinates_data[longitude_column] = pd.to_numeric(coordinates_data[longitude_column], errors='coerce')
    coordinates_data[latitude_column] = pd.to_numeric(coordinates_data[latitude_column], errors='coerce')

    # Drop rows with invalid or missing coordinates
    coordinates_data = coordinates_data.dropna(subset=[longitude_column, latitude_column])
    coordinates_data = coordinates_data[
        (coordinates_data[longitude_column].between(-180, 180)) &
        (coordinates_data[latitude_column].between(-90, 90))
    ]

    # User provides map customization options
    st.header("Map Customization")
    map_title = st.text_input("Enter the title of the map", "Health Facility Coordinates", key="map_title")
    
    # Predefined background color options
    background_colors = ["white", "black", "gray", "lightgray"]
    background_color = st.selectbox("Select background color of the map", background_colors, key="background")

    # Predefined point color options
    point_colors = ["lightblue", "lightgreen", "yellow", "brown", "red", "blue", "purple"]
    point_color = st.selectbox("Select point color", point_colors, key="points")

    # Convert DataFrame to GeoDataFrame
    geometry = [Point(xy) for xy in zip(coordinates_data[longitude_column], coordinates_data[latitude_column])]
    coordinates_gdf = gpd.GeoDataFrame(coordinates_data, geometry=geometry, crs="EPSG:4326")

    # Ensure shapefile CRS is set or transformed to EPSG:4326
    if shapefile.crs is None:
        shapefile.set_crs(epsg=4326, inplace=True)
    else:
        shapefile = shapefile.to_crs(epsg=4326)

    # Plot the map
    fig, ax = plt.subplots(figsize=(12, 8))
    shapefile.plot(ax=ax, color=background_color, edgecolor='black', linewidth=0.5)
    coordinates_gdf.plot(ax=ax, color=point_color, markersize=50, alpha=0.7)

    plt.title(map_title, fontsize=20, fontweight='bold')
    plt.axis('off')

    # Display the map
    st.pyplot(fig)

    # Provide download option for the map
    output_path = "health_facility_coordinates.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    with open(output_path, "rb") as file:
        st.download_button(label="Download Map as PNG", data=file, file_name="health_facility_coordinates.png", mime="image/png")

else:
    st.write("Please upload all required files to generate the map.")

import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import numpy as np
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap

# Page config and theming
st.set_page_config(layout="wide", page_title="Health Facility Map Generator")
st.markdown("""
    <style>
    .main {
        background-color: #F8F9FA;
    }
    .block-container {
        padding: 2rem 3rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("\U0001F5FA️ Health Facility Distribution Mapper")
st.markdown("""
Upload your **administrative boundary shapefiles** and **health facility dataset** to generate a beautiful, interactive map.
""")

# Upload Section
col1, col2 = st.columns(2)
with col1:
    st.header("Step 1: Upload Shapefiles")
    shp_file = st.file_uploader("Upload `.shp` file", type=["shp"], key="shp")
    shx_file = st.file_uploader("Upload `.shx` file", type=["shx"], key="shx")
    dbf_file = st.file_uploader("Upload `.dbf` file", type=["dbf"], key="dbf")

with col2:
    st.header("Step 2: Upload Facility Data")
    facility_file = st.file_uploader("Upload `.xlsx` file with coordinates", type=["xlsx"], key="facility")

# Ensure all files are uploaded
if all([shp_file, shx_file, dbf_file, facility_file]):
    try:
        # Save shapefile components temporarily
        with open("temp.shp", "wb") as f: f.write(shp_file.read())
        with open("temp.shx", "wb") as f: f.write(shx_file.read())
        with open("temp.dbf", "wb") as f: f.write(dbf_file.read())
        shapefile = gpd.read_file("temp.shp")

        # Load Excel data
        coordinates_data = pd.read_excel(facility_file)
        st.subheader("\U0001F4CA Data Preview")
        st.dataframe(coordinates_data.head())

        # Map customization UI
        st.header("\U0001F527 Step 3: Customize Map")
        col3, col4, col5 = st.columns(3)

        with col3:
            longitude_col = st.selectbox("Select Longitude Column", coordinates_data.columns)
            latitude_col = st.selectbox("Select Latitude Column", coordinates_data.columns)

        with col4:
            map_title = st.text_input("Map Title", "Health Facility Distribution")
            point_size = st.slider("Point Size", 10, 200, 50)
            point_alpha = st.slider("Point Transparency", 0.1, 1.0, 0.7)

        with col5:
            background_color = st.selectbox("Map Background", ["white", "lightgray", "beige", "lightblue"])
            point_color = st.selectbox("Facility Point Color", ["#47B5FF", "red", "green", "purple", "orange"])

        # Drop missing and invalid coordinates
        coordinates_data = coordinates_data.dropna(subset=[longitude_col, latitude_col])
        coordinates_data = coordinates_data[
            (coordinates_data[longitude_col].between(-180, 180)) &
            (coordinates_data[latitude_col].between(-90, 90))
        ]

        if coordinates_data.empty:
            st.error("No valid coordinates found.")
            st.stop()

        # Convert to GeoDataFrame
        geometry = [Point(xy) for xy in zip(coordinates_data[longitude_col], coordinates_data[latitude_col])]
        coordinates_gdf = gpd.GeoDataFrame(coordinates_data, geometry=geometry, crs="EPSG:4326")

        # Ensure same CRS
        if shapefile.crs is None:
            shapefile = shapefile.set_crs(epsg=4326)
        else:
            shapefile = shapefile.to_crs(epsg=4326)

        # Plotting map
        fig, ax = plt.subplots(figsize=(15, 10))
        shapefile.plot(ax=ax, color=background_color, edgecolor='black', linewidth=0.5)

        bounds = shapefile.total_bounds
        mid_y = np.mean([bounds[1], bounds[3]])
        aspect = 1 / np.cos(np.radians(mid_y)) if -90 < mid_y < 90 else 1
        ax.set_aspect(aspect)

        coordinates_gdf.plot(ax=ax, color=point_color, markersize=point_size, alpha=point_alpha)

        # Title and axis
        plt.title(map_title, fontsize=20, pad=20)
        plt.axis('off')

        # Map summary
        stats = (
            f"Total Facilities: {len(coordinates_data)}\n"
            f"Longitude: {coordinates_data[longitude_col].min():.2f}° to {coordinates_data[longitude_col].max():.2f}°\n"
            f"Latitude: {coordinates_data[latitude_col].min():.2f}° to {coordinates_data[latitude_col].max():.2f}°"
        )
        plt.figtext(0.02, 0.02, stats, fontsize=8, bbox=dict(facecolor='white', alpha=0.8))

        # Show map
        st.pyplot(fig)

        # Download buttons
        col6, col7 = st.columns(2)
        with col6:
            plt.savefig("health_facility_map.png", dpi=300, bbox_inches='tight')
            with open("health_facility_map.png", "rb") as f:
                st.download_button("\U0001F4BE Download Map (PNG)", f, file_name="health_facility_map.png", mime="image/png")

        with col7:
            csv = coordinates_data.to_csv(index=False)
            st.download_button("\U0001F4C2 Download Processed Data (CSV)", csv, file_name="processed_coordinates.csv", mime="text/csv")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.warning("\U0001F4E5 Please upload all required files to proceed.")
    st.subheader("\U0001F4D6 Expected Excel Format")
    st.markdown("""
    Your Excel file should include:
    - **Longitude column** (e.g., `w_long`)
    - **Latitude column** (e.g., `w_lat`)
    
    Coordinates must be in **decimal degrees** format.
    """)

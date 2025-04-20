import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import numpy as np

st.set_page_config(layout="wide", page_title="Health Facility Map Generator")

st.title("🗺️ Health Facility Distribution Map")
st.markdown("Upload administrative shapefiles and health facility data to generate a custom facility distribution map.")

# ────────── Upload Section ──────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Upload Shapefiles")
    shp_file = st.file_uploader("Upload `.shp` file", type=["shp"])
    shx_file = st.file_uploader("Upload `.shx` file", type=["shx"])
    dbf_file = st.file_uploader("Upload `.dbf` file", type=["dbf"])

with col2:
    st.subheader("🏥 Upload Facility Data")
    facility_file = st.file_uploader("Upload facility data file", type=["xlsx", "xls", "csv"])

# ────────── Check All Files ──────────
if all([shp_file, shx_file, dbf_file, facility_file]):
    try:
        # Save and read shapefiles
        with open("temp.shp", "wb") as f: f.write(shp_file.read())
        with open("temp.shx", "wb") as f: f.write(shx_file.read())
        with open("temp.dbf", "wb") as f: f.write(dbf_file.read())
        shapefile = gpd.read_file("temp.shp")

        # Read facility data based on file type
        file_extension = facility_file.name.split('.')[-1].lower()
        if file_extension in ['xlsx', 'xls']:
            facility_data = pd.read_excel(facility_file)
        elif file_extension == 'csv':
            facility_data = pd.read_csv(facility_file)
        else:
            st.error("Unsupported file format.")
            st.stop()

        st.subheader("🔍 Preview of Health Facility Data")
        st.dataframe(facility_data.head())

        # ────────── Map Customization ──────────
        st.header("🎨 Map Customization Options")
        col3, col4, col5 = st.columns(3)

        # Try to detect lat/long columns automatically
        lat_cols = [col for col in facility_data.columns if any(s in col.lower() for s in ['lat', 'latitude', 'y_coord'])]
        long_cols = [col for col in facility_data.columns if any(s in col.lower() for s in ['lon', 'long', 'longitude', 'x_coord'])]

        with col3:
            # Use detected column if available, otherwise default to first column
            default_long_index = 0
            if long_cols and long_cols[0] in facility_data.columns:
                default_long_index = facility_data.columns.get_loc(long_cols[0])
            
            longitude_col = st.selectbox("Select Longitude Column", facility_data.columns, index=default_long_index)
            
            default_lat_index = 0
            if lat_cols and lat_cols[0] in facility_data.columns:
                default_lat_index = facility_data.columns.get_loc(lat_cols[0])
                
            latitude_col = st.selectbox("Select Latitude Column", facility_data.columns, index=default_lat_index)

        with col4:
            map_title = st.text_input("Map Title", "Health Facility Distribution")
            point_size = st.slider("Point Size", 10, 200, 50)
            point_alpha = st.slider("Point Transparency", 0.1, 1.0, 0.7)

        with col5:
            background_color = st.selectbox("Background Color", ["white", "lightgray", "beige", "lightblue"])
            point_color = st.selectbox("Facility Point Color", ["#47B5FF", "red", "green", "purple", "orange"])

        # ────────── Clean Coordinates ──────────
        facility_data[longitude_col] = pd.to_numeric(facility_data[longitude_col], errors='coerce')
        facility_data[latitude_col] = pd.to_numeric(facility_data[latitude_col], errors='coerce')

        facility_data = facility_data.dropna(subset=[longitude_col, latitude_col])
        facility_data = facility_data[
            (facility_data[longitude_col].between(-180, 180)) &
            (facility_data[latitude_col].between(-90, 90))
        ]

        if facility_data.empty:
            st.error("❗ No valid coordinates found. Please check the data.")
            st.stop()

        # ────────── Convert to GeoDataFrame ──────────
        geometry = [Point(xy) for xy in zip(facility_data[longitude_col], facility_data[latitude_col])]
        facility_gdf = gpd.GeoDataFrame(facility_data, geometry=geometry, crs="EPSG:4326")

        # Align CRS
        shapefile = shapefile.to_crs(epsg=4326) if shapefile.crs else shapefile.set_crs(epsg=4326)

        # ────────── Plotting ──────────
        fig, ax = plt.subplots(figsize=(15, 10))
        shapefile.plot(ax=ax, color=background_color, edgecolor='black', linewidth=0.5)

        # Adjust aspect ratio based on midpoint latitude
        bounds = shapefile.total_bounds
        mid_lat = np.mean([bounds[1], bounds[3]])
        try:
            aspect = 1 / np.cos(np.radians(mid_lat))
            aspect = aspect if np.isfinite(aspect) and aspect > 0 else 1.0
        except:
            aspect = 1.0
        ax.set_aspect(aspect)

        facility_gdf.plot(ax=ax, color=point_color, markersize=point_size, alpha=point_alpha)

        # Title and stat box
        plt.title(map_title, fontsize=20, pad=20)
        plt.axis('off')
        stats_text = (
            f"Total Facilities: {len(facility_data)}\n"
            f"Longitude: {facility_data[longitude_col].min():.2f}° to {facility_data[longitude_col].max():.2f}°\n"
            f"Latitude: {facility_data[latitude_col].min():.2f}° to {facility_data[latitude_col].max():.2f}°"
        )
        plt.figtext(0.02, 0.02, stats_text, fontsize=9, bbox=dict(facecolor='white', alpha=0.7))

        # ────────── Display Map ──────────
        st.pyplot(fig)

        # ────────── Download Buttons ──────────
        col6, col7 = st.columns(2)

        with col6:
            output_path_png = "health_facility_map.png"
            plt.savefig(output_path_png, dpi=300, bbox_inches='tight', pad_inches=0.1)
            with open(output_path_png, "rb") as file:
                st.download_button("📥 Download Map (PNG)", file, file_name="health_facility_map.png", mime="image/png")

        with col7:
            csv_data = facility_data.to_csv(index=False)
            st.download_button("📄 Download Cleaned Data (CSV)", csv_data, file_name="processed_facilities.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❗ An error occurred: {str(e)}")
        st.warning("Please double-check your uploaded files.")
else:
    st.info("📤 Upload all required files (.shp, .shx, .dbf, and facility data) to generate the map.")
    st.subheader("🧾 Required Format")
    st.markdown("""
    Your facility data file can be:
    - **Excel file** (.xlsx, .xls)
    - **CSV file** (.csv)
    
    It should contain:
    - **Longitude column** (e.g., `longitude`, `long`, `lon`, `x_coord`)
    - **Latitude column** (e.g., `latitude`, `lat`, `y_coord`)
    
    Coordinates must be in **decimal degrees**.
    """)

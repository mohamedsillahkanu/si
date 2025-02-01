import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from shapely.geometry import Point

st.set_page_config(layout="wide", page_title="Health Facility Map Generator")

st.title("Interactive Health Facility Map Generator")
st.write("Upload your shapefiles and health facility data to generate a customized map.")

# File upload columns
col1, col2 = st.columns(2)

with col1:
    st.header("Upload Shapefiles")
    shp_file = st.file_uploader("Upload .shp file", type=["shp"], key="shp")
    shx_file = st.file_uploader("Upload .shx file", type=["shx"], key="shx")
    dbf_file = st.file_uploader("Upload .dbf file", type=["dbf"], key="dbf")

with col2:
    st.header("Upload Health Facility Data")
    facility_file = st.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"], key="facility")

if all([shp_file, shx_file, dbf_file, facility_file]):
    try:
        # Read files
        with open("temp.shp", "wb") as f:
            f.write(shp_file.read())
        with open("temp.shx", "wb") as f:
            f.write(shx_file.read())
        with open("temp.dbf", "wb") as f:
            f.write(dbf_file.read())
        shapefile = gpd.read_file("temp.shp")
        facility_data = pd.read_excel(facility_file)

        # Column selection
        st.header("Coordinate Column Selection")
        col3, col4, col5 = st.columns(3)
        
        with col3:
            longitude_col = st.selectbox(
                "Select Longitude Column",
                facility_data.columns,
                index=facility_data.columns.get_loc("w_long") if "w_long" in facility_data.columns else 0
            )
        with col4:
            latitude_col = st.selectbox(
                "Select Latitude Column",
                facility_data.columns,
                index=facility_data.columns.get_loc("w_lat") if "w_lat" in facility_data.columns else 0
            )
        with col5:
            name_col = st.selectbox(
                "Select Facility Name Column",
                facility_data.columns,
                index=0
            )

        # Map customization
        st.header("Map Customization")
        col6, col7 = st.columns(2)

        with col6:
            map_title = st.text_input("Map Title", "Health Facility Distribution")
            point_size = st.slider("Point Size", 5, 20, 10)
            point_color = st.color_picker("Point Color", "#FF4B4B")

        with col7:
            show_facility_count = st.checkbox("Show Facility Count", value=True)
            show_chiefdom_name = st.checkbox("Show Chiefdom Names", value=True)

        # Convert facility data to GeoDataFrame
        geometry = [Point(xy) for xy in zip(facility_data[longitude_col], facility_data[latitude_col])]
        facilities_gdf = gpd.GeoDataFrame(
            facility_data, 
            geometry=geometry,
            crs="EPSG:4326"
        )

        # District selection
        districts = sorted(shapefile['FIRST_DNAM'].unique())
        selected_district = st.selectbox("Select District", districts)

        # Filter data for selected district
        district_shapefile = shapefile[shapefile['FIRST_DNAM'] == selected_district]
        
        # Create single map
        fig = go.Figure()

        # Add facilities
        district_facilities = gpd.sjoin(
            facilities_gdf,
            district_shapefile,
            how="inner",
            predicate="within"
        )

        if len(district_facilities) > 0:
            fig.add_trace(
                go.Scattermapbox(
                    lat=district_facilities[latitude_col],
                    lon=district_facilities[longitude_col],
                    mode='markers',
                    marker=dict(
                        size=point_size,
                        color=point_color,
                    ),
                    text=district_facilities[name_col],
                    hovertemplate=(
                        f"Facility: %{{text}}<br>"
                        f"Latitude: %{{lat}}<br>"
                        f"Longitude: %{{lon}}<br>"
                        "<extra></extra>"
                    )
                )
            )

        # Get district bounds
        bounds = district_shapefile.total_bounds

        # Update layout
        fig.update_layout(
            mapbox=dict(
                style="carto-positron",
                center=dict(
                    lat=np.mean([bounds[1], bounds[3]]),
                    lon=np.mean([bounds[0], bounds[2]])
                ),
                zoom=9
            ),
            height=800,
            title=dict(
                text=f"{map_title} - {selected_district} District",
                x=0.5,
                xanchor='center'
            ),
            margin=dict(t=50, r=0, l=0, b=0)
        )

        # Display map
        st.plotly_chart(fig, use_container_width=True)

        # Display statistics
        if show_facility_count:
            st.info(f"Total Facilities in {selected_district}: {len(district_facilities)}")

        # Download options
        col8, col9 = st.columns(2)
        
        with col8:
            html_file = f"health_facility_map_{selected_district}.html"
            fig.write_html(html_file)
            with open(html_file, "rb") as file:
                st.download_button(
                    label="Download Interactive Map (HTML)",
                    data=file,
                    file_name=html_file,
                    mime="text/html"
                )

        with col9:
            if len(district_facilities) > 0:
                csv = district_facilities.to_csv(index=False)
                st.download_button(
                    label="Download Facility Data (CSV)",
                    data=csv,
                    file_name=f"health_facilities_{selected_district}.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.write("Please check your input files and try again.")

else:
    st.info("Please upload all required files to generate the map.")
    st.write("""
    Expected data format:
    - Shapefile with FIRST_DNAM (District) and FIRST_CHIE (Chiefdom) columns
    - Excel file with longitude, latitude, and facility name columns
    """)

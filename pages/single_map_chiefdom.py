import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from shapely.geometry import Point

def create_chiefdom_subplots(district_shapefile, facilities_gdf, district_name, 
                            longitude_col, latitude_col, name_col, point_size, point_color):
    """Create subplots for each chiefdom in a district."""
    
    # Get unique chiefdoms
    chiefdoms = sorted(district_shapefile['FIRST_CHIE'].unique())
    n_chiefdoms = len(chiefdoms)
    
    # Calculate grid dimensions
    n_cols = min(4, n_chiefdoms)
    n_rows = int(np.ceil(n_chiefdoms / n_cols))
    
    # Create subplot figure
    fig = make_subplots(
        rows=n_rows,
        cols=n_cols,
        subplot_titles=chiefdoms,
        specs=[[{"type": "scattermapbox"} for _ in range(n_cols)] for _ in range(n_rows)]
    )

    # Plot each chiefdom
    for idx, chiefdom in enumerate(chiefdoms):
        row = idx // n_cols + 1
        col = idx % n_cols + 1
        
        # Filter data for current chiefdom
        chiefdom_shapefile = district_shapefile[district_shapefile['FIRST_CHIE'] == chiefdom]
        chiefdom_facilities = gpd.sjoin(
            facilities_gdf,
            chiefdom_shapefile,
            how="inner",
            predicate="within"
        )
        
        # Get chiefdom bounds
        bounds = chiefdom_shapefile.total_bounds
        center_lat = np.mean([bounds[1], bounds[3]])
        center_lon = np.mean([bounds[0], bounds[2]])
        
        # Add facilities if any exist
        if len(chiefdom_facilities) > 0:
            fig.add_trace(
                go.Scattermapbox(
                    lat=chiefdom_facilities[latitude_col],
                    lon=chiefdom_facilities[longitude_col],
                    mode='markers',
                    marker=dict(
                        size=point_size,
                        color=point_color,
                    ),
                    text=chiefdom_facilities[name_col],
                    hovertemplate=(
                        f"{chiefdom}<br>"
                        f"Facility: %{{text}}<br>"
                        f"Latitude: %{{lat}}<br>"
                        f"Longitude: %{{lon}}<br>"
                        f"Count: {len(chiefdom_facilities)}"
                        "<extra></extra>"
                    ),
                    name=chiefdom
                ),
                row=row,
                col=col
            )

        # Update layout for each subplot
        fig.update_layout({
            f'mapbox{idx+1}' if idx > 0 else 'mapbox': {
                'style': "carto-positron",
                'center': {'lat': center_lat, 'lon': center_lon},
                'zoom': 9
            }
        })

    # Calculate appropriate height based on number of rows
    height = max(400, n_rows * 400)  # minimum 400px, 400px per row

    # Update overall layout
    fig.update_layout(
        height=height,
        title=f"Health Facilities by Chiefdom - {district_name} District",
        showlegend=False,
        margin=dict(t=50, r=0, l=0, b=20)
    )

    return fig, chiefdoms

def main():
    st.set_page_config(layout="wide")
    st.title("Health Facility Distribution by Chiefdom")

    # File upload
    col1, col2 = st.columns(2)
    with col1:
        shp_file = st.file_uploader("Upload .shp file", type=["shp"])
        shx_file = st.file_uploader("Upload .shx file", type=["shx"])
        dbf_file = st.file_uploader("Upload .dbf file", type=["dbf"])

    with col2:
        facility_file = st.file_uploader("Upload facility Excel file", type=["xlsx"])

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
            col3, col4, col5 = st.columns(3)
            with col3:
                longitude_col = st.selectbox(
                    "Longitude Column",
                    facility_data.columns,
                    index=facility_data.columns.get_loc("w_long") if "w_long" in facility_data.columns else 0
                )
            with col4:
                latitude_col = st.selectbox(
                    "Latitude Column",
                    facility_data.columns,
                    index=facility_data.columns.get_loc("w_lat") if "w_lat" in facility_data.columns else 0
                )
            with col5:
                name_col = st.selectbox(
                    "Facility Name Column",
                    facility_data.columns,
                    index=0
                )

            # Map customization
            col6, col7 = st.columns(2)
            with col6:
                point_size = st.slider("Point Size", 5, 20, 10)
            with col7:
                point_color = st.color_picker("Point Color", "#FF4B4B")

            # Convert to GeoDataFrame
            geometry = [Point(xy) for xy in zip(facility_data[longitude_col], facility_data[latitude_col])]
            facilities_gdf = gpd.GeoDataFrame(
                facility_data, 
                geometry=geometry,
                crs="EPSG:4326"
            )

            # District selection
            districts = sorted(shapefile['FIRST_DNAM'].unique())
            selected_district = st.selectbox("Select District", districts)
            
            # Filter for selected district
            district_shapefile = shapefile[shapefile['FIRST_DNAM'] == selected_district]
            
            # Create and display subplots
            fig, chiefdoms = create_chiefdom_subplots(
                district_shapefile, 
                facilities_gdf,
                selected_district,
                longitude_col,
                latitude_col,
                name_col,
                point_size,
                point_color
            )
            
            st.plotly_chart(fig, use_container_width=True)

            # Download options
            col8, col9 = st.columns(2)
            with col8:
                # Save HTML
                html_file = f"health_facilities_{selected_district}.html"
                fig.write_html(html_file)
                with open(html_file, "rb") as file:
                    st.download_button(
                        "Download Interactive Map (HTML)",
                        file,
                        file_name=html_file,
                        mime="text/html"
                    )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.write("Please check your input files and try again.")

    else:
        st.info("Please upload all required files to generate the maps.")

if __name__ == "__main__":
    main()

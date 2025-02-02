import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from shapely.geometry import Point, Polygon

def clean_coordinate_data(df, longitude_col, latitude_col):
    """
    Clean coordinate data by:
    1. Removing rows with null values
    2. Converting to numeric, coercing errors to NaN
    3. Dropping rows with NaN coordinates
    """
    # Make a copy to avoid modifying original DataFrame
    cleaned_df = df.copy()
    
    # Convert to numeric, forcing errors to NaN
    cleaned_df[longitude_col] = pd.to_numeric(cleaned_df[longitude_col], errors='coerce')
    cleaned_df[latitude_col] = pd.to_numeric(cleaned_df[latitude_col], errors='coerce')
    
    # Drop rows with NaN coordinates
    cleaned_df = cleaned_df.dropna(subset=[longitude_col, latitude_col])
    
    return cleaned_df

def get_polygon_centroid(polygon):
    """
    Get the centroid of a polygon
    """
    if isinstance(polygon, Polygon):
        return polygon.centroid.coords[0]
    elif isinstance(polygon, MultiPolygon):
        # For multipolygon, use the centroid of the largest polygon
        largest_polygon = max(polygon.geoms, key=lambda p: p.area)
        return largest_polygon.centroid.coords[0]
    return None

st.set_page_config(layout="wide", page_title="Health Facility Map Generator")
st.title("Interactive Health Facility Map Generator")
st.write("Upload your shapefiles and health facility data to generate a customized map.")

# File upload UI
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
        # Read input files
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
            # Smart default for longitude column
            default_long_index = 0
            for i, col in enumerate(facility_data.columns):
                if any(kw in col.lower() for kw in ['long', 'lon', 'x', 'longitude']):
                    default_long_index = i
                    break
            
            longitude_col = st.selectbox(
                "Select Longitude Column",
                facility_data.columns,
                index=default_long_index
            )
        
        with col4:
            # Smart default for latitude column
            default_lat_index = 0
            for i, col in enumerate(facility_data.columns):
                if any(kw in col.lower() for kw in ['lat', 'y', 'latitude']):
                    default_lat_index = i
                    break
            
            latitude_col = st.selectbox(
                "Select Latitude Column",
                facility_data.columns,
                index=default_lat_index
            )
        
        with col5:
            name_col = st.selectbox(
                "Select Facility Name Column",
                facility_data.columns,
                index=0
            )

        # Allow user to select additional hover columns
        st.header("Hover Information")
        hover_cols = st.multiselect(
            "Select Additional Columns to Show in Hover",
            [col for col in facility_data.columns if col not in [name_col, longitude_col, latitude_col]],
            default=[]
        )

        # Clean coordinate data
        facility_data = clean_coordinate_data(facility_data, longitude_col, latitude_col)

        # Map customization
        st.header("Map Customization")
        col6, col7 = st.columns(2)

        with col6:
            map_title = st.text_input("Map Title", "Health Facility Distribution")
            title_font_size = st.slider("Title Font Size", 12, 48, 24)
            point_size = st.slider("Point Size", 5, 20, 10)
            chiefdom_label_size = st.slider("Chiefdom Label Size", 8, 20, 12)

        with col7:
            point_color = st.color_picker("Point Color", "#FF4B4B")
            background_color = st.color_picker("Background Color", "#FFFFFF")
            boundary_width = st.slider("Boundary Line Width", 1, 10, 3)
            chiefdom_label_color = st.color_picker("Chiefdom Label Color", "#000000")

        # Create GeoDataFrame from facility data
        geometry = [Point(xy) for xy in zip(facility_data[longitude_col], facility_data[latitude_col])]
        facilities_gdf = gpd.GeoDataFrame(
            facility_data, 
            geometry=geometry,
            crs="EPSG:4326"
        )

        # Get districts and user selection
        districts = sorted(shapefile['FIRST_DNAM'].unique())
        selected_district = st.selectbox("Select District", districts)

        # Filter for selected district
        district_shapefile = shapefile[shapefile['FIRST_DNAM'] == selected_district]
        
        # Get district boundary coordinates
        bounds = district_shapefile.total_bounds
        
        # Spatial join to get facilities within the district
        district_facilities = gpd.sjoin(
            facilities_gdf,
            district_shapefile,
            how="inner",
            predicate="within"
        )
        
        # Create figure
        fig = go.Figure()
        
        # Add chiefdom boundaries and labels
        for _, chiefdom in district_shapefile.iterrows():
            # Convert chiefdom geometry to GeoJSON
            chiefdom_geojson = chiefdom.geometry.__geo_interface__
            
            # Check if it's a polygon or multipolygon
            if chiefdom_geojson['type'] == 'Polygon':
                coords = chiefdom_geojson['coordinates'][0]
            elif chiefdom_geojson['type'] == 'MultiPolygon':
                # Take the first polygon if it's a multipolygon
                coords = chiefdom_geojson['coordinates'][0][0]
            else:
                st.warning(f"Unsupported geometry type: {chiefdom_geojson['type']}")
                continue
            
            # Add chiefdom boundary
            fig.add_trace(
                go.Scattermapbox(
                    mode='lines',
                    lon=[coord[0] for coord in coords],
                    lat=[coord[1] for coord in coords],
                    line=dict(
                        color='black',
                        width=boundary_width
                    ),
                    name=chiefdom['FIRST_CHIE'],
                    hovertemplate=f"Chiefdom: {chiefdom['FIRST_CHIE']}<extra></extra>"
                )
            )
            
            # Add chiefdom label
            # Get centroid coordinates
            centroid = get_polygon_centroid(chiefdom.geometry)
            if centroid:
                fig.add_trace(
                    go.Scattermapbox(
                        mode='text',
                        lon=[centroid[0]],
                        lat=[centroid[1]],
                        text=[chiefdom['FIRST_CHIE']],
                        textfont=dict(
                            color=chiefdom_label_color,
                            size=chiefdom_label_size
                        ),
                        hoverinfo='none'
                    )
                )
        
        # Prepare hover text
        def create_hover_text(row):
            hover_info = [f"Facility: {row[name_col]}"]
            hover_info.append(f"Latitude: {row[latitude_col]:.4f}")
            hover_info.append(f"Longitude: {row[longitude_col]:.4f}")
            
            # Add selected additional columns
            for col in hover_cols:
                hover_info.append(f"{col}: {row[col]}")
            
            return "<br>".join(hover_info)
        
        district_facilities['hover_text'] = district_facilities.apply(create_hover_text, axis=1)
        
        # Add facilities
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
                    text=district_facilities['hover_text'],
                    hoverinfo='text'
                )
            )

        # Update layout
        fig.update_layout(
            height=2000,
            width=2000,
            title={
                'text': f"{map_title}<br>{selected_district} District",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': title_font_size}
            },
            mapbox=dict(
                style="carto-positron",
                center=dict(
                    lat=np.mean([bounds[1], bounds[3]]),
                    lon=np.mean([bounds[0], bounds[2]])
                ),
                zoom=9
            ),
            showlegend=True,
            margin=dict(t=100, r=30, l=30, b=30),
            paper_bgcolor=background_color
        )

        # Display map
        st.plotly_chart(fig, use_container_width=True)

        # Save and download options
        html_content = fig.to_html(
            config={
                'displayModeBar': True,
                'scrollZoom': True,
                'displaylogo': False,
                'responsive': True,
                'toImageButtonOptions': {
                    'format': 'png',
                    'height': 2000,
                    'width': 2000,
                    'scale': 1
                }
            },
            include_plotlyjs=True,
            full_html=True,
            include_mathjax=False
        )

        # Download button
        st.download_button(
            label=f"Download {selected_district} District Map (HTML)",
            data=html_content,
            file_name=f"health_facility_map_{selected_district}.html",
            mime='text/html'
        )

        # Display success message with facility count
        st.success(f"Generated map for {selected_district} District with {len(district_facilities)} facilities")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        import traceback
        st.write(traceback.format_exc())
        st.write("Please check your input files and try again.")

else:
    st.info("Please upload all required files to generate the map.")
    
    st.subheader("Expected Data Format")
    st.write("""
    Shapefile should contain:
    - FIRST_DNAM (District Name)
    - FIRST_CHIE (Chiefdom Name)
    
    Excel file should contain:
    - Longitude column
    - Latitude column
    - Facility name column
    
    The coordinates should be in decimal degrees format.
    """)

import streamlit as st
import geopandas as gpd
import folium
from folium import plugins
import tempfile
import os
from streamlit_folium import folium_static
import branca.colormap as cm
import pandas as pd
import osmnx as ox

st.set_page_config(page_title="Geographic Feature Analysis", layout="wide")

def process_shapefile(shp_file, shx_file, dbf_file, prj_file=None):
    """Process uploaded shapefile components"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Save uploaded files to temporary directory
        file_paths = {}
        for file_obj, ext in [(shp_file, 'shp'), (shx_file, 'shx'), 
                             (dbf_file, 'dbf')]:
            if file_obj is not None:
                file_path = os.path.join(tmp_dir, f"temp.{ext}")
                with open(file_path, 'wb') as f:
                    f.write(file_obj.getvalue())
                file_paths[ext] = file_path
        
        if prj_file:
            prj_path = os.path.join(tmp_dir, "temp.prj")
            with open(prj_path, 'wb') as f:
                f.write(prj_file.getvalue())
        
        # Read shapefile
        gdf = gpd.read_file(file_paths['shp'])
        return gdf

def create_map(gdf, water_bodies=None, buildings=None):
    """Create Folium map with layers"""
    # Get center of the shapefile
    center_lat = gdf.geometry.centroid.y.mean()
    center_lon = gdf.geometry.centroid.x.mean()
    
    # Create base map
    m = folium.Map(location=[center_lat, center_lon], 
                   zoom_start=12,
                   tiles='CartoDB positron')
    
    # Add main shapefile layer
    folium.GeoJson(
        gdf,
        name='Area Boundary',
        style_function=lambda x: {
            'fillColor': 'gray',
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.1
        }
    ).add_to(m)
    
    # Add water bodies if available
    if water_bodies is not None:
        water_style = lambda x: {
            'fillColor': 'blue',
            'color': 'blue',
            'weight': 1,
            'fillOpacity': 0.5
        }
        folium.GeoJson(
            water_bodies,
            name='Water Bodies',
            style_function=water_style
        ).add_to(m)
    
    # Add buildings if available
    if buildings is not None:
        building_style = lambda x: {
            'fillColor': 'red',
            'color': 'red',
            'weight': 1,
            'fillOpacity': 0.5
        }
        folium.GeoJson(
            buildings,
            name='Buildings',
            style_function=building_style
        ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m

def fetch_features(gdf):
    """Fetch water bodies and buildings from OSM"""
    try:
        # Get the bounds of the area
        bounds = gdf.total_bounds
        north, south = bounds[3], bounds[1]
        east, west = bounds[2], bounds[0]
        
        # Fetch water bodies
        water_tags = {'natural': ['water'], 
                     'water': True,
                     'waterway': ['river', 'stream', 'canal']}
        water_bodies = ox.features_from_bbox(north, south, east, west, 
                                           tags=water_tags)
        
        # Fetch buildings
        building_tags = {'building': True}
        buildings = ox.features_from_bbox(north, south, east, west, 
                                        tags=building_tags)
        
        return water_bodies, buildings
    except Exception as e:
        st.error(f"Error fetching features: {str(e)}")
        return None, None

def main():
    st.title("Geographic Feature Analysis")
    st.write("Upload a shapefile to visualize area features on the map")
    
    # File upload section
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        shp_file = st.file_uploader("Upload .shp file", type=['shp'])
    with col2:
        shx_file = st.file_uploader("Upload .shx file", type=['shx'])
    with col3:
        dbf_file = st.file_uploader("Upload .dbf file", type=['dbf'])
    with col4:
        prj_file = st.file_uploader("Upload .prj file (optional)", type=['prj'])
    
    if all([shp_file, shx_file, dbf_file]):
        try:
            # Process shapefile
            gdf = process_shapefile(shp_file, shx_file, dbf_file, prj_file)
            
            # Ensure CRS is in WGS84
            if gdf.crs is None:
                gdf = gdf.set_crs(epsg=4326)
            else:
                gdf = gdf.to_crs(epsg=4326)
            
            # Fetch additional features
            with st.spinner('Fetching water bodies and buildings...'):
                water_bodies, buildings = fetch_features(gdf)
            
            # Create and display map
            st.write("### Map Visualization")
            m = create_map(gdf, water_bodies, buildings)
            folium_static(m)
            
            # Display statistics
            if water_bodies is not None and buildings is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Number of water bodies: {len(water_bodies)}")
                with col2:
                    st.write(f"Number of buildings: {len(buildings)}")
            
        except Exception as e:
            st.error(f"Error processing files: {str(e)}")
    else:
        st.info("Please upload the required files (.shp, .shx, .dbf)")

if __name__ == "__main__":
    main()

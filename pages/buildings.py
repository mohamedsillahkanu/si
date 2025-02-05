import streamlit as st
import geopandas as gpd
import folium
import tempfile
import os
from streamlit_folium import folium_static
import pandas as pd

def process_shapefile(shp_file, shx_file, dbf_file):
    """Process uploaded shapefile and group by FIRST_DNAM"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Save uploaded files
        file_paths = {}
        for file_obj, ext in [(shp_file, 'shp'), (shx_file, 'shx'), (dbf_file, 'dbf')]:
            if file_obj is not None:
                file_path = os.path.join(tmp_dir, f"temp.{ext}")
                with open(file_path, 'wb') as f:
                    f.write(file_obj.getvalue())
                file_paths[ext] = file_path
        
        # Read shapefile
        gdf = gpd.read_file(file_paths['shp'])
        
        # Create a DataFrame for FIRST_DNAM and FIRST_CHIE
        if 'FIRST_DNAM' in gdf.columns and 'FIRST_CHIE' in gdf.columns:
            chiefs_df = gdf[['FIRST_DNAM', 'FIRST_CHIE']].drop_duplicates()
            chiefs_by_district = chiefs_df.groupby('FIRST_DNAM')['FIRST_CHIE'].agg(list).reset_index()
            return gdf, chiefs_by_district
        return gdf, None

def create_map(gdf):
    """Create Folium map with hoverable features"""
    # Get center of the shapefile
    center_lat = gdf.geometry.centroid.y.mean()
    center_lon = gdf.geometry.centroid.x.mean()
    
    # Create base map
    m = folium.Map(location=[center_lat, center_lon], 
                   zoom_start=12)
    
    # Add GeoJSON layer with tooltips
    tooltip_fields = [col for col in gdf.columns if isinstance(gdf[col].iloc[0], (str, int, float))]
    
    folium.GeoJson(
        gdf,
        name='Areas',
        style_function=lambda x: {
            'fillColor': '#ff7800',
            'color': '#000000',
            'weight': 2,
            'fillOpacity': 0.5
        },
        highlight_function=lambda x: {
            'weight': 3,
            'fillOpacity': 0.7
        },
        tooltip=folium.GeoJsonTooltip(
            fields=tooltip_fields,
            aliases=tooltip_fields,
            style="""
                background-color: white;
                color: #333333;
                font-family: arial;
                font-size: 12px;
                padding: 10px;
            """
        )
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m

def main():
    st.title("Geographic Feature Analysis")
    
    # File upload section
    col1, col2, col3 = st.columns(3)
    with col1:
        shp_file = st.file_uploader("Upload .shp file", type=['shp'])
    with col2:
        shx_file = st.file_uploader("Upload .shx file", type=['shx'])
    with col3:
        dbf_file = st.file_uploader("Upload .dbf file", type=['dbf'])
    
    if all([shp_file, shx_file, dbf_file]):
        try:
            # Process shapefile
            gdf, chiefs_by_district = process_shapefile(shp_file, shx_file, dbf_file)
            
            # Display chiefs by district if available
            if chiefs_by_district is not None:
                st.subheader("Chiefs by District")
                for _, row in chiefs_by_district.iterrows():
                    with st.expander(f"🏛️ {row['FIRST_DNAM']}"):
                        for chief in row['FIRST_CHIE']:
                            st.write(f"👤 {chief}")
            
            # Create and display map
            st.subheader("Map Visualization")
            m = create_map(gdf)
            folium_static(m)
            
            # Display data summary
            st.subheader("Data Summary")
            if 'FIRST_DNAM' in gdf.columns:
                num_districts = len(gdf['FIRST_DNAM'].unique())
                st.write(f"Number of Districts: {num_districts}")
            if 'FIRST_CHIE' in gdf.columns:
                num_chiefs = len(gdf['FIRST_CHIE'].unique())
                st.write(f"Number of Chiefs: {num_chiefs}")
            
        except Exception as e:
            st.error(f"Error processing files: {str(e)}")
    else:
        st.info("Please upload all required files (.shp, .shx, .dbf)")

if __name__ == "__main__":
    main()

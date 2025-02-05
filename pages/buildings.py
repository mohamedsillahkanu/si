import streamlit as st
import geopandas as gpd
import folium
from folium import plugins
import tempfile
import os
from streamlit_folium import folium_static
import pandas as pd
import random

def generate_color():
    """Generate a random color for district visualization"""
    return f'#{random.randint(0, 0xFFFFFF):06x}'

def process_shapefile(shp_file, shx_file, dbf_file):
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_paths = {}
        for file_obj, ext in [(shp_file, 'shp'), (shx_file, 'shx'), (dbf_file, 'dbf')]:
            if file_obj is not None:
                file_path = os.path.join(tmp_dir, f"temp.{ext}")
                with open(file_path, 'wb') as f:
                    f.write(file_obj.getvalue())
                file_paths[ext] = file_path
        
        return gpd.read_file(file_paths['shp'])

def create_map(gdf):
    # Get center of the shapefile
    center_lat = gdf.geometry.centroid.y.mean()
    center_lon = gdf.geometry.centroid.x.mean()
    
    # Create base map
    m = folium.Map(location=[center_lat, center_lon], 
                   zoom_start=12,
                   tiles='CartoDB positron')
    
    # Create color dictionary for districts
    if 'FIRST_DNAM' in gdf.columns:
        districts = gdf['FIRST_DNAM'].unique()
        district_colors = {district: generate_color() for district in districts}
        
        # Group by district
        for district in districts:
            district_data = gdf[gdf['FIRST_DNAM'] == district]
            
            # Add district layer
            folium.GeoJson(
                district_data,
                name=f"District: {district}",
                style_function=lambda x, district=district: {
                    'fillColor': district_colors[district],
                    'color': 'black',
                    'weight': 2,
                    'fillOpacity': 0.3
                },
                tooltip=folium.GeoJsonTooltip(
                    fields=['FIRST_DNAM', 'FIRST_CHIE', 'STRUCTURE'],
                    aliases=['District', 'Chief', 'Structure'],
                    style="""
                        background-color: white;
                        color: #333333;
                        font-family: arial;
                        font-size: 12px;
                        padding: 10px;
                    """
                ),
                popup=folium.GeoJsonPopup(
                    fields=['STRUCTURE', 'FIRST_CHIE', 'FIRST_DNAM'],
                    aliases=['Structure', 'Chief', 'District'],
                    style="""
                        background-color: white;
                        color: #333333;
                        font-family: arial;
                        font-size: 12px;
                        padding: 10px;
                    """
                )
            ).add_to(m)

            # Add markers for structures if available
            if 'STRUCTURE' in gdf.columns:
                for idx, row in district_data.iterrows():
                    if pd.notna(row['STRUCTURE']):
                        folium.CircleMarker(
                            location=[row.geometry.centroid.y, row.geometry.centroid.x],
                            radius=6,
                            popup=f"""<b>Structure:</b> {row['STRUCTURE']}<br>
                                     <b>District:</b> {row['FIRST_DNAM']}<br>
                                     <b>Chief:</b> {row['FIRST_CHIE']}""",
                            color='red',
                            fill=True,
                            fill_color='red'
                        ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add search function
    if 'STRUCTURE' in gdf.columns:
        search_data = []
        for idx, row in gdf.iterrows():
            if pd.notna(row['STRUCTURE']):
                search_data.append({
                    'loc': [row.geometry.centroid.y, row.geometry.centroid.x],
                    'title': f"Structure: {row['STRUCTURE']}"
                })
        
        search = plugins.Search(
            layer=None,
            geom_type='Point',
            placeholder='Search for structures',
            collapsed=False,
            search_label='title',
            search_zoom=18,
            position='topright'
        ).add_to(m)
        
        for item in search_data:
            folium.CircleMarker(
                location=item['loc'],
                radius=1,
                popup=item['title'],
                search_label=item['title'],
            ).add_to(search)

    return m

def main():
    st.title("Structure Analysis by District")
    st.write("Upload shapefile to view structures within each district")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        shp_file = st.file_uploader("Upload .shp file", type=['shp'])
    with col2:
        shx_file = st.file_uploader("Upload .shx file", type=['shx'])
    with col3:
        dbf_file = st.file_uploader("Upload .dbf file", type=['dbf'])
    
    if all([shp_file, shx_file, dbf_file]):
        try:
            gdf = process_shapefile(shp_file, shx_file, dbf_file)
            
            if 'STRUCTURE' in gdf.columns:
                # Display statistics first
                st.subheader("Summary Statistics")
                total_structures = gdf['STRUCTURE'].count()
                total_districts = len(gdf['FIRST_DNAM'].unique())
                st.write(f"Total Structures: {total_structures}")
                st.write(f"Total Districts: {total_districts}")
                
                # Create expandable sections for each district
                st.subheader("Structures by District")
                for district in sorted(gdf['FIRST_DNAM'].unique()):
                    district_data = gdf[gdf['FIRST_DNAM'] == district]
                    with st.expander(f"District: {district} ({len(district_data)} structures)"):
                        for _, row in district_data.iterrows():
                            if pd.notna(row['STRUCTURE']):
                                st.write(f"🏛️ {row['STRUCTURE']}")
                
                # Display interactive map
                st.subheader("Interactive Map")
                m = create_map(gdf)
                folium_static(m, width=1000, height=600)
                
            else:
                st.error("No structure information found in the shapefile")
                
        except Exception as e:
            st.error(f"Error processing files: {str(e)}")
            st.write("Please ensure your shapefile contains structure information")
    else:
        st.info("Please upload all required files (.shp, .shx, .dbf)")

if __name__ == "__main__":
    main()

import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from shapely.geometry import Point
import os
import zipfile
import io

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

        # [Previous code remains the same until the file generation part]

        # Store HTML files in memory
        html_files = []
        
        # Generate individual plots
        for chiefdom in chiefdoms:
            chiefdom_shapefile = district_shapefile[district_shapefile['FIRST_CHIE'] == chiefdom]
            bounds = chiefdom_shapefile.total_bounds
            
            chiefdom_facilities = gpd.sjoin(
                facilities_gdf,
                chiefdom_shapefile,
                how="inner",
                predicate="within"
            )
            
            # Create figure
            fig = go.Figure()
            
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
                        hovertemplate="Facility: %{text}<br>Latitude: %{lat:.4f}<br>Longitude: %{lon:.4f}<extra></extra>"
                    )
                )

            # Update layout
            fig.update_layout(
                height=2000,
                width=2000,
                title={
                    'text': f"{map_title}<br>{chiefdom} Chiefdom, {selected_district} District",
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
                    zoom=10
                ),
                showlegend=False,
                margin=dict(t=title_spacing + title_font_size + 10, r=30, l=30, b=30),
                paper_bgcolor=background_color
            )

            # Generate HTML content
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
            
            # Store HTML content and filename
            html_files.append({
                'filename': f"health_facility_map_{selected_district}_{chiefdom}.html",
                'content': html_content
            })

        # Create download interface
        st.header("Download Maps")
        
        # Individual file downloads
        st.subheader("Download Individual Maps")
        for html_file in html_files:
            st.download_button(
                label=f"Download {html_file['filename']}",
                data=html_file['content'],
                file_name=html_file['filename'],
                mime='text/html',
                key=html_file['filename']
            )

        # Create ZIP file containing all maps
        st.subheader("Download All Maps")
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for html_file in html_files:
                zip_file.writestr(html_file['filename'], html_file['content'])
        
        st.download_button(
            label="Download All Maps (ZIP)",
            data=zip_buffer.getvalue(),
            file_name=f"health_facility_maps_{selected_district}.zip",
            mime="application/zip"
        )

        # Display success message
        st.success(f"Generated {len(chiefdoms)} maps for {selected_district} District")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
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

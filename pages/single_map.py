import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from shapely.geometry import Point
import os

st.set_page_config(layout="wide", page_title="Health Facility Map Generator")

# [Previous code remains same until after the facility_data processing]

        # Create output directory for HTML files
        output_dir = "chiefdom_maps"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Get unique districts from shapefile
        districts = sorted(shapefile['FIRST_DNAM'].unique())
        selected_district = st.selectbox("Select District", districts)

        # Filter shapefile for selected district
        district_shapefile = shapefile[shapefile['FIRST_DNAM'] == selected_district]
        
        # Get unique chiefdoms for the selected district
        chiefdoms = sorted(district_shapefile['FIRST_CHIE'].unique())
        
        # Create individual plots for each chiefdom
        for chiefdom in chiefdoms:
            # Filter shapefile for current chiefdom
            chiefdom_shapefile = district_shapefile[district_shapefile['FIRST_CHIE'] == chiefdom]
            
            # Get chiefdom boundary coordinates
            bounds = chiefdom_shapefile.total_bounds
            
            # Spatial join to get facilities within the chiefdom
            chiefdom_facilities = gpd.sjoin(
                facilities_gdf,
                chiefdom_shapefile,
                how="inner",
                predicate="within"
            )
            
            # Create individual figure for the chiefdom
            fig = go.Figure()
            
            if len(chiefdom_facilities) > 0:
                # Add scatter mapbox trace for facilities
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
                            f"Facility: %{{text}}<br>"
                            f"Latitude: %{{lat}}<br>"
                            f"Longitude: %{{lon}}<br>"
                            "<extra></extra>"
                        ),
                        name=chiefdom
                    )
                )

            # Update layout for the individual plot
            fig.update_layout(
                height=2000,  # 20x20 size
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

            # Save individual HTML file
            html_file = os.path.join(output_dir, f"health_facility_map_{selected_district}_{chiefdom}.html")
            
            config = {
                'displayModeBar': True,
                'scrollZoom': True,
                'displaylogo': False,
                'responsive': True,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': f'health_facility_map_{selected_district}_{chiefdom}',
                    'height': 2000,
                    'width': 2000,
                    'scale': 1
                }
            }
            
            fig.write_html(
                html_file,
                config=config,
                include_plotlyjs=True,
                full_html=True,
                include_mathjax=False
            )

        # Create a zip file containing all HTML files
        import zipfile
        zip_filename = f"health_facility_maps_{selected_district}.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for html_file in os.listdir(output_dir):
                if html_file.endswith('.html'):
                    zipf.write(os.path.join(output_dir, html_file), html_file)

        # Add download button for the zip file
        with open(zip_filename, "rb") as f:
            st.download_button(
                label="Download All Chiefdom Maps (ZIP)",
                data=f,
                file_name=zip_filename,
                mime="application/zip"
            )

        # Display success message
        st.success(f"Generated individual HTML maps for {len(chiefdoms)} chiefdoms in {selected_district} District")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.write("Please check your input files and try again.")

else:
    st.info("Please upload all required files to generate the map.")
    
    # Show example data format
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

import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap, to_hex
import io

st.image("icf_sl (1).jpg", caption="MAP GENERATOR", use_column_width=True)

# Load the shapefile
gdf = gpd.read_file("https://raw.githubusercontent.com/mohamedsillahkanu/si/2b7f982174b609f9647933147dec2a59a33e736a/Chiefdom%202021.shp")

# File upload (Excel or CSV)
uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])
if uploaded_file is not None:
    # Read the uploaded file (Excel or CSV)
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    # Exclude certain columns from being selectable for the map
    excluded_columns = ['FIRST_DNAM', 'FIRST_CHIE', 'adm3']
    available_columns = [col for col in df.columns if col not in excluded_columns]

    # UI elements for selecting map settings
    map_column = st.selectbox("Select Map Column:", available_columns)
    map_title = st.text_input("Map Title:")
    image_name = st.text_input("Image Name:", value="Generated_Map")
    line_color = st.selectbox("Select Line Color:", options=["White", "Black", "Red"], index=1)
    line_width = st.slider("Select Line Width:", min_value=0.5, max_value=5.0, value=2.5)

    # Generate the map upon button click
    if st.button("Generate Map"):
        try:
            # Merge the shapefile and Excel data using FIRST_DNAM
            merged_gdf = gdf.merge(df, on='FIRST_DNAM', how='left')

            if map_column not in merged_gdf.columns:
                st.error(f"The column '{map_column}' does not exist in the merged dataset.")
            else:
                fig, ax = plt.subplots(figsize=(10, 10))

                # Plot the boundaries only
                merged_gdf.boundary.plot(ax=ax, edgecolor=line_color.lower(), linewidth=line_width)

                # Add title
                ax.set_title(map_title, fontsize=15, fontweight='bold')
                ax.set_axis_off()

                # Save the map to a BytesIO object for downloading
                img_bytes = io.BytesIO()
                plt.savefig(img_bytes, format='png', dpi=300, bbox_inches='tight')
                img_bytes.seek(0)
                st.image(img_bytes, caption=map_title)

                # Allow user to download the map
                st.download_button("Download Map", img_bytes, file_name=f"{image_name}.png", mime="image/png")

        except Exception as e:
            st.error(f"An error occurred while generating the map: {e}")

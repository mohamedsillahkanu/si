import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
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

    # Select the map column
    available_columns = [col for col in df.columns if col not in ['FIRST_DNAM', 'FIRST_CHIE', 'adm3']]
    map_column = st.selectbox("Select Map Column:", available_columns)

    # Generate the map upon button click
    if st.button("Generate Map"):
        try:
            # Merge the shapefile and Excel data
            merged_gdf = gdf.merge(df, on=['FIRST_DNAM','FIRST_CHIE'], how='left')

            if map_column not in merged_gdf.columns:
                st.error(f"The column '{map_column}' does not exist in the merged dataset.")
            else:
                fig, ax = plt.subplots(1, 1, figsize=(10, 10))

                # Plot the map
                merged_gdf.plot(column=map_column, ax=ax, edgecolor='black', linewidth=1, legend=True)

                # Add boundaries for 'FIRST_DNAM' only
                dissolved_gdf1 = merged_gdf.dissolve(by='FIRST_DNAM')
                dissolved_gdf1.boundary.plot(ax=ax, edgecolor='black', linewidth=2)

                ax.set_title("Generated Map", fontsize=15, fontweight='bold')
                ax.set_axis_off()

                # Save the map to a BytesIO object for downloading
                img_bytes = io.BytesIO()
                plt.savefig(img_bytes, format='png', dpi=300, bbox_inches='tight')
                img_bytes.seek(0)

                # Display the map in Streamlit
                st.image(img_bytes, caption="Generated Map", use_column_width=True)

                # Add download button
                st.download_button(
                    label="Download Map Image",
                    data=img_bytes,
                    file_name="generated_map.png",
                    mime="image/png"
                )

        except Exception as e:
            st.error(f"An error occurred while generating the map: {str(e)}")

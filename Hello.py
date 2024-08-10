import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("Map Generator")

# File uploads
shp_file = st.file_uploader("Upload .shp File", type=["shp"])
shx_file = st.file_uploader("Upload .shx File", type=["shx"])
dbf_file = st.file_uploader("Upload .dbf File", type=["dbf"])
xlsx_file = st.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"])

if shp_file and shx_file and dbf_file and xlsx_file:
    with open("/tmp/uploaded.shp", "wb") as f:
        f.write(shp_file.getbuffer())
    with open("/tmp/uploaded.shx", "wb") as f:
        f.write(shx_file.getbuffer())
    with open("/tmp/uploaded.dbf", "wb") as f:
        f.write(dbf_file.getbuffer())
    with open("/tmp/uploaded.xlsx", "wb") as f:
        f.write(xlsx_file.getbuffer())

    gdf = gpd.read_file("/tmp/uploaded.shp")
    df = pd.read_excel("/tmp/uploaded.xlsx")

    shapefile_column_name = st.text_input("Shapefile Column:")
    excel_column_name = st.text_input("Excel Column:")
    map_column_name = st.text_input("Map Column:")
    map_title = st.text_input("Map Title:")
    image_name = st.text_input("Image Name:", value="map_image")
    font_size = st.slider("Font Size:", min_value=8, max_value=24, value=15)
    line_width = st.slider("Line Width:", min_value=0.5, max_value=5.0, value=2.5)
    color_palette = st.selectbox("Color Palette:", options=list(plt.colormaps()), index=list(plt.colormaps()).index('viridis'))

    if st.button("Generate Map"):
        try:
            merged_gdf = gdf.merge(df, left_on=shapefile_column_name, right_on=excel_column_name, how='left')
            
            if map_column_name not in merged_gdf.columns:
                st.error(f"The column '{map_column_name}' does not exist in the merged dataset.")
            else:
                fig, ax = plt.subplots(1, 1, figsize=(10, 10))
                merged_gdf.plot(column=map_column_name, ax=ax, linewidth=line_width, edgecolor='black', cmap=color_palette, 
                                legend=True, missing_kwds={'color': 'lightgray', 'edgecolor': 'black', 'hatch': '//', 'label': 'No Data'})
                ax.set_title(map_title, fontsize=font_size)
                ax.set_axis_off()
                
                st.pyplot(fig)
                
                if st.button("Download Image"):
                    image_path = f"/tmp/{image_name}.png"
                    fig.savefig(image_path, bbox_inches='tight')
                    with open(image_path, "rb") as img:
                        st.download_button(label="Download Image", data=img, file_name=f"{image_name}.png", mime="image/png")
        except KeyError as e:
            st.error(f"Error: The specified column '{e.args[0]}' does not exist in the dataset.")
else:
    st.warning("Please upload all required files (.shp, .shx, .dbf, .xlsx).")

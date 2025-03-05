import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap, to_hex
import io

# Displaying the images
st.image("icf_sl (1).jpg", caption="MAP GENERATOR", use_column_width=True)

# Load the shapefile
gdf = gpd.read_file("https://raw.githubusercontent.com/mohamedsillahkanu/si/2b7f982174b609f9647933147dec2a59a33e736a/Chiefdom%202021.shp")

# File upload (Excel or CSV)
uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])
if uploaded_file is not None:
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    excluded_columns = ['FIRST_DNAM', 'FIRST_CHIE', 'adm3']
    available_columns = [col for col in df.columns if col not in excluded_columns]

    map_column = st.selectbox("Select Map Column:", available_columns)
    map_title = st.text_input("Map Title:")
    legend_title = st.text_input("Legend Title:")
    image_name = st.text_input("Image Name:", value="Generated_Map")
    font_size = st.slider("Font Size (for Map Title):", min_value=8, max_value=24, value=15)

    show_image = st.checkbox('Check this box to display the Color Palette')
    if show_image:
        st.image('Color palette.png', caption='Color Palette')

    color_palette_name = st.selectbox("Color Palette:", options=list(plt.colormaps()), index=list(plt.colormaps()).index('Set3'))

    # Line color and width options
    line_colors = ["White", "Black", "Red", "Gray10", "Gray20", "Gray30", "Gray40", "Gray50", "Gray60", "Gray70", "Gray80", "Gray90"]
    line_color = st.selectbox("Select Default Line Color:", options=line_colors, index=0)
    line_width = st.slider("Select Default Line Width:", min_value=0.5, max_value=5.0, value=2.5)

    # Manual color selection for columns
    all_colors = ["White", "Black", "Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Brown", "Pink", "Cyan", "Magenta", "Lime", "Teal", "Navy", "Maroon", "Olive", "Gray"]
    manual_color_selection = st.checkbox("Manually Select Colors for a Column")
    if manual_color_selection:
        selected_column = st.selectbox("Select Column to Apply Manual Colors:", available_columns)
        unique_values = df[selected_column].dropna().unique().tolist()
        custom_colors = {val: st.selectbox(f"Select Color for {val}:", all_colors) for val in unique_values}

    missing_value_color = st.selectbox("Select Color for Missing Values:", options=all_colors, index=0)
    missing_value_label = st.text_input("Label for Missing Values:", value="No Data")

    # Generate map
    if st.button("Generate Map"):
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf.boundary.plot(ax=ax, linewidth=line_width, color=line_color.lower())
        
        # Apply colors based on manual selection
        if manual_color_selection:
            df["color"] = df[selected_column].map(custom_colors)
        else:
            cmap = plt.get_cmap(color_palette_name)
            num_colors = min(9, cmap.N)
            colors = [to_hex(cmap(i / (num_colors - 1))) for i in range(num_colors)]
            color_mapping = {val: colors[i % num_colors] for i, val in enumerate(df[map_column].dropna().unique())}
            df["color"] = df[map_column].map(color_mapping)
        
        for _, row in gdf.iterrows():
            color = df[df["adm3"] == row["adm3"]]["color"].values[0] if row["adm3"] in df["adm3"].values else missing_value_color.lower()
            row_geometry = row.geometry
            if row_geometry is not None:
                gdf[gdf["adm3"] == row["adm3"]].plot(ax=ax, color=color, edgecolor=line_color.lower(), linewidth=line_width)
        
        ax.set_title(map_title, fontsize=font_size)
        ax.axis("off")
        
        # Add legend
        legend_patches = [Patch(facecolor=color_mapping[val], label=val) for val in color_mapping]
        ax.legend(handles=legend_patches, title=legend_title, loc='lower left', fontsize=font_size - 3)
        
        st.pyplot(fig)

        # Save Image
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        buf.seek(0)
        st.download_button(label="Download Map", data=buf, file_name=f"{image_name}.png", mime="image/png")

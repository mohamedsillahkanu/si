import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap, to_hex
import requests
from io import BytesIO

st.image("icf_sl (1).jpg", caption="MAP GENERATOR", use_column_width=True)

# Shapefile URLs
shp_file_url = "https://raw.githubusercontent.com/mohamedsillahkanu/si/2b7f982174b609f9647933147dec2a59a33e736a/Chiefdom%202021.shp"
shx_file_url = "https://raw.githubusercontent.com/mohamedsillahkanu/si/2b7f982174b609f9647933147dec2a59a33e736a/Chiefdom%202021.shx"
dbf_file_url = "https://raw.githubusercontent.com/mohamedsillahkanu/si/2b7f982174b609f9647933147dec2a59a33e736a/Chiefdom%202021.dbf"

# Load shapefiles directly from URL
@st.cache_data
def load_shapefile(shp_url, shx_url, dbf_url):
    shp = BytesIO(requests.get(shp_url).content)
    shx = BytesIO(requests.get(shx_url).content)
    dbf = BytesIO(requests.get(dbf_url).content)
    return gpd.read_file(shp, shx=shx, dbf=dbf)

# File upload for Excel
xlsx_file = st.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"])

if xlsx_file:
    # Load shapefile from URLs
    gdf = load_shapefile(shp_file_url, shx_file_url, dbf_file_url)
    df = pd.read_excel(xlsx_file)

    shapefile_columns = st.multiselect("Select Shapefile Column(s):", gdf.columns)
    excel_columns = st.multiselect("Select Excel Column(s):", df.columns)
    map_column = st.selectbox("Select Map Column:", df.columns)
    map_title = st.text_input("Map Title:")
    legend_title = st.text_input("Legend Title:")
    image_name = st.text_input("Image Name:", value="map_image")
    font_size = st.slider("Font Size (for Map Title):", min_value=8, max_value=24, value=15)
    color_palette_name = st.selectbox("Color Palette:", options=list(plt.colormaps()), index=list(plt.colormaps()).index('Set3'))

    # Default line color and width settings
    line_color = st.selectbox("Select Default Line Color:", options=["White", "Black", "Red"], index=1)
    line_width = st.slider("Select Default Line Width:", min_value=0.5, max_value=5.0, value=2.5)

    missing_value_color = st.selectbox("Select Color for Missing Values:", options=["White", "Gray", "Red"], index=1)
    missing_value_label = st.text_input("Label for Missing Values:", value="No Data")

    # Categorical or Numeric variable selection
    variable_type = st.radio("Select the variable type:", options=["Categorical", "Numeric"])
    category_counts = {}

    if variable_type == "Categorical":
        unique_values = sorted(df[map_column].dropna().unique().tolist())
        selected_categories = st.multiselect(f"Select Categories for the Legend of {map_column}:", unique_values, default=unique_values)
        category_counts = df[map_column].value_counts().to_dict()
        
    elif variable_type == "Numeric":
        bin_labels_input = st.text_input("Enter labels for bins (comma-separated, e.g., '10-20.5, 20.6-30.1, >30.2'):")
        bin_labels = [label.strip() for label in bin_labels_input.split(',')]
        bins = []
        
        try:
            for label in bin_labels:
                if '>' in label:
                    lower = float(label.replace('>', '').strip())
                    bins.append(lower)
                elif '-' in label:
                    lower, upper = map(float, label.split('-'))
                    bins.append(lower)
                    bins.append(upper)
            bins = sorted(list(set(bins)))
            bins.append(df[map_column].max() + 1)
            df[map_column + "_bins"] = pd.cut(df[map_column], bins=bins, labels=bin_labels, include_lowest=True)
            map_column = map_column + "_bins"
            selected_categories = bin_labels
            category_counts = df[map_column].value_counts().to_dict()
        except ValueError:
            st.error(f"Error: The column '{map_column}' contains non-numeric data or cannot be converted to numeric values.")
    
    cmap = plt.get_cmap(color_palette_name)
    num_colors = min(9, cmap.N)
    colors = [to_hex(cmap(i / (num_colors - 1))) for i in range(num_colors)]
    color_mapping = {category: colors[i % num_colors] for i, category in enumerate(selected_categories)}

    if st.checkbox("Select Colors for Columns"):
        for i, category in enumerate(selected_categories):
            color_mapping[category] = st.selectbox(f"Select Color for '{category}' in {map_column}:", options=colors, index=i)

    # Check for matching columns for merging
    if len(shapefile_columns) == 1 and len(excel_columns) == 1:
        if st.button("Generate Map"):
            try:
                merged_gdf = gdf.merge(df, left_on=shapefile_columns[0], right_on=excel_columns[0], how='left')

                if map_column not in merged_gdf.columns:
                    st.error(f"The column '{map_column}' does not exist in the merged dataset.")
                else:
                    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
                    custom_cmap = ListedColormap([color_mapping[cat] for cat in selected_categories])

                    merged_gdf.plot(column=map_column, ax=ax, linewidth=line_width, edgecolor=line_color.lower(), cmap=custom_cmap, 
                                    legend=False, missing_kwds={'color': missing_value_color.lower(), 'edgecolor': line_color.lower(), 'label': missing_value_label})
                    ax.set_title(map_title, fontsize=font_size, fontweight='bold')
                    ax.set_axis_off()

                    handles = [Patch(color=color_mapping[cat], label=f"{cat} ({category_counts.get(cat, 0)})") for cat in selected_categories]
                    handles.append(Patch(color=missing_value_color.lower(), label=f"{missing_value_label} ({df[map_column].isna().sum()})"))

                    legend = ax.legend(handles=handles, title=legend_title, fontsize=10, loc='lower left', bbox_to_anchor=(-0.5, 0))
                    plt.setp(legend.get_title(), fontsize=10, fontweight='bold')
                    plt.setp(legend.get_texts(), fontsize=10, fontweight='bold')

                    st.pyplot(fig)

                    # Save image and provide download button
                    image_path = f"/tmp/{image_name}_{map_column}.png"
                    fig.savefig(image_path, bbox_inches='tight')
                    with open(image_path, "rb") as img:
                        st.download_button(label="Download Image", data=img, file_name=f"{image_name}_{map_column}.png", mime="image/png")
            except Exception as e:
                st.error(f"Error generating map: {e}")

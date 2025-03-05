import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
import io

# Display the App Header
st.image("icf_sl (1).jpg", caption="MAP GENERATOR", use_column_width=True)

# Load the shapefile
gdf = gpd.read_file("https://raw.githubusercontent.com/mohamedsillahkanu/si/2b7f982174b609f9647933147dec2a59a33e736a/Chiefdom%202021.shp")

# File upload (Excel or CSV)
uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Read the uploaded file
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)

    # Exclude certain columns from being selectable for the map
    excluded_columns = ['FIRST_DNAM', 'FIRST_CHIE', 'adm3']
    available_columns = [col for col in df.columns if col not in excluded_columns]

    # UI elements for selecting map settings
    map_column = st.selectbox("Select Map Column:", available_columns)
    map_title = st.text_input("Map Title:")
    legend_title = st.text_input("Legend Title:")
    image_name = st.text_input("Image Name:", value="Generated_Map")
    font_size = st.slider("Font Size (for Map Title):", min_value=8, max_value=24, value=15)

    # Color selection method
    color_selection = st.radio("Select Color Mode:", ["Predefined Palette", "Manual Colors"])

    # Display the color palette image
    show_image = st.checkbox('Check this box to display the Color Palette')
    if show_image:
        st.image('Color palette.png', caption='Color Palette')

    # Default Line Color & Width Selection
    line_colors = ["White", "Light Gray", "Gray", "Dark Gray", "Black", "Red", "Blue", "Green", "Yellow", "Orange", "Purple"]
    line_color = st.selectbox("Select Default Line Color:", options=line_colors, index=0)
    line_width = st.slider("Select Default Line Width:", min_value=0.5, max_value=5.0, value=2.5)

    # Missing Value Settings
    missing_value_color = st.selectbox("Select Color for Missing Values:", options=line_colors, index=2)
    missing_value_label = st.text_input("Label for Missing Values:", value="No Data")

    # Handle Color Mapping
    if color_selection == "Manual Colors":
        if "color" not in df.columns:
            df["color"] = None  # Initialize the color column

        unique_adm3_values = df["adm3"].unique()
        color_mapping = {}  # Store selected colors

        for adm3_value in unique_adm3_values:
            selected_color = st.color_picker(f"Select color for {adm3_value}:", "#FFFFFF")
            df.loc[df["adm3"] == adm3_value, "color"] = selected_color
            color_mapping[adm3_value] = selected_color

    else:
        color_palette_name = st.selectbox("Color Palette:", options=list(plt.colormaps()), index=list(plt.colormaps()).index('Set3'))
        cmap = plt.get_cmap(color_palette_name)
        colors = [to_hex(cmap(i / (len(df["adm3"].unique()) - 1))) for i in range(len(df["adm3"].unique()))]
        color_mapping = dict(zip(df["adm3"].unique(), colors))
        df["color"] = df["adm3"].map(color_mapping)

    # Assign colors safely with fallback
    def get_color(row):
        if "color" in df.columns and row["adm3"] in df["adm3"].values:
            filtered_values = df[df["adm3"] == row["adm3"]]["color"].values
            return filtered_values[0] if len(filtered_values) > 0 else missing_value_color.lower()
        return missing_value_color.lower()

    gdf["color"] = gdf.apply(get_color, axis=1)

    # Plot Map
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    gdf.plot(ax=ax, color=gdf["color"], edgecolor=line_color.lower(), linewidth=line_width)

    ax.set_title(map_title, fontsize=font_size)
    ax.axis("off")

    # Add Legend
    legend_patches = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markersize=10, label=category)
                      for category, color in color_mapping.items()]
    ax.legend(handles=legend_patches, title=legend_title, loc="lower left", fontsize=10)

    # Show Plot
    st.pyplot(fig)

    # Download Map as Image
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    buf.seek(0)
    st.download_button(label="Download Map", data=buf, file_name=f"{image_name}.png", mime="image/png")

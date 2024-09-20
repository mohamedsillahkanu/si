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
    legend_title = st.text_input("Legend Title:")
    image_name = st.text_input("Image Name:", value="Generated_Map")
    font_size = st.slider("Font Size (for Map Title):", min_value=8, max_value=24, value=15)

    show_image = st.checkbox('Check this box to display the Color Palette')

    # Display the image when the checkbox is checked
    if show_image:
        st.image('Color palette.png', caption='Color Palette')
    color_palette_name = st.selectbox("Color Palette:", options=list(plt.colormaps()), index=list(plt.colormaps()).index('Set3'))

    # Default line color and width settings for FIRST_DNAM boundaries
    line_color = st.selectbox("Select Default Line Color for FIRST_DNAM Boundaries:", options=["White", "Black", "Red"], index=1)
    line_width = st.slider("Select Default Line Width for FIRST_DNAM Boundaries:", min_value=0.5, max_value=5.0, value=2.5)

    # Missing value settings
    missing_value_color = st.selectbox("Select Color for Missing Values:", options=["White", "Gray", "Red"], index=1)
    missing_value_label = st.text_input("Label for Missing Values:", value="No Data")

    # Initialize category_counts dictionary for managing category counts
    category_counts = {}

    # Categorical or Numeric variable selection
    variable_type = st.radio("Select the variable type:", options=["Categorical", "Numeric"])

    if variable_type == "Categorical":
        unique_values = sorted(df[map_column].dropna().unique().tolist())
        selected_categories = st.multiselect(f"Select Categories for the Legend of {map_column}:", unique_values, default=unique_values)
        category_counts = df[map_column].value_counts().to_dict()

        # Reorder the categories
        df[map_column] = pd.Categorical(df[map_column], categories=selected_categories, ordered=True)

    elif variable_type == "Numeric":
        try:
            # Custom labels for bins
            bin_labels_input = st.text_input("Enter labels for bins (comma-separated):")
            bin_labels = [label.strip() for label in bin_labels_input.split(',')]

            # Create bin ranges from labels
            bins = []
            for label in bin_labels:
                if '>' in label:
                    lower = float(label.replace('>', '').strip())
                    bins.append(lower)
                elif '-' in label:
                    lower, upper = map(float, label.split('-'))
                    bins.append(lower)
                    bins.append(upper)

            # Sort bins and ensure the last bin covers the max value
            bins = sorted(list(set(bins)))
            if bins[-1] < df[map_column].max():
                bins.append(df[map_column].max() + 1)

            # Perform binning
            df[map_column + "_bins"] = pd.cut(df[map_column], bins=bins, labels=bin_labels, include_lowest=True)
            map_column = map_column + "_bins"
            selected_categories = bin_labels
            category_counts = df[map_column].value_counts().to_dict()

        except ValueError:
            st.error(f"Error: The column '{map_column}' contains non-numeric data or cannot be converted to numeric values.")

    # Merge Excel data with GeoDataFrame by FIRST_DNAM
    gdf = gdf.merge(df, how='left', on='FIRST_DNAM')

    # Filter GeoDataFrame to include only the polygons for FIRST_DNAM
    adm2_gdf = gdf.dissolve(by='FIRST_DNAM')

    # Define a colormap
    cmap = plt.get_cmap(color_palette_name, len(selected_categories))

    # Create a plot
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot the GeoDataFrame with the categorical column
    adm2_gdf.plot(column=map_column, ax=ax, legend=True, cmap=cmap, legend_kwds={'bbox_to_anchor': (1, 1)})

    # Add FIRST_DNAM names on the map with black font
    for idx, row in adm2_gdf.iterrows():
        centroid = row['geometry'].centroid
        ax.annotate(text=row.name, xy=(centroid.x, centroid.y), color='black', fontsize=10, ha='center')

    # Remove the axis
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
        file_name=f"{image_name}.png",
        mime="image/png"
    )

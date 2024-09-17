import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap, to_hex

st.image("icf_sl (1).jpg", caption="MAP GENERATOR", use_column_width=True)

# Load shapefile and Excel data
gdf = gpd.read_file("https://raw.githubusercontent.com/mohamedsillahkanu/si/2b7f982174b609f9647933147dec2a59a33e736a/Chiefdom%202021.shp")
df = pd.read_excel("/tmp/uploaded.xlsx")

# User input for columns and settings
shapefile_columns = st.multiselect("Select Shapefile Column(s):", gdf.columns)
excel_columns = st.multiselect("Select Excel Column(s):", df.columns)
map_column = st.selectbox("Select Map Column:", df.columns)
map_title = st.text_input("Map Title:")
legend_title = st.text_input("Legend Title:")
image_name = st.text_input("Image Name:", value="map_image")
font_size = st.slider("Font Size (for Map Title):", min_value=8, max_value=24, value=15)
color_palette_name = st.selectbox("Color Palette:", options=list(plt.colormaps()), index=list(plt.colormaps()).index('Set3'))

line_color = st.selectbox("Select Default Line Color:", options=["White", "Black", "Red"], index=1)
line_width = st.slider("Select Default Line Width:", min_value=0.5, max_value=5.0, value=2.5)

missing_value_color = st.selectbox("Select Color for Missing Values:", options=["White", "Gray", "Red"], index=1)
missing_value_label = st.text_input("Label for Missing Values:", value="No Data")

# Initialize category_counts
category_counts = {}

variable_type = st.radio("Select the variable type:", options=["Categorical", "Numeric"])

if variable_type == "Categorical":
    unique_values = sorted(df[map_column].dropna().unique().tolist())
    selected_categories = st.multiselect(f"Select Categories for the Legend of {map_column}:", unique_values, default=unique_values)
    category_counts = df[map_column].value_counts().to_dict()

    # Reorder the categories to match the selected categories order
    df[map_column] = pd.Categorical(df[map_column], categories=selected_categories, ordered=True)

    # Ensure the counts for each category remain consistent
    for category in selected_categories:
        if category not in category_counts:
            category_counts[category] = 0

elif variable_type == "Numeric":
    try:
        bin_labels_input = st.text_input("Enter labels for bins (comma-separated, e.g., '10-20.5, 20.6-30.1, >30.2'): ")
        bin_labels = [label.strip() for label in bin_labels_input.split(',')]

        bins = []
        for label in bin_labels:
            if '>' in label:
                lower = float(label.replace('>', '').strip())
                bins.append(lower)
            elif '-' in label:
                lower, upper = map(float, label.split('-'))
                bins.append(lower)
                bins.append(upper)
            else:
                st.error("Incorrect format. Please enter ranges as 'lower-upper' or '>lower'.")

        bins = sorted(list(set(bins)))
        if bins[-1] < df[map_column].max():
            bins.append(df[map_column].max() + 1)  # Adjust the max bin to include the max value

        df[map_column + "_bins"] = pd.cut(df[map_column], bins=bins, labels=bin_labels, include_lowest=True)
        map_column = map_column + "_bins"
        selected_categories = bin_labels
        category_counts = df[map_column].value_counts().to_dict()

    except ValueError:
        st.error(f"Error: The column '{map_column}' contains non-numeric data or cannot be converted to numeric values.")

# Get colors from the selected palette (max 9 colors)
cmap = plt.get_cmap(color_palette_name)
num_colors = min(9, cmap.N)
colors = [to_hex(cmap(i / (num_colors - 1))) for i in range(num_colors)]

color_mapping = {category: colors[i % num_colors] for i, category in enumerate(selected_categories)}

if st.checkbox("Select Colors for Columns"):
    for i, category in enumerate(selected_categories):
        color_mapping[category] = st.selectbox(f"Select Color for '{category}' in {map_column}:", options=colors, index=i)

# Check if columns are selected for merging
if len(shapefile_columns) == 2 and len(excel_columns) == 2:
    column1_line_color = st.selectbox(f"Select Line Color for '{shapefile_columns[0]}' boundaries:", options=["White", "Black", "Red"], index=1)
    column1_line_width = st.slider(f"Select Line Width for '{shapefile_columns[0]}' boundaries:", min_value=0.5, max_value=10.0, value=2.5)
    column2_line_color = st.selectbox(f"Select Line Color for '{shapefile_columns[1]}' boundaries:", options=["White", "Black", "Red"], index=1)
    column2_line_width = st.slider(f"Select Line Width for '{shapefile_columns[1]}' boundaries:", min_value=0.5, max_value=10.0, value=2.5)
elif len(shapefile_columns) == 1 and len(excel_columns) == 1:
    column1_line_color = st.selectbox(f"Select Line Color for '{shapefile_columns[0]}' boundaries:", options=["White", "Black", "Red"], index=1)
    column1_line_width = st.slider(f"Select Line Width for '{shapefile_columns[0]}' boundaries:", min_value=0.5, max_value=10.0, value=2.5)
    column2_line_color = None
    column2_line_width = None
else:
    st.warning("Please select the same number of columns from the shapefile and Excel file (either one or two).")

# Checkboxes for optional features
show_category_counts = st.checkbox("Show Category Counts in Legend", value=True)
show_missing_value_label = st.checkbox("Show Missing Value Label", value=True)
show_first_dnam = st.checkbox("Show FIRST_DNAM in Plots", value=True)
show_first_chie = st.checkbox("Show FIRST_CHIE in Plots", value=True)

if st.button("Generate Map"):
    try:
        # Merge the shapefile and Excel data based on the selected columns
        merged_gdf = gdf
        if len(shapefile_columns) == 2 and len(excel_columns) == 2:
            merged_gdf = merged_gdf.merge(df, left_on=shapefile_columns, right_on=excel_columns, how='left')
        elif len(shapefile_columns) == 1 and len(excel_columns) == 1:
            merged_gdf = merged_gdf.merge(df, left_on=shapefile_columns[0], right_on=excel_columns[0], how='left')

        if map_column not in merged_gdf.columns:
            st.error(f"The column '{map_column}' does not exist in the merged dataset.")
        else:
            # Plot the general map with the legend
            fig, ax = plt.subplots(1, 1, figsize=(12, 12))
            
            # Set default line color and width
            boundary_color = line_color.lower()
            boundary_width = line_width
            
            # Plot boundaries with the selected line width
            merged_gdf.boundary.plot(ax=ax, edgecolor=boundary_color, linewidth=boundary_width)
            
            # Apply custom colors if specified
            custom_cmap = ListedColormap([color_mapping.get(cat, missing_value_color.lower()) for cat in selected_categories])
            
            # Plot the map data with categories
            merged_gdf.plot(column=map_column, ax=ax, linewidth=boundary_width, edgecolor=boundary_color, cmap=custom_cmap,
                            legend=False, missing_kwds={'color': missing_value_color.lower(), 'edgecolor': boundary_color, 'label': missing_value_label})
            
            ax.set_title(f"{map_title} (General Map)", fontsize=font_size, fontweight='bold')
            ax.set_axis_off()
            
            # Create legend handles with category counts if enabled
            handles = []
            for cat in selected_categories:
                if show_category_counts:
                    label_with_count = f"{cat} ({category_counts.get(cat, 0)})"
                else:
                    label_with_count = cat
                handles.append(Patch(color=color_mapping.get(cat, missing_value_color.lower()), label=label_with_count))
            
            if show_missing_value_label:
                handles.append(Patch(color=missing_value_color.lower(), label=missing_value_label))
            
            # Add legend to the map
            ax.legend(handles=handles, title=legend_title, title_fontsize='13', fontsize='10', loc='upper right')
            
            # Save and display the map
            plt.savefig(f"{image_name}.png", dpi=300, bbox_inches='tight')
            st.image(f"{image_name}.png", caption="Generated Map", use_column_width=True)

            st.success(f"Map has been successfully generated and saved as {image_name}.png")

    except Exception as e:
        st.error(f"An error occurred: {e}")


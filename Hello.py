import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap, to_hex

st.image("icf_sl (1).jpg", caption="MAP GENERATOR", use_column_width=True)
gdf = gpd.read_file("https://raw.githubusercontent.com/mohamedsillahkanu/si/2b7f982174b609f9647933147dec2a59a33e736a/Chiefdom%202021.shp")
df = pd.read_excel("/tmp/uploaded.xlsx")

shapefile_columns = st.multiselect("Select Shapefile Column(s):", gdf.columns)
excel_columns = st.multiselect("Select Excel Column(s):", df.columns)
map_column = st.selectbox("Select Map Column:", df.columns)
map_title = st.text_input("Map Title:")
legend_title = st.text_input("Legend Title:")
image_name = st.text_input("Image Name:", value="map_image")
font_size = st.slider("Font Size (for Map Title):", min_value=8, max_value=24, value=15)
color_palette_name = st.selectbox("Color Palette:", options=list(plt.colormaps()), index=list(plt.colormaps()).index('Set3'))

# General map line color and width
general_line_color = st.selectbox("Select Line Color for General Map Boundaries:", options=["None", "White", "Black", "Red"], index=1)
general_line_width = st.slider("Select Line Width for General Map Boundaries:", min_value=0.5, max_value=5.0, value=2.5)

# FIRST_DNAM subplots line color and width
first_dnam_line_color = st.selectbox("Select Line Color for FIRST_DNAM Subplots Boundaries:", options=["None", "White", "Black", "Red"], index=1)
first_dnam_line_width = st.slider("Select Line Width for FIRST_DNAM Subplots Boundaries:", min_value=0.5, max_value=5.0, value=2.5)

# FIRST_CHIE line color and width
general_first_chie_line_color = st.selectbox("Select Line Color for FIRST_CHIE in General Map:", options=["None", "White", "Black", "Red"], index=1)
general_first_chie_line_width = st.slider("Select Line Width for FIRST_CHIE in General Map:", min_value=0.5, max_value=5.0, value=2.5)
subplot_first_chie_line_color = st.selectbox("Select Line Color for FIRST_CHIE in FIRST_DNAM Subplots:", options=["None", "White", "Black", "Red"], index=1)
subplot_first_chie_line_width = st.slider("Select Line Width for FIRST_CHIE in FIRST_DNAM Subplots:", min_value=0.5, max_value=5.0, value=2.5)

missing_value_color = st.selectbox("Select Color for Missing Values:", options=["None", "White", "Gray", "Red"], index=1)
missing_value_label = st.text_input("Label for Missing Values:", value="No Data")

show_label_counts = st.checkbox("Show Label Counts in Legend", value=True)
show_missing_data = st.checkbox("Show Missing Data in Legend", value=True)

category_counts = {}

variable_type = st.radio("Select the variable type:", options=["Categorical", "Numeric"])

if variable_type == "Categorical":
    unique_values = sorted(df[map_column].dropna().unique().tolist())
    selected_categories = st.multiselect(f"Select Categories for the Legend of {map_column}:", unique_values, default=unique_values)
    category_counts = df[map_column].value_counts().to_dict()

    df[map_column] = pd.Categorical(df[map_column], categories=selected_categories, ordered=True)
    for category in selected_categories:
        if category not in category_counts:
            category_counts[category] = 0

elif variable_type == "Numeric":
    try:
        bin_labels_input = st.text_input("Enter labels for bins (comma-separated, e.g., '10-20.5, 20.6-30.1, >30.2'):").strip()
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
                break

        bins = sorted(list(set(bins)))
        if bins[-1] < df[map_column].max():
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

if len(shapefile_columns) == 2 and len(excel_columns) == 2:
    column1_line_color = st.selectbox(f"Select Line Color for '{shapefile_columns[0]}' boundaries:", options=["None", "White", "Black", "Red"], index=1)
    column1_line_width = st.slider(f"Select Line Width for '{shapefile_columns[0]}' boundaries:", min_value=0.5, max_value=10.0, value=2.5)
    column2_line_color = st.selectbox(f"Select Line Color for '{shapefile_columns[1]}' boundaries:", options=["None", "White", "Black", "Red"], index=1)
    column2_line_width = st.slider(f"Select Line Width for '{shapefile_columns[1]}' boundaries:", min_value=0.5, max_value=10.0, value=2.5)
elif len(shapefile_columns) == 1 and len(excel_columns) == 1:
    column1_line_color = st.selectbox(f"Select Line Color for '{shapefile_columns[0]}' boundaries:", options=["None", "White", "Black", "Red"], index=1)
    column1_line_width = st.slider(f"Select Line Width for '{shapefile_columns[0]}' boundaries:", min_value=0.5, max_value=10.0, value=2.5)
    column2_line_color = None
    column2_line_width = None
else:
    st.warning("Please select the same number of columns from the shapefile and Excel file (either one or two).")

display_option = st.radio("Select Display Option:", options=["General Map", "Maps for Each Unique FIRST_DNAM"])

if st.button("Generate Map"):
    try:
        merged_gdf = gdf
        if len(shapefile_columns) == 2 and len(excel_columns) == 2:
            merged_gdf = merged_gdf.merge(df, left_on=shapefile_columns, right_on=excel_columns, how='left')
        elif len(shapefile_columns) == 1 and len(excel_columns) == 1:
            merged_gdf = merged_gdf.merge(df, left_on=shapefile_columns[0], right_on=excel_columns[0], how='left')

        if map_column not in merged_gdf.columns:
            st.error(f"The column '{map_column}' does not exist in the merged dataset.")
        else:
            if display_option == "General Map":
                fig, ax = plt.subplots(1, 1, figsize=(12, 12))
                merged_gdf.boundary.plot(ax=ax, edgecolor=general_line_color.lower() if general_line_color != 'None' else 'black', linewidth=general_line_width)
                merged_gdf.plot(column=map_column, ax=ax, linewidth=general_line_width, edgecolor=general_line_color.lower() if general_line_color != 'None' else 'black', cmap=cmap,
                                legend=False, missing_kwds={'color': missing_value_color.lower() if missing_value_color != 'None' else 'gray', 'edgecolor': general_line_color.lower() if general_line_color != 'None' else 'black', 'label': missing_value_label if missing_value_label else None})

                # Add text labels for each `FIRST_CHIE`
                for idx, row in merged_gdf.iterrows():
                    ax.text(row.geometry.centroid.x, row.geometry.centroid.y, row['FIRST_CHIE'], fontsize=10, ha='center', color='black', fontweight='bold')

                ax.set_title(map_title, fontsize=font_size, fontweight='bold')
                ax.set_axis_off()

                # Create general legend
                handles = []
                for cat in selected_categories:
                    handles.append(Patch(color=color_mapping.get(cat, 'gray'), label=cat))

                if show_missing_data and missing_value_color != 'None':
                    handles.append(Patch(color=missing_value_color.lower(), label=f"{missing_value_label}"))

                ax.legend(handles=handles, title=legend_title, bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False, prop={'weight': 'bold'})

                # Save or display general map
                general_map_path = f"/tmp/{image_name}_general.png"
                plt.savefig(general_map_path, dpi=300, bbox_inches='tight')
                st.image(general_map_path, caption="General Map", use_column_width=True)
                plt.close(fig)

            elif display_option == "Maps for Each Unique FIRST_DNAM":
                first_dnam_values = merged_gdf['FIRST_DNAM'].unique()

                for value in first_dnam_values:
                    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
                    subset_gdf = merged_gdf[merged_gdf['FIRST_DNAM'] == value]

                    # Set line color and width for FIRST_DNAM subplots
                    subset_boundary_color = first_dnam_line_color.lower() if first_dnam_line_color != 'None' else 'black'
                    subset_boundary_width = first_dnam_line_width if first_dnam_line_width else 1

                    subset_gdf.boundary.plot(ax=ax, edgecolor=subset_boundary_color, linewidth=subset_boundary_width)
                    subset_gdf.plot(column=map_column, ax=ax, linewidth=subset_boundary_width, edgecolor=subset_boundary_color, cmap=cmap,
                                    legend=False, missing_kwds={'color': missing_value_color.lower() if missing_value_color != 'None' else 'gray', 'edgecolor': subset_boundary_color, 'label': missing_value_label if missing_value_label else None})

                    # Add text labels for each `FIRST_CHIE`
                    for idx, row in subset_gdf.iterrows():
                        ax.text(row.geometry.centroid.x, row.geometry.centroid.y, row['FIRST_CHIE'], fontsize=10, ha='center', color='black', fontweight='bold')

                    ax.set_title(f"{map_title} - {value}", fontsize=font_size, fontweight='bold')
                    ax.set_axis_off()

                    # Create legend handles with category counts if checkbox is selected
                    handles = []
                    for cat in selected_categories:
                        label_with_count = f"{cat} ({category_counts.get(cat, 0)})" if show_label_counts else cat
                        handles.append(Patch(color=color_mapping.get(cat, 'gray'), label=label_with_count))

                    if show_missing_data and missing_value_color != 'None':
                        handles.append(Patch(color=missing_value_color.lower(), label=f"{missing_value_label} ({subset_gdf[map_column].isna().sum()})"))

                    ax.legend(handles=handles, title=legend_title, bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False, prop={'weight': 'bold'})

                    # Save or display each subplot
                    subplot_path = f"/tmp/{image_name}_{value}.png"
                    plt.savefig(subplot_path, dpi=300, bbox_inches='tight')
                    st.image(subplot_path, caption=f"Map for {value}", use_column_width=True)
                    plt.close(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")

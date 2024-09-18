import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap, to_hex

# Title and image display
st.image("icf_sl (1).jpg", caption="MAP GENERATOR", use_column_width=True)

# Load the shapefile
gdf = gpd.read_file("https://raw.githubusercontent.com/mohamedsillahkanu/si/2b7f982174b609f9647933147dec2a59a33e736a/Chiefdom%202021.shp")

# Prompt the user to upload the Excel file
uploaded_file = st.file_uploader("Upload your Excel file:", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Automatically select the Shapefile columns
    shapefile_columns = ["FIRST_DNAM", "FIRST_CHIE"]
    
    # Exclude specified columns from the map_column selection
    excluded_columns = ["FIRST_DNAM", "FIRST_CHIE", "adm3"]
    selectable_excel_columns = [col for col in df.columns if col not in excluded_columns]
    map_column = st.selectbox("Select Map Column:", selectable_excel_columns)

    # Inputs for map title, legend title, etc.
    map_title = st.text_input("Map Title:")
    legend_title = st.text_input("Legend Title:")
    font_size = st.slider("Font Size (for Map Title):", min_value=8, max_value=24, value=15)
    color_palette_name = st.selectbox("Color Palette:", options=list(plt.colormaps()), index=list(plt.colormaps()).index('Set3'))

    # Line width and color for FIRST_DNAM and FIRST_CHIE
    line_width_dnam = st.slider("Select Line Width for FIRST_DNAM:", min_value=0.5, max_value=5.0, value=2.5)
    line_color_dnam = st.color_picker("Select Line Color for FIRST_DNAM:", "#000000")
    
    line_width_chie = st.slider("Select Line Width for FIRST_CHIE:", min_value=0.5, max_value=5.0, value=2.5)
    line_color_chie = st.color_picker("Select Line Color for FIRST_CHIE:", "#000000")

    # Missing value color and label
    missing_value_color = st.selectbox("Select Color for Missing Values:", options=["", "White", "Gray", "Red"], index=1)
    missing_value_label = st.text_input("Label for Missing Values:", value="No Data")

    # Optional category counter selection
    show_category_counter = st.checkbox("Show Category Counts", value=False)
    category_counts = {}

    # Variable type selection (Categorical or Numeric)
    variable_type = st.radio("Select the variable type:", options=["Categorical", "Numeric"])

    # Handle Categorical variables
    if variable_type == "Categorical":
        unique_values = sorted(df[map_column].dropna().unique().tolist())
        selected_categories = st.multiselect(f"Select Categories for the Legend of {map_column}:", unique_values, default=unique_values)
        if show_category_counter:
            category_counts = df[map_column].value_counts().to_dict()

        # Reorder categories
        df[map_column] = pd.Categorical(df[map_column], categories=selected_categories, ordered=True)

    # Handle Numeric variables
    elif variable_type == "Numeric":
        try:
            bin_labels_input = st.text_input("Enter labels for bins (comma-separated, e.g., '10-20, 20-30, >30'):")
            bin_labels = [label.strip() for label in bin_labels_input.split(',')]
            
            # Generate bins based on user input
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
                    st.error("Please enter valid ranges (e.g., 'lower-upper' or '>lower').")

            bins = sorted(list(set(bins)))
            if bins[-1] < df[map_column].max():
                bins.append(df[map_column].max() + 1)
            
            df[map_column + "_bins"] = pd.cut(df[map_column], bins=bins, labels=bin_labels, include_lowest=True)
            map_column = map_column + "_bins"
            selected_categories = bin_labels

            if show_category_counter:
                category_counts = df[map_column].value_counts().to_dict()

        except ValueError:
            st.error(f"Error: The column '{map_column}' contains non-numeric data or cannot be converted.")

    # Generate color mapping
    cmap = plt.get_cmap(color_palette_name)
    num_colors = min(9, cmap.N)
    colors = [to_hex(cmap(i / (num_colors - 1))) for i in range(num_colors)]
    color_mapping = {category: colors[i % num_colors] for i, category in enumerate(selected_categories)}

    # Color selection option
    if st.checkbox("Select Colors for Columns"):
        for i, category in enumerate(selected_categories):
            color_mapping[category] = st.selectbox(f"Select Color for '{category}' in {map_column}:", options=colors, index=i)

    # Generate the map
    if st.button("Generate Map"):
        try:
            # Merge shapefile and Excel data
            merged_gdf = gdf.merge(df, left_on=shapefile_columns, right_on=["FIRST_DNAM", "FIRST_CHIE"], how='left')

            if map_column not in merged_gdf.columns:
                st.error(f"The column '{map_column}' does not exist in the merged dataset.")
            else:
                fig, ax = plt.subplots(1, 1, figsize=(10, 10))

                # Apply custom colors
                custom_cmap = ListedColormap([color_mapping[cat] for cat in selected_categories])
                merged_gdf.plot(column=map_column, ax=ax, linewidth=line_width_dnam, edgecolor=line_color_dnam, cmap=custom_cmap, 
                                legend=False, missing_kwds={'color': missing_value_color.lower(), 'edgecolor': line_color_dnam, 'label': missing_value_label})
                ax.set_title(map_title, fontsize=font_size, fontweight='bold')
                ax.set_axis_off()

                # Apply line style for FIRST_CHIE
                merged_gdf.boundary.plot(ax=ax, linewidth=line_width_chie, edgecolor=line_color_chie)

                # Add the legend
                if show_category_counter:
                    handles = [Patch(color=color_mapping[cat], label=f"{cat} ({category_counts.get(cat, 0)})") for cat in selected_categories]
                    handles.append(Patch(color=missing_value_color.lower(), label=f"{missing_value_label} ({df[map_column].isna().sum()})"))

                    ax.legend(handles=handles, title=legend_title, fontsize=10, loc='lower left', bbox_to_anchor=(-0.5, 0), 
                              frameon=True, framealpha=1, edgecolor='black', fancybox=True)

                # Display the map using st.pyplot
                st.pyplot(fig)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

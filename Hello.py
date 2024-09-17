import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap, to_hex
import requests
from io import BytesIO

# Direct URL to the shapefile on GitHub
shapefile_base_url = "https://github.com/mohamedsillahkanu/si/raw/e1c761955bbbb09b49d5ab40d51409632a71395c/"
shapefile_name = "Chiefdom 2021"

# Function to download shapefile and associated files
def download_shapefile(base_url, file_name):
    files = ['.shp', '.shx', '.dbf']
    local_files = []
    for file_extension in files:
        url = f"{base_url}{file_name}{file_extension}"
        response = requests.get(url)
        response.raise_for_status()
        local_file = f"/tmp/{file_name}{file_extension}"
        with open(local_file, "wb") as f:
            f.write(response.content)
        local_files.append(local_file)
    return local_files

# Download shapefile
shapefile_files = download_shapefile(shapefile_base_url, shapefile_name)
gdf = gpd.read_file(shapefile_files[0])

st.image("icf_sl (1).jpg", caption="MAP GENERATOR", use_column_width=True)

# User uploads Excel file
uploaded_excel_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_excel_file:
    df = pd.read_excel(uploaded_excel_file)

    # Streamlit components
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

    # Initialize category_counts
    category_counts = {}

    # Categorical or Numeric variable selection as radio buttons
    variable_type = st.radio("Select the variable type:", options=["Categorical", "Numeric"])
    if variable_type == "Categorical":
        unique_values = sorted(df[map_column].dropna().unique().tolist())
        selected_categories = st.multiselect(f"Select Categories for the Legend of {map_column}:", unique_values, default=unique_values)
        category_counts = df[map_column].value_counts().to_dict()  # Preserve original counts

        # Reorder the categories to match the selected categories order
        df[map_column] = pd.Categorical(df[map_column], categories=selected_categories, ordered=True)

        # Ensure the counts for each category remain consistent
        for category in selected_categories:
            if category not in category_counts:
                category_counts[category] = 0

    elif variable_type == "Numeric":
        try:
            # Allow user to input custom labels for bins, accepting decimal intervals
            bin_labels_input = st.text_input("Enter labels for bins (comma-separated, e.g., '10-20.5, 20.6-30.1, >30.2'): ")
            bin_labels = [label.strip() for label in bin_labels_input.split(',')]

            # Convert the labels into bin ranges, supporting decimal points
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

            # Ensure that the bins list ends with the max value in the data
            bins = sorted(list(set(bins)))
            if bins[-1] < df[map_column].max():
                bins.append(df[map_column].max() + 1)  # Adjust the max bin to include the max value

            # Perform binning
            df[map_column + "_bins"] = pd.cut(df[map_column], bins=bins, labels=bin_labels, include_lowest=True)
            map_column = map_column + "_bins"
            selected_categories = bin_labels

            # Calculate counts for the binned categories
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

    # Check if two columns are selected for merging
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
                fig, ax = plt.subplots(1, 1, figsize=(10, 10))
                merged_gdf.plot(column=map_column, ax=ax, legend=True, cmap=ListedColormap(colors), legend_kwds={"label": map_column})

                # Plot boundaries with custom line settings
                if len(shapefile_columns) == 2 and len(excel_columns) == 2:
                    merged_gdf.boundary.plot(ax=ax, linewidth=column1_line_width, edgecolor=column1_line_color.lower())
                elif len(shapefile_columns) == 1 and len(excel_columns) == 1:
                    merged_gdf.boundary.plot(ax=ax, linewidth=column1_line_width, edgecolor=column1_line_color.lower())

                # Customize the map title and legend
                if map_title:
                    ax.set_title(map_title, fontsize=font_size)

                legend_labels = [Patch(color=color_mapping[cat], label=cat) for cat in selected_categories]
                ax.legend(handles=legend_labels, title=legend_title, fontsize=font_size)

                st.pyplot(fig)

                # Save and display the image
                fig.savefig(f"{image_name}.png", dpi=300, bbox_inches='tight')
                with open(f"{image_name}.png", "rb") as file:
                    st.download_button(label="Download Map Image", data=file, file_name=f"{image_name}.png", mime="image/png")

        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    st.warning("Please upload an Excel file.")

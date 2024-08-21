import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap, to_hex


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

    try:
        gdf = gpd.read_file("/tmp/uploaded.shp")
    except Exception as e:
        st.error(f"Error loading shapefile: {e}")
    else:
        df = pd.read_excel("/tmp/uploaded.xlsx")

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
                bin_labels_input = st.text_input("Enter labels for bins (comma-separated, e.g., '10-20.5, 20.6-30.1, >30.2'):")
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

                    # Apply custom colors if specified
                    custom_cmap = ListedColormap([color_mapping[cat] for cat in selected_categories])

                    # Plot the main map with default line settings
                    merged_gdf.plot(column=map_column, ax=ax, linewidth=line_width, edgecolor=line_color.lower(), cmap=custom_cmap, 
                                    legend=False, missing_kwds={'color': missing_value_color.lower(), 'edgecolor': line_color.lower(), 'label': missing_value_label})
                    ax.set_title(map_title, fontsize=font_size, fontweight='bold')
                    ax.set_axis_off()

                    # Dissolve the GeoDataFrame by a column if specified
                    if len(shapefile_columns) > 0:
                        dissolved_gdf = merged_gdf.dissolve(by=shapefile_columns[0])
                        dissolved_gdf.boundary.plot(ax=ax, edgecolor=column1_line_color.lower(), linewidth=column1_line_width)
                        if len(shapefile_columns) > 1:
                            dissolved_gdf2 = merged_gdf.dissolve(by=shapefile_columns[1])
                            dissolved_gdf2.boundary.plot(ax=ax, edgecolor=column2_line_color.lower(), linewidth=column2_line_width)

                    # Create legend handles with category counts
                    handles = []
                    for cat in selected_categories:
                        label_with_count = f"{cat} ({category_counts.get(cat, 0)})"
                        handles.append(Patch(color=color_mapping[cat], label=label_with_count))

                    # Add missing value handle
                    handles.append(Patch(color=missing_value_color.lower(), label=f"{missing_value_label} ({df[map_column].isna().sum()})"))

                    # Customize and position the legend in the lower left outside the map
                    legend = ax.legend(
                        handles=handles, 
                        title=legend_title, 
                        fontsize=14, 
                        loc='lower left', 
                        bbox_to_anchor=(-0.5, 0),  # Lower-left position outside the map
                        frameon=True, 
                        framealpha=1, 
                        edgecolor='black', 
                        fancybox=True
                    )

                    # Bold the title and categories
                    plt.setp(legend.get_title(), fontsize=16, fontweight='bold')
                    plt.setp(legend.get_texts(), fontsize=14, fontweight='bold')

                    # Draw a rectangular box around the legend
                    legend.get_frame().set_linewidth(2)
                    legend.get_frame().set_edgecolor('black')
                    legend.get_frame().set_boxstyle('Round,pad=0.5,rounding_size=0.5')

                    # Customize missing data label
                    for text in legend.get_texts():
                        if text.get_text() == missing_value_label:
                            text.set_fontsize(14)
                            text.set_fontweight('bold')

                    st.pyplot(fig)


                    # Save the figure and provide download button
                    image_path = f"/tmp/{image_name}_{map_column}.png"
                    fig.savefig(image_path, bbox_inches='tight')
                    with open(image_path, "rb") as img:
                        st.download_button(label="Download Image", data=img, file_name=f"{image_name}_{map_column}.png", mime="image/png")


            except Exception as e:
                st.error(f"Error generating map: {e}")

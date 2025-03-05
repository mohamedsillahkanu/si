import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
import io
from matplotlib.patches import Patch

# Display the App Header
st.set_page_config(layout="wide", page_title="Map Generator")
st.image("icf_sl (1).jpg", caption="MAP GENERATOR", use_column_width=True)

# Load the shapefile
@st.cache_data
def load_shapefile():
    return gpd.read_file("https://raw.githubusercontent.com/mohamedsillahkanu/si/2b7f982174b609f9647933147dec2a59a33e736a/Chiefdom%202021.shp")

try:
    gdf = load_shapefile()
    # Clean shapefile string columns
    gdf['FIRST_DNAM'] = gdf['FIRST_DNAM'].str.strip()
    gdf['FIRST_CHIE'] = gdf['FIRST_CHIE'].str.strip()
except Exception as e:
    st.error(f"Error loading shapefile: {e}")
    st.stop()

# File upload (Excel or CSV)
uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        # Read the uploaded file
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        
        # Clean dataframe string columns if they exist
        if 'FIRST_DNAM' in df.columns:
            df['FIRST_DNAM'] = df['FIRST_DNAM'].str.strip()
        if 'FIRST_CHIE' in df.columns:
            df['FIRST_CHIE'] = df['FIRST_CHIE'].str.strip()
        
        # Check if required join columns exist
        required_columns = ['FIRST_DNAM', 'FIRST_CHIE']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Required columns missing in data: {', '.join(missing_columns)}")
            st.info("Your data needs to have FIRST_DNAM and FIRST_CHIE columns for joining with the map.")
            st.stop()
        
        # Exclude certain columns from being selectable for the map
        excluded_columns = ['FIRST_DNAM', 'FIRST_CHIE', 'adm3', 'geometry', 'SHAPE_Area', 'SHAPE_Leng']
        available_columns = [col for col in df.columns if col not in excluded_columns]
        
        if not available_columns:
            st.error("No valid columns found for mapping after excluding system columns.")
            st.stop()

        # UI elements for selecting map settings
        col1, col2 = st.columns(2)
        
        with col1:
            map_column = st.selectbox("Select Map Column:", available_columns)
            map_title = st.text_input("Map Title:", value=map_column)
            legend_title = st.text_input("Legend Title:", value=map_column)
            image_name = st.text_input("Image Name:", value=f"{map_column}_map")
        
        with col2:
            font_size = st.slider("Font Size (Title):", min_value=8, max_value=24, value=15)
            # Color selection method
            color_selection = st.radio("Select Color Mode:", ["Predefined Palette", "Manual Colors"])
            # Default Line Color & Width Selection
            line_colors = ["White", "Light Gray", "Gray", "Dark Gray", "Black", "Red", "Blue", "Green", "Yellow", "Orange", "Purple"]
            line_color = st.selectbox("Line Color:", options=line_colors, index=4)  # Black as default
            line_width = st.slider("Line Width:", min_value=0.1, max_value=3.0, value=0.5, step=0.1)

        # Merge data with shapefile
        merged_gdf = gdf.merge(df, on=['FIRST_DNAM', 'FIRST_CHIE'], how='left', validate='1:1')
        
        # Check if merge was successful
        if len(merged_gdf) == 0:
            st.error("Merging resulted in an empty dataset. Check if the district and chiefdom names match.")
            st.stop()
        
        # Determine if selected column is categorical or numeric
        is_categorical = False
        if map_column in merged_gdf.columns:
            if not pd.api.types.is_numeric_dtype(merged_gdf[map_column]):
                is_categorical = True
            else:
                # Check if numeric column has few unique values (treat as categorical)
                unique_values = merged_gdf[map_column].nunique()
                if unique_values <= 10:  # Threshold for treating as categorical
                    is_categorical = True
                    st.info(f"Treating numeric column with {unique_values} unique values as categorical")
        
        # Handle coloring based on data type
        if is_categorical:
            # Handle categorical data
            categories = merged_gdf[map_column].dropna().unique()
            
            if color_selection == "Predefined Palette":
                color_palette_name = st.selectbox(
                    "Color Palette:", 
                    options=['tab10', 'tab20', 'Set1', 'Set2', 'Set3', 'Pastel1', 'Pastel2', 'Paired', 'Accent'],
                    index=2
                )
                cmap = plt.get_cmap(color_palette_name)
                colors = [to_hex(cmap(i % cmap.N)) for i in range(len(categories))]
                color_mapping = dict(zip(categories, colors))
            else:
                # Manual color selection for each category
                color_mapping = {}
                st.write("Select colors for each category:")
                for category in categories:
                    if pd.notna(category):  # Skip NaN values
                        default_color = "#1E88E5"  # Default blue
                        color_mapping[category] = st.color_picker(f"{category}", default_color)
            
            # Missing value settings
            missing_value_color = "#D9D9D9"  # Gray default
            missing_value_color = st.color_picker("Color for Missing Values:", missing_value_color)
            missing_value_label = st.text_input("Label for Missing Values:", value="No Data")
            
            # Create the plot
            fig, ax = plt.subplots(1, 1, figsize=(10, 8), dpi=300)
            
            # Function to get color for each feature
            def get_cat_color(value):
                if pd.isna(value):
                    return missing_value_color
                return color_mapping.get(value, missing_value_color)
            
            # Plot with categorical colors
            merged_gdf.plot(
                column=map_column,
                ax=ax,
                categorical=True,
                legend=False,
                color=merged_gdf[map_column].map(lambda x: get_cat_color(x)),
                edgecolor=line_color.lower(),
                linewidth=line_width
            )
            
            # Add district boundaries with thicker lines
            district_boundaries = merged_gdf.dissolve(by='FIRST_DNAM')
            district_boundaries.boundary.plot(
                ax=ax,
                color='black',
                linewidth=line_width * 2,
                zorder=2
            )
            
            # Create legend elements
            legend_elements = []
            for category in sorted(categories):
                if pd.notna(category):
                    count = len(merged_gdf[merged_gdf[map_column] == category])
                    patch = Patch(
                        facecolor=color_mapping.get(category, missing_value_color),
                        edgecolor='black',
                        linewidth=0.5,
                        label=f"{category} ({count})"
                    )
                    legend_elements.append(patch)
            
            # Add missing value to legend if there are any
            if merged_gdf[map_column].isna().any():
                missing_count = merged_gdf[map_column].isna().sum()
                legend_elements.append(
                    Patch(
                        facecolor=missing_value_color,
                        edgecolor='black',
                        linewidth=0.5,
                        label=f"{missing_value_label} ({missing_count})"
                    )
                )
            
            # Add legend
            if legend_elements:
                ax.legend(
                    handles=legend_elements,
                    title=legend_title,
                    loc='lower right',
                    fontsize=10,
                    title_fontsize=12
                )
            
        else:
            # Handle numeric data
            cmap_options = ['Blues', 'Greens', 'Reds', 'Purples', 'Oranges', 'viridis', 'plasma', 'inferno', 'magma', 'cividis']
            cmap_name = st.selectbox("Color Scale:", options=cmap_options, index=0)
            
            # Create the plot
            fig, ax = plt.subplots(1, 1, figsize=(10, 8), dpi=300)
            
            # Plot with continuous color scale
            merged_gdf.plot(
                column=map_column,
                ax=ax,
                cmap=cmap_name,
                legend=True,
                edgecolor=line_color.lower(),
                linewidth=line_width,
                legend_kwds={
                    'label': legend_title,
                    'orientation': 'horizontal',
                    'shrink': 0.8,
                    'pad': 0.05
                }
            )
            
            # Add district boundaries with thicker lines
            district_boundaries = merged_gdf.dissolve(by='FIRST_DNAM')
            district_boundaries.boundary.plot(
                ax=ax,
                color='black',
                linewidth=line_width * 2,
                zorder=2
            )
        
        # Set title and layout
        ax.set_title(map_title, fontsize=font_size)
        ax.axis("off")
        
        # Show Plot
        st.pyplot(fig)
        
        # Download Map as Image
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight", dpi=300)
        buf.seek(0)
        st.download_button(
            label="Download Map", 
            data=buf, 
            file_name=f"{image_name}.png", 
            mime="image/png"
        )
        
    except Exception as e:
        st.error(f"Error processing data: {e}")
else:
    st.info("Please upload an Excel or CSV file to generate a map. The file should contain FIRST_DNAM and FIRST_CHIE columns for joining with the map data.")

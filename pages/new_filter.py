import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex

# Display Title Image
st.image("icf_sl (1).jpg", caption="MAP GENERATOR", use_column_width=True)

# Load the shapefile
shapefile_url = "https://raw.githubusercontent.com/mohamedsillahkanu/si/2b7f982174b609f9647933147dec2a59a33e736a/Chiefdom%202021.shp"
gdf = gpd.read_file(shapefile_url)

# File Upload
uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)

    # Exclude certain columns
    excluded_columns = ['FIRST_DNAM', 'FIRST_CHIE', 'adm3']
    available_columns = [col for col in df.columns if col not in excluded_columns]

    # User Inputs
    with st.form("map_settings"):
        st.subheader("Map Settings")
        map_column = st.selectbox("Select Map Column:", available_columns)
        map_title = st.text_input("Map Title:")
        legend_title = st.text_input("Legend Title:")
        font_size = st.slider("Font Size:", min_value=8, max_value=24, value=15)

        color_palette_name = st.selectbox("Color Palette:", options=list(plt.colormaps()), index=list(plt.colormaps()).index('Set3'))
        line_color = st.selectbox("Line Color:", options=["White", "Black", "Red"], index=1)
        line_width = st.slider("Line Width:", min_value=0.5, max_value=5.0, value=2.5)

        # Dynamic Filtering Section
        st.subheader("Filter Data (Optional)")
        selected_filters = {}
        for column in available_columns:
            unique_values = sorted(df[column].dropna().unique().tolist())
            selected_value = st.multiselect(f"Select values for {column}:", unique_values, default=unique_values)
            if selected_value:
                selected_filters[column] = selected_value

        submit_button = st.form_submit_button("Generate Map")

    if submit_button:
        # Apply filters dynamically
        if selected_filters:
            for col, values in selected_filters.items():
                df = df[df[col].isin(values)]

        if df.empty:
            st.warning("No data matches the selected filters. Please adjust your selection.")
        else:
            # Merge with Shapefile using both FIRST_DNAM and FIRST_CHIE
            merged_gdf = gdf.merge(df, on=["FIRST_DNAM", "FIRST_CHIE"], how="left")

            # Color Mapping
            unique_categories = sorted(df[map_column].dropna().unique().tolist())
            cmap = plt.get_cmap(color_palette_name)
            num_colors = min(len(unique_categories), cmap.N)
            colors = [to_hex(cmap(i / (num_colors - 1))) for i in range(num_colors)]
            color_mapping = {category: colors[i % num_colors] for i, category in enumerate(unique_categories)}

            # Generate Map
            fig, ax = plt.subplots(figsize=(10, 6))
            merged_gdf.plot(column=map_column, cmap=color_palette_name, linewidth=line_width, edgecolor=line_color.lower(), ax=ax, legend=True)
            ax.set_title(map_title, fontsize=font_size)
            ax.axis("off")

            # Display Map
            st.pyplot(fig)

            # Download Option
            st.download_button(label="Download Map", data=plt.savefig(fname="Generated_Map", format="png"), file_name="Generated_Map.png", mime="image/png")

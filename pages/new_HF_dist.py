import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import numpy as np
import os
import tempfile
from matplotlib.colors import LinearSegmentedColormap
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    layout="wide",
    page_title="Health Facility Map Generator",
    page_icon="🏥",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #3366cc;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #555;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .section-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .info-text {
        background-color: #e7f3fe;
        border-left: 6px solid #2196F3;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .success-message {
        background-color: #e6ffe6;
        border-left: 6px solid #4CAF50;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .sidebar .sidebar-content {
        background-color: #f5f7f9;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
    }
    .download-btn {
        background-color: #3366cc !important;
    }
</style>
""", unsafe_allow_html=True)

# Create sidebar for app navigation and help
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4320/4320371.png", width=100)
    st.markdown("## Navigation")
    
    page = st.radio("", ["Map Generator", "Help & Instructions", "About"])
    
    st.markdown("---")
    st.markdown("### Need Help?")
    with st.expander("FAQ"):
        st.markdown("""
        **Q: What files do I need to upload?**
        
        A: You need to upload 3 shapefile components (.shp, .shx, .dbf) and a facility Excel file with latitude/longitude coordinates.
        
        **Q: What format should my coordinates be in?**
        
        A: Coordinates should be in decimal degrees (e.g., 35.6895, 139.6917).
        
        **Q: Can I customize my map?**
        
        A: Yes! You can change colors, point size, transparency, and add a title.
        """)

# Main content based on selected page
if page == "Map Generator":
    # Header
    st.markdown("<h1 class='main-header'>Interactive Health Facility Map Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p>Create professional geographic visualizations of health facility distribution.</p>", unsafe_allow_html=True)
    
    # Create tabs for workflow steps
    tab1, tab2, tab3 = st.tabs(["1️⃣ Upload Data", "2️⃣ Configure Map", "3️⃣ Results & Download"])
    
    with tab1:
        st.markdown("<div class='section-container'>", unsafe_allow_html=True)
        st.markdown("<h2 class='sub-header'>Upload Your Data Files</h2>", unsafe_allow_html=True)
        
        # Create two columns for file uploads with visual indicators
        col1, col2 = st.columns(2)
        
        # Temporary directory for files
        temp_dir = tempfile.mkdtemp()
        shp_path = os.path.join(temp_dir, "temp.shp")
        shx_path = os.path.join(temp_dir, "temp.shx")
        dbf_path = os.path.join(temp_dir, "temp.dbf")
        
        with col1:
            st.markdown("<h3>Geographic Boundary Files</h3>", unsafe_allow_html=True)
            st.markdown("<p>Upload your shapefiles that define region boundaries:</p>", unsafe_allow_html=True)
            
            shp_file = st.file_uploader("Upload .shp file", type=["shp"], key="shp", 
                                         help="The main shapefile containing geometry data")
            shx_uploaded = False
            if shp_file:
                with open(shp_path, "wb") as f:
                    f.write(shp_file.read())
                st.success("✓ .shp file uploaded")
                
            shx_file = st.file_uploader("Upload .shx file", type=["shx"], key="shx",
                                        help="The index file that stores the index of the geometry")
            if shx_file:
                with open(shx_path, "wb") as f:
                    f.write(shx_file.read())
                st.success("✓ .shx file uploaded")
                
            dbf_file = st.file_uploader("Upload .dbf file", type=["dbf"], key="dbf",
                                        help="The database file that stores attributes")
            if dbf_file:
                with open(dbf_path, "wb") as f:
                    f.write(dbf_file.read())
                st.success("✓ .dbf file uploaded")
        
        with col2:
            st.markdown("<h3>Health Facility Data</h3>", unsafe_allow_html=True)
            st.markdown("<p>Upload your Excel file containing facility locations:</p>", unsafe_allow_html=True)
            
            facility_file = st.file_uploader("Upload facility data (.xlsx)", type=["xlsx"], key="facility",
                                            help="Excel file with facility coordinates and attributes")
            
            if facility_file:
                st.success("✓ Facility data uploaded")
                # Preview sample format
                st.markdown("#### Sample Data Format:")
                sample_df = pd.DataFrame({
                    'facility_name': ['Hospital A', 'Clinic B', 'Pharmacy C'],
                    'w_long': [120.123, 121.456, 119.789],
                    'w_lat': [15.123, 16.456, 14.789],
                    'type': ['Hospital', 'Clinic', 'Pharmacy']
                })
                st.dataframe(sample_df, use_container_width=True, height=150)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='section-container'>", unsafe_allow_html=True)
        st.markdown("<h2 class='sub-header'>Configure Your Map</h2>", unsafe_allow_html=True)
        
        # Check if files are uploaded before showing configuration
        if all([shp_file, shx_file, dbf_file, facility_file]):
            try:
                # Read shapefile
                shapefile = gpd.read_file(shp_path)
                
                # Read facility data
                coordinates_data = pd.read_excel(facility_file)
                
                # Display data preview with expander
                with st.expander("Data Preview", expanded=True):
                    st.dataframe(coordinates_data.head(10), use_container_width=True)
                    st.info(f"Total records: {len(coordinates_data)}")
                
                # Organize customization options
                st.markdown("<h3>Customize Map Appearance</h3>", unsafe_allow_html=True)
                
                # Create three columns for configuration
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("##### Data Mapping")
                    # Coordinate column selection
                    longitude_col = st.selectbox(
                        "Longitude Column",
                        coordinates_data.columns,
                        index=coordinates_data.columns.get_loc("w_long") if "w_long" in coordinates_data.columns else 0
                    )
                    latitude_col = st.selectbox(
                        "Latitude Column",
                        coordinates_data.columns,
                        index=coordinates_data.columns.get_loc("w_lat") if "w_lat" in coordinates_data.columns else 0
                    )
                    
                    # Optional: Category/type field
                    if len(coordinates_data.columns) > 2:
                        category_options = ["None"] + list(coordinates_data.columns)
                        category_col = st.selectbox(
                            "Category Column (Optional)",
                            category_options,
                            index=category_options.index("type") if "type" in category_options else 0
                        )
                    else:
                        category_col = "None"
                
                with col2:
                    st.markdown("##### Style Settings")
                    # Visual customization
                    map_title = st.text_input("Map Title", "Health Facility Distribution")
                    point_size = st.slider("Point Size", 10, 200, 50)
                    point_alpha = st.slider("Point Transparency", 0.1, 1.0, 0.7)
                
                with col3:
                    st.markdown("##### Color Scheme")
                    # Color selection
                    background_colors = {
                        "Light": "#f8f9fa", 
                        "White": "#ffffff",
                        "Beige": "#f5f5dc",
                        "Light Blue": "#e6f2ff",
                        "Light Green": "#e8f5e9"
                    }
                    
                    point_colors = {
                        "Blue": "#1e88e5",
                        "Red": "#e53935",
                        "Green": "#43a047",
                        "Purple": "#8e24aa",
                        "Orange": "#fb8c00",
                        "Teal": "#26a69a"
                    }
                    
                    background_color = st.selectbox(
                        "Background Color", 
                        list(background_colors.keys())
                    )
                    
                    point_color = st.selectbox(
                        "Point Color", 
                        list(point_colors.keys())
                    )
                
                # Advanced settings expander
                with st.expander("Advanced Settings"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        map_width = st.slider("Map Width (inches)", 8, 20, 15)
                        map_height = st.slider("Map Height (inches)", 6, 15, 10)
                        
                    with col2:
                        edge_color = st.color_picker("Boundary Edge Color", "#333333")
                        edge_width = st.slider("Boundary Line Width", 0.1, 2.0, 0.5)
                
                # Button to generate map
                generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])
                with generate_col2:
                    generate_map = st.button("Generate Map", use_container_width=True)
                
            except Exception as e:
                st.error(f"Configuration error: {str(e)}")
                st.info("Please make sure all files are properly formatted and try again.")
        else:
            st.markdown("<div class='info-text'>", unsafe_allow_html=True)
            st.write("Please upload all required files in the 'Upload Data' tab to configure your map.")
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<div class='section-container'>", unsafe_allow_html=True)
        st.markdown("<h2 class='sub-header'>Results & Download</h2>", unsafe_allow_html=True)
        
        # Check if all required files are uploaded and map generation is requested
        if all([shp_file, shx_file, dbf_file, facility_file]) and 'generate_map' in locals() and generate_map:
            try:
                # Data processing
                # Remove missing coordinates
                coordinates_data = coordinates_data.dropna(subset=[longitude_col, latitude_col])
                
                # Filter invalid coordinates
                coordinates_data = coordinates_data[
                    (coordinates_data[longitude_col].between(-180, 180)) &
                    (coordinates_data[latitude_col].between(-90, 90))
                ]
                
                if len(coordinates_data) == 0:
                    st.error("No valid coordinates found in the data after filtering.")
                    st.stop()
                
                # Convert to GeoDataFrame
                geometry = [Point(xy) for xy in zip(coordinates_data[longitude_col], coordinates_data[latitude_col])]
                coordinates_gdf = gpd.GeoDataFrame(coordinates_data, geometry=geometry, crs="EPSG:4326")
                
                # Ensure consistent CRS
                if shapefile.crs is None:
                    shapefile = shapefile.set_crs(epsg=4326)
                else:
                    shapefile = shapefile.to_crs(epsg=4326)
                
                # Calculate aspect ratio based on area
                bounds = shapefile.total_bounds
                mid_y = np.mean([bounds[1], bounds[3]])  # middle latitude
                aspect = 1.0  # default aspect ratio
                
                if -90 < mid_y < 90:  # check if latitude is valid
                    try:
                        aspect = 1 / np.cos(np.radians(mid_y))
                        if not np.isfinite(aspect) or aspect <= 0:
                            aspect = 1.0
                    except:
                        aspect = 1.0
                
                # Create two map options
                map_type = st.radio("Select Map Type", ["Standard Map", "Interactive Map"])
                
                if map_type == "Standard Map":
                    # Create the map with user-defined dimensions
                    fig, ax = plt.subplots(figsize=(map_width, map_height))
                    
                    # Plot shapefile with custom style
                    shapefile.plot(
                        ax=ax, 
                        color=background_colors[background_color], 
                        edgecolor=edge_color, 
                        linewidth=edge_width
                    )
                    
                    # Plot points with custom style - with category if available
                    if category_col != "None" and category_col in coordinates_data.columns:
                        # Get unique categories
                        categories = coordinates_data[category_col].unique()
                        cmap = plt.cm.get_cmap('tab10', len(categories))
                        
                        # Create legend handles
                        handles = []
                        labels = []
                        
                        # Plot each category with different color
                        for i, cat in enumerate(categories):
                            cat_data = coordinates_gdf[coordinates_gdf[category_col] == cat]
                            cat_plot = cat_data.plot(
                                ax=ax,
                                color=cmap(i),
                                markersize=point_size,
                                alpha=point_alpha,
                                label=cat
                            )
                            handles.append(plt.Line2D([0], [0], marker='o', color='w', 
                                                     markerfacecolor=cmap(i), markersize=8))
                            labels.append(cat)
                        
                        # Add legend
                        plt.legend(handles, labels, loc='upper right', title=category_col.title())
                        
                    else:
                        # Plot all points with same color
                        coordinates_gdf.plot(
                            ax=ax,
                            color=point_colors[point_color],
                            markersize=point_size,
                            alpha=point_alpha
                        )
                    
                    # Set aspect ratio
                    ax.set_aspect(aspect)
                    
                    # Customize map appearance
                    plt.title(map_title, fontsize=20, pad=20)
                    plt.axis('off')
                    
                    # Add statistics
                    stats_text = (
                        f"Total Facilities: {len(coordinates_data)}\n"
                        f"Coordinates Range:\n"
                        f"Longitude: {coordinates_data[longitude_col].min():.2f}° to {coordinates_data[longitude_col].max():.2f}°\n"
                        f"Latitude: {coordinates_data[latitude_col].min():.2f}° to {coordinates_data[latitude_col].max():.2f}°"
                    )
                    plt.figtext(0.02, 0.02, stats_text, fontsize=10, 
                                bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))
                    
                    # Add timestamp and author
                    import datetime
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
                    plt.figtext(0.98, 0.02, f"Generated: {timestamp}", fontsize=8, 
                                ha='right', bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.3'))
                    
                    # Display the map
                    st.pyplot(fig)
                    
                    # Save high-resolution PNG
                    output_path_png = os.path.join(temp_dir, "health_facility_map.png")
                    plt.savefig(output_path_png, dpi=300, bbox_inches='tight', pad_inches=0.1)
                    
                    # Download options
                    st.markdown("<h3>Download Options</h3>", unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        with open(output_path_png, "rb") as file:
                            st.download_button(
                                label="Download Map (PNG)",
                                data=file,
                                file_name="health_facility_map.png",
                                mime="image/png"
                            )
                    
                    with col2:
                        # Export coordinates as CSV
                        csv = coordinates_data.to_csv(index=False)
                        st.download_button(
                            label="Download Processed Data (CSV)",
                            data=csv,
                            file_name="processed_coordinates.csv",
                            mime="text/csv"
                        )
                
                else:  # Interactive Map
                    st.write("Interactive map with zoom and hover capabilities:")
                    
                    # Create interactive plotly map
                    if category_col != "None" and category_col in coordinates_data.columns:
                        fig = px.scatter_mapbox(
                            coordinates_data, 
                            lat=latitude_col, 
                            lon=longitude_col,
                            color=category_col,
                            hover_name=category_col,
                            hover_data=coordinates_data.columns,
                            title=map_title,
                            opacity=point_alpha,
                            size_max=point_size/5,  # Adjust size for mapbox
                            zoom=5
                        )
                    else:
                        fig = px.scatter_mapbox(
                            coordinates_data, 
                            lat=latitude_col, 
                            lon=longitude_col,
                            hover_data=coordinates_data.columns,
                            title=map_title,
                            opacity=point_alpha,
                            color_discrete_sequence=[point_colors[point_color]],
                            size_max=point_size/5,  # Adjust size for mapbox
                            zoom=5
                        )
                    
                    # Use Open Street Map as the base map
                    fig.update_layout(
                        mapbox_style="open-street-map",
                        height=800,
                        margin={"r":0,"t":50,"l":0,"b":0}
                    )
                    
                    # Display interactive map
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Download as HTML
                    html_path = os.path.join(temp_dir, "interactive_map.html")
                    fig.write_html(html_path)
                    
                    with open(html_path, "rb") as file:
                        st.download_button(
                            label="Download Interactive Map (HTML)",
                            data=file,
                            file_name="interactive_map.html",
                            mime="text/html"
                        )
                
                # Display summary statistics
                st.markdown("<h3>Summary Statistics</h3>", unsafe_allow_html=True)
                
                metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                
                with metrics_col1:
                    st.metric("Total Facilities", f"{len(coordinates_data)}")
                
                with metrics_col2:
                    st.metric("Geographic Coverage", 
                             f"{abs(coordinates_data[longitude_col].max() - coordinates_data[longitude_col].min()):.1f}° × "
                             f"{abs(coordinates_data[latitude_col].max() - coordinates_data[latitude_col].min()):.1f}°")
                
                with metrics_col3:
                    # If we have categories, show count by category
                    if category_col != "None" and category_col in coordinates_data.columns:
                        # Get top category
                        top_category = coordinates_data[category_col].value_counts().index[0]
                        top_count = coordinates_data[category_col].value_counts().iloc[0]
                        st.metric(f"Top {category_col}", f"{top_category} ({top_count})")
                    else:
                        # Calculate facility density
                        area = (bounds[2] - bounds[0]) * (bounds[3] - bounds[1]) * 111 * 111  # Approx sq km
                        density = len(coordinates_data) / area if area > 0 else 0
                        st.metric("Facility Density", f"{density:.4f} per km²")
                
                # If we have categories, show distribution
                if category_col != "None" and category_col in coordinates_data.columns:
                    st.markdown("<h3>Category Distribution</h3>", unsafe_allow_html=True)
                    
                    # Create pie chart for category distribution
                    cat_counts = coordinates_data[category_col].value_counts()
                    
                    fig = px.pie(values=cat_counts.values, names=cat_counts.index, 
                                title=f"Distribution by {category_col}")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Success message
                st.markdown("<div class='success-message'>", unsafe_allow_html=True)
                st.write("✅ Map generated successfully!")
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred during map generation: {str(e)}")
                st.write("Please check your input files and configuration settings and try again.")
        else:
            if 'generate_map' in locals() and generate_map:
                st.error("Please complete all required uploads before generating the map.")
            else:
                st.info("Configure your map in the previous tab and click 'Generate Map' to see results here.")
        
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Help & Instructions":
    st.markdown("<h1 class='main-header'>Help & Instructions</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>How to Use This Tool</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    ### Step 1: Prepare Your Files
    - **Shapefile Components**: You'll need three files (.shp, .shx, .dbf) that define your geographic boundaries.
    - **Health Facility Data**: Prepare an Excel file (.xlsx) containing facility information with latitude and longitude columns.
    
    ### Step 2: Upload Files
    - Upload all required files in the "Upload Data" tab.
    - The app will validate your files and show a preview of your facility data.
    
    ### Step 3: Configure Your Map
    - Select the correct columns for longitude and latitude.
    - Customize the map appearance (colors, point size, title).
    - Adjust advanced settings if needed.
    - Click "Generate Map" to create your visualization.
    
    ### Step 4: Download and Share
    - View your generated map in the "Results" tab.
    - Download the map as a high-resolution PNG file.
    - Download the processed data as a CSV file.
    - For interactive maps, download as HTML to share with others.
    """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Tips for Better Maps</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Data Preparation
        - Clean your data before uploading
        - Remove or fix invalid coordinates
        - Use consistent naming conventions
        - Include category/type fields if available
        """)
    
    with col2:
        st.markdown("""
        ### Visual Design
        - Choose contrasting colors for better visibility
        - Adjust point size based on map scale
        - Use transparency when points overlap
        - Keep titles concise but descriptive
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Troubleshooting</h2>", unsafe_allow_html=True)
    
    with st.expander("Common Issues"):
        st.markdown("""
        **Issue**: Map doesn't show after generating
        - **Solution**: Check that your coordinates are in the correct format (decimal degrees)
        - **Solution**: Make sure your shapefile and coordinates use compatible coordinate systems
        
        **Issue**: Points appear in wrong locations
        - **Solution**: Verify that longitude and latitude columns are correctly selected
        - **Solution**: Check for any coordinate system mismatches
        
        **Issue**: File upload errors
        - **Solution**: Ensure all required shapefile components (.shp, .shx, .dbf) are from the same set
        - **Solution**: Check Excel file format and column headers
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

else:  # About page
    st.markdown("<h1 class='main-header'>About This Tool</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    st.markdown("""
    ### Health Facility Map Generator
    
    This application was designed to help health professionals, researchers, and planners visualize the geographic distribution of health facilities. With a user-friendly interface, you can quickly generate professional maps without GIS expertise.
    
    #### Features:
    - Support for various geographic regions via shapefiles
    - Both static and interactive map options
    - Customizable visual design
    - Category-based visualization
    - Statistical summaries of facility distribution
    - High-resolution exports for reports and presentations
    
    #### Technologies Used:
    - Streamlit framework
    - GeoPandas for geospatial processing
    - Matplotlib for static visualization
    - Plotly for interactive maps
    - Pandas for data management
    
    #### Version:
    1.0.0
    """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Contact & Support</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    For questions, feature requests, or technical support, please contact:
    
    📧 support@healthmapgenerator.org
    
    Or visit our documentation at [healthmapgenerator.org/docs](https://example.com)
    """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Add footer
footer_html = """
<div style="text-align: center; margin-top: 3rem; padding: 1rem; background-color: #f5f7f9; border-radius: 10px;">
    <p style="color: #666; font-size: 0.8rem;">Health Facility Map Generator © 2025 | Built with Streamlit</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)

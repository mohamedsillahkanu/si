import streamlit as st
import streamlit.components.v1 as components
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import numpy as np
import os
import tempfile
from matplotlib.colors import LinearSegmentedColormap

# Set page configuration
st.set_page_config(
    layout="wide",
    page_title="Health Facility Map Generator",
    page_icon="🏥",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit's default sidebar and menu
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# Particles.js HTML configuration with full page coverage
particles_js = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Particles.js</title>
    <style>
        #particles-js {
            position: fixed;
            width: 100vw;
            height: 100vh;
            top: 0;
            left: 0;
            z-index: 0;
            background-color: transparent;
        }
        
        .content {
            position: relative;
            z-index: 1;
        }
    </style>
</head>
<body>
    <div id="particles-js"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS("particles-js", {
            "particles": {
                "number": {"value": 150, "density": {"enable": true, "value_area": 1500}},
                "color": {"value": "#47B5FF"},
                "shape": {"type": "circle"},
                "opacity": {"value": 0.5, "random": true, "anim": {"enable": true, "speed": 0.2, "opacity_min": 0.1, "sync": false}},
                "size": {"value": 3, "random": true, "anim": {"enable": true, "speed": 2, "size_min": 0.1, "sync": false}},
                "line_linked": {
                    "enable": true,
                    "distance": 120,
                    "color": "#47B5FF",
                    "opacity": 0.15,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": 0.4,
                    "direction": "none",
                    "random": true,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false,
                    "attract": {"enable": true, "rotateX": 600, "rotateY": 1200}
                }
            },
            "interactivity": {
                "detect_on": "window",
                "events": {
                    "onhover": {"enable": true, "mode": "grab"},
                    "onclick": {"enable": true, "mode": "push"},
                    "resize": true
                },
                "modes": {
                    "grab": {"distance": 140, "line_linked": {"opacity": 0.5}},
                    "push": {"particles_nb": 3}
                }
            },
            "retina_detect": true
        });
    </script>
</body>
</html>
"""

# Inject particles.js (full page)
components.html(particles_js, height=0, width=0)

# Styling
st.markdown("""
    <style>
        /* Base styling */
        .stApp {
            background-color: #0E1117 !important;
            color: #E0E0E0 !important;
        }
        
        /* Main content styling */
        .stMarkdown, p, h1, h2, h3 {
            color: #E0E0E0 !important;
            position: relative;
            z-index: 1;
        }
        
        .stButton, .stSelectbox, .stTextInput, .stHeader {
            position: relative;
            z-index: 1;
        }
        
        /* Card styling */
        .section-card {
            background: rgba(30, 30, 30, 0.85) !important;
            color: #E0E0E0 !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            border-left: 5px solid #47B5FF;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            z-index: 2;
            backdrop-filter: blur(5px);
        }
        
        .section-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5), 0 0 10px rgba(71, 181, 255, 0.3) !important;
        }

        .section-header {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #47B5FF !important;
            text-shadow: 0 0 10px rgba(71, 181, 255, 0.3);
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(90deg, #47B5FF, #1E88E5) !important;
            color: white !important;
            border: none !important;
            padding: 0.6rem 1.5rem !important;
            border-radius: 30px !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3), 0 0 10px rgba(71, 181, 255, 0.3) !important;
        }
        
        /* File uploader styling */
        [data-testid="stFileUploader"] {
            background: rgba(30, 30, 30, 0.8) !important;
            border-radius: 10px !important;
            padding: 5px !important;
            border: 1px solid #333 !important;
        }

        [data-testid="stFileUploader"] > div {
            color: #E0E0E0 !important;
        }
        
        .upload-container {
            background: rgba(30, 30, 30, 0.6);
            border: 2px dashed #47B5FF;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin-bottom: 15px;
            transition: all 0.3s;
        }
        
        .upload-container:hover {
            border-color: #0E86D4;
            box-shadow: 0 0 15px rgba(71, 181, 255, 0.2);
            background: rgba(46, 46, 46, 0.6);
        }
        
        .upload-icon {
            font-size: 2.5rem;
            color: #47B5FF;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(71, 181, 255, 0.5);
        }
        
        /* Status indicators */
        .success-indicator {
            color: #00C853;
            font-weight: bold;
            margin-top: 10px;
            display: flex;
            align-items: center;
        }
        
        .success-indicator::before {
            content: "✓";
            display: inline-block;
            background-color: #00C853;
            color: white;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            text-align: center;
            line-height: 20px;
            margin-right: 8px;
        }
        
        /* Slider styling */
        .stSlider [data-baseweb="slider"] {
            margin-top: 1rem !important;
        }
        
        .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
            background-color: #47B5FF !important;
            color: white !important;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: rgba(46, 46, 46, 0.7) !important;
            color: #E0E0E0 !important;
            border-radius: 5px !important;
        }
        
        .streamlit-expanderContent {
            background-color: rgba(30, 30, 30, 0.7) !important;
            color: #E0E0E0 !important;
            border-radius: 0 0 5px 5px !important;
        }
        
        /* Map container */
        .map-container {
            background-color: rgba(46, 46, 46, 0.8);
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            margin: 20px 0;
            border-left: 5px solid #47B5FF;
            backdrop-filter: blur(5px);
        }
        
        /* Stats cards */
        .stat-card {
            background-color: rgba(46, 46, 46, 0.7);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            margin-bottom: 15px;
            transition: transform 0.3s ease;
            backdrop-filter: blur(5px);
        }
        
        .stat-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3), 0 0 10px rgba(71, 181, 255, 0.2);
        }
        
        .stat-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #47B5FF;
            text-shadow: 0 0 5px rgba(71, 181, 255, 0.3);
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #B0B0B0;
            margin-top: 5px;
        }
        
        /* Main title styling */
        .main-title {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 0.3rem;
            text-shadow: 0 0 15px rgba(71, 181, 255, 0.5);
            position: relative;
            z-index: 2;
        }
        
        .main-subtitle {
            color: #B0B0B0;
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 2rem;
            position: relative;
            z-index: 2;
        }
        
        /* File upload container */
        .file-uploads {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin-bottom: 20px;
        }
        
        .upload-card {
            background: rgba(30, 30, 30, 0.7);
            border-radius: 10px;
            padding: 20px;
            width: 100%;
            max-width: 350px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            backdrop-filter: blur(5px);
        }
        
        .upload-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.3);
        }
        
        .upload-title {
            color: #47B5FF;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 15px;
            text-align: center;
        }
        
        /* Dataframe styling */
        .dataframe-container {
            background-color: rgba(30, 30, 30, 0.8);
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            border-left: 3px solid #47B5FF;
            backdrop-filter: blur(5px);
        }
        
        /* Download button */
        .download-button {
            background: linear-gradient(90deg, #47B5FF, #0E86D4) !important;
            color: white !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
            border: none !important;
            padding: 0.6rem 1.2rem !important;
            border-radius: 30px !important;
            font-weight: bold !important;
            margin-top: 1rem !important;
            transition: all 0.3s ease !important;
        }
        
        .download-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3), 0 0 10px rgba(71, 181, 255, 0.5) !important;
        }
        
        /* Make sure everything is on top of particles */
        .stAlert, .stCheckbox, div[data-testid="stVerticalBlock"] {
            position: relative;
            z-index: 2;
        }
        
        /* Custom selectbox styling */
        .stSelectbox > div > div {
            background-color: rgba(30, 30, 30, 0.7) !important;
            border-radius: 8px !important;
            border-color: #333 !important;
        }
        
        .stSelectbox > div > div:hover {
            border-color: #47B5FF !important;
        }
        
        /* Custom number input styling */
        [data-testid="stNumberInput"] > div {
            background-color: rgba(30, 30, 30, 0.7) !important;
            border-radius: 8px !important;
            border-color: #333 !important;
        }
        
        [data-testid="stNumberInput"] > div:hover {
            border-color: #47B5FF !important;
        }
        
        /* Checkbox styling */
        .stCheckbox > div > div > div {
            background-color: rgba(30, 30, 30, 0.7) !important;
        }
        
        .stCheckbox > div > div > div[data-checked="true"] {
            background-color: #47B5FF !important;
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            padding: 1rem;
            color: #6c757d;
            font-size: 0.8rem;
            margin-top: 2rem;
            background-color: rgba(30, 30, 30, 0.5);
            border-radius: 10px;
            backdrop-filter: blur(5px);
            position: relative;
            z-index: 2;
        }
    </style>
""", unsafe_allow_html=True)

# Display title with special styling
st.markdown("""
    <h1 class="main-title">🏥 Health Facility Map Generator</h1>
    <p class="main-subtitle">Create beautiful geospatial visualizations of health facilities</p>
""", unsafe_allow_html=True)

# Welcome animation (only on first load)
if 'first_load' not in st.session_state:
    st.session_state.first_load = True

if st.session_state.first_load:
    st.balloons()
    st.session_state.first_load = False

# File Upload Card
st.markdown("""
    <div class="section-card">
        <div class="section-header">📁 Upload Required Files</div>
""", unsafe_allow_html=True)

# Use a more visual layout for the file uploads
st.markdown("""
    <div class="file-uploads">
        <div class="upload-card">
            <div class="upload-title">Shapefile Components</div>
            <div class="upload-icon" style="text-align: center;">🗺️</div>
""", unsafe_allow_html=True)

# Shapefile uploads
shp_file = st.file_uploader("Upload .shp file", type=["shp"], key="shp", label_visibility="collapsed")
shx_file = st.file_uploader("Upload .shx file", type=["shx"], key="shx", label_visibility="collapsed")
dbf_file = st.file_uploader("Upload .dbf file", type=["dbf"], key="dbf", label_visibility="collapsed")

if all([shp_file, shx_file, dbf_file]):
    st.markdown('<div class="success-indicator">All boundary files uploaded</div>', unsafe_allow_html=True)

st.markdown("""
        </div>
        <div class="upload-card">
            <div class="upload-title">Health Facility Data</div>
            <div class="upload-icon" style="text-align: center;">📊</div>
""", unsafe_allow_html=True)

# Facility data upload
facility_file = st.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"], key="facility", label_visibility="collapsed")

if facility_file:
    st.markdown('<div class="success-indicator">Facility data uploaded</div>', unsafe_allow_html=True)

st.markdown("""
        </div>
    </div>
""", unsafe_allow_html=True)

# Configuration section
if all([shp_file, shx_file, dbf_file, facility_file]):
    try:
        # Create a temp directory for files
        temp_dir = tempfile.mkdtemp()
        shp_path = os.path.join(temp_dir, "temp.shp")
        shx_path = os.path.join(temp_dir, "temp.shx")
        dbf_path = os.path.join(temp_dir, "temp.dbf")
        
        # Save uploaded files to temp directory
        with open(shp_path, "wb") as f:
            f.write(shp_file.read())
        with open(shx_path, "wb") as f:
            f.write(shx_file.read())
        with open(dbf_path, "wb") as f:
            f.write(dbf_file.read())
        
        # Read the shapefile
        shapefile = gpd.read_file(shp_path)
        
        # Read facility data
        coordinates_data = pd.read_excel(facility_file)
        
        # Display data preview in an expander
        with st.expander("📋 Data Preview"):
            st.dataframe(coordinates_data.head(), use_container_width=True)
            st.info(f"Total records: {len(coordinates_data)}")
        
        # Configuration options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<p style="color: #47B5FF; font-weight: bold; margin-bottom: 0.5rem;">Coordinate Columns</p>', unsafe_allow_html=True)
            
            # Column selection
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
            
            # Optional category column
            category_options = ["None"] + list(coordinates_data.columns)
            category_col = st.selectbox(
                "Category Column (Optional)",
                category_options,
                index=category_options.index("type") if "type" in category_options else 0
            )
        
        with col2:
            st.markdown('<p style="color: #47B5FF; font-weight: bold; margin-bottom: 0.5rem;">Map Style</p>', unsafe_allow_html=True)
            
            # Map title
            map_title = st.text_input("Map Title", "Health Facility Distribution")
            
            # Color options
            map_themes = {
                "Blue Night": {"bg": "#1A1A2E", "point": "#47B5FF"},
                "Deep Ocean": {"bg": "#16213E", "point": "#00C2FF"},
                "Emerald": {"bg": "#1A2E22", "point": "#00C853"},
                "Purple Haze": {"bg": "#1A1A2E", "point": "#BB86FC"}
            }
            
            # Theme selection
            map_theme = st.selectbox("Color Theme", list(map_themes.keys()))
            bg_color = map_themes[map_theme]["bg"]
            point_color = map_themes[map_theme]["point"]
        
        with col3:
            st.markdown('<p style="color: #47B5FF; font-weight: bold; margin-bottom: 0.5rem;">Visual Settings</p>', unsafe_allow_html=True)
            
            # Visual settings
            point_size = st.slider("Point Size", 10, 200, 50)
            point_alpha = st.slider("Point Transparency", 0.1, 1.0, 0.7)
            
            # Show borders checkbox
            show_borders = st.checkbox("Show Region Borders", value=True)
            border_width = st.slider("Border Width", 0.1, 2.0, 0.5) if show_borders else 0.5
        
        # Generate map button
        generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])
        with generate_col2:
            generate_button = st.button("Generate Map", use_container_width=True)
        
    except Exception as e:
        st.error(f"Error configuring map: {str(e)}")
        st.info("Please check that your files are in the correct format and try again.")
else:
    st.info("Please upload all required files to configure your map.")

st.markdown("""</div>""", unsafe_allow_html=True)

# Results section
if all([shp_file, shx_file, dbf_file, facility_file]) and ('generate_button' in locals() and generate_button):
    st.markdown("""
        <div class="section-card">
            <div class="section-header">🗺️ Generated Map</div>
    """, unsafe_allow_html=True)
    
    try:
        # Process data
        # Remove missing coordinates
        coordinates_data = coordinates_data.dropna(subset=[longitude_col, latitude_col])
        
        # Filter invalid coordinates
        coordinates_data = coordinates_data[
            (coordinates_data[longitude_col].between(-180, 180)) &
            (coordinates_data[latitude_col].between(-90, 90))
        ]
        
        if len(coordinates_data) == 0:
            st.error("No valid coordinates found in the data after filtering.")
            st.info("Please check your coordinate columns and try again.")
            st.markdown("""</div>""", unsafe_allow_html=True)
            st.stop()
        
        # Convert to GeoDataFrame
        geometry = [Point(xy) for xy in zip(coordinates_data[longitude_col], coordinates_data[latitude_col])]
        coordinates_gdf = gpd.GeoDataFrame(coordinates_data, geometry=geometry, crs="EPSG:4326")
        
        # Ensure consistent CRS
        if shapefile.crs is None:
            shapefile = shapefile.set_crs(epsg=4326)
        else:
            shapefile = shapefile.to_crs(epsg=4326)
        
        # Create figure with dark theme
        fig, ax = plt.subplots(figsize=(15, 10), facecolor=bg_color)
        ax.set_facecolor(bg_color)
        
        # Plot shapefile
        border_color = '#FFFFFF'
        shapefile.plot(
            ax=ax,
            color=bg_color,
            edgecolor=border_color if show_borders else bg_color,
            linewidth=border_width if show_borders else 0
        )
        
        # Calculate aspect ratio
        bounds = shapefile.total_bounds
        mid_y = np.mean([bounds[1], bounds[3]])
        aspect = 1.0
        
        if -90 < mid_y < 90:
            try:
                aspect = 1 / np.cos(np.radians(mid_y))
                if not np.isfinite(aspect) or aspect <= 0:
                    aspect = 1.0
            except:
                aspect = 1.0
        
        ax.set_aspect(aspect)
        
        # Plot points - with categories if available
        if category_col != "None" and category_col in coordinates_data.columns:
            # Get unique categories
            categories = coordinates_data[category_col].dropna().unique()
            
            # Generate a color palette for categories
            if len(categories) <= 10:
                # Predefined colors that work well in dark mode
                colors = ['#FF9671', '#FFC75F', '#F9F871', '#00C853', '#BB86FC', 
                          '#03DAC6', '#FF5252', '#82B1FF', '#EA80FC', '#FFFFFF'][:len(categories)]
            else:
                # Generate colors from colormap
                cmap = plt.cm.get_cmap('tab20', len(categories))
                colors = [plt.cm.colors.rgb2hex(cmap(i)) for i in range(len(categories))]
            
            # Plot each category with different color
            for i, cat in enumerate(categories):
                cat_data = coordinates_gdf[coordinates_gdf[category_col] == cat]
                cat_data.plot(
                    ax=ax,
                    color=colors[i],
                    markersize=point_size,
                    alpha=point_alpha,
                    label=cat
                )
            
            # Add legend with styling
            legend = ax.legend(
                title=category_col.title(),
                loc='upper right',
                frameon=True,
                facecolor=bg_color,
                edgecolor='#333333'
            )
            plt.setp(legend.get_title(), color='white')
            plt.setp(legend.get_texts(), color='white')
        else:
            # Plot all points with same color
            coordinates_gdf.plot(
                ax=ax,
                color=point_color,
                markersize=point_size,
                alpha=point_alpha
            )
        
        # Style the map
        plt.title(map_title, fontsize=20, pad=20, color='white', fontweight='bold')
        plt.axis('off')
        
        # Add statistics box with styling
        stats_box = {
            'facecolor': 'black',
            'alpha': 0.6,
            'pad': 1.0,
            'boxstyle': 'round,pad=0.6',
            'edgecolor': '#47B5FF'
        }
        
        # Statistics text
        stats_text = (
            f"Total Facilities: {len(coordinates_data)}\n"
            f"Longitude Range: {coordinates_data[longitude_col].min():.2f}° to {coordinates_data[longitude_col].max():.2f}°\n"
            f"Latitude Range: {coordinates_data[latitude_col].min():.2f}° to {coordinates_data[latitude_col].max():.2f}°"
        )
        
        # Add text with glow effect
        plt.figtext(
            0.02, 0.02, 
            stats_text, 
            fontsize=10, 
            color='white',
            bbox=stats_box
        )
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        plt.figtext(
            0.98, 0.02, 
            f"Generated: {timestamp}", 
            fontsize=8, 
            color='white', 
            ha='right',
            bbox={
                'facecolor': 'black',
                'alpha': 0.6,
                'pad': 0.5,
                'boxstyle': 'round',
                'edgecolor': '#47B5FF'
            }
        )
        
        # Display the map in a container
        st.markdown('<div class="map-container">', unsafe_allow_html=True)
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display statistics in cards
        st.markdown('<h3 style="color: #47B5FF; margin-top: 1.5rem; text-shadow: 0 0 10px rgba(71, 181, 255, 0.3);">Statistics & Distribution</h3>', unsafe_allow_html=True)
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        with stat_col1:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{len(coordinates_data)}</div>
                    <div class="stat-label">Total Facilities</div>
                </div>
            """, unsafe_allow_html=True)
        
        with stat_col2:
            # Calculate area (approximate)
            area = (bounds[2] - bounds[0]) * (bounds[3] - bounds[1])
            area_km2 = area * 111 * 111 * np.cos(np.radians(mid_y))  # Approx conversion to km²
            
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{area_km2:.1f} km²</div>
                    <div class="stat-label">Coverage Area</div>
                </div>
            """, unsafe_allow_html=True)
        
        with stat_col3:
            # Calculate density
            density = len(coordinates_data) / area_km2 if area_km2 > 0 else 0
            
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{density:.4f}</div>
                    <div class="stat-label">Facilities / km²</div>
                </div>
            """, unsafe_allow_html=True)
        
        # If category column was selected, show distribution chart
        if category_col != "None" and category_col in coordinates_data.columns:
            st.markdown('<h3 style="color: #47B5FF; margin-top: 1.5rem; text-shadow: 0 0 10px rgba(71, 181, 255, 0.3);">Category Distribution</h3>', unsafe_allow_html=True)
            
            # Calculate category counts
            cat_counts = coordinates_data[category_col].value_counts()
            
            # Create a horizontal bar chart
            fig2, ax2 = plt.subplots(figsize=(10, max(4, min(10, len(cat_counts) * 0.5))), facecolor=bg_color)
            ax2.set_facecolor(bg_color)
            
            # Get same colors as in map
            if len(cat_counts) <= 10:
                colors = ['#FF9671', '#FFC75F', '#F9F871', '#00C853', '#BB86FC', 
                          '#03DAC6', '#FF5252', '#82B1FF', '#EA80FC', '#FFFFFF'][:len(cat_counts)]
            else:
                cmap = plt.cm.get_cmap('tab20', len(cat_counts))
                colors = [plt.cm.colors.rgb2hex(cmap(i)) for i in range(len(cat_counts))]
            
            # Plot horizontal bars
            y_pos = range(len(cat_counts))
            bars = ax2.barh(y_pos, cat_counts.values, color=colors)
            
            # Add labels and values
            ax2.set_yticks(y_pos)
            ax2.set_yticklabels(cat_counts.index, color='white')
            
            # Add value labels to the right of each bar
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax2.text(width + (max(cat_counts.values) * 0.02), 
                         bar.get_y() + bar.get_height()/2, 
                         str(cat_counts.values[i]), 
                         ha='left', va='center', color='white', fontweight='bold')
            
            # Style the chart
            ax2.set_title(f"Distribution by {category_col}", color='white', fontsize=14, pad=20)
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.spines['bottom'].set_color('#555')
            ax2.spines['left'].set_color('#555')
            ax2.tick_params(axis='x', colors='white')
            ax2.xaxis.label.set_color('white')
            
            # Display the chart
            st.markdown('<div class="map-container">', unsafe_allow_html=True)
            st.pyplot(fig2)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Save map for download
        output_path_png = os.path.join(temp_dir, "health_facility_map.png")
        plt.figure(1)  # Make sure we're saving the map figure
        plt.savefig(output_path_png, dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor=bg_color)
        
        # Download options
        st.markdown('<h3 style="color: #47B5FF; margin-top: 1.5rem; text-shadow: 0 0 10px rgba(71, 181, 255, 0.3);">Download Options</h3>', unsafe_allow_html=True)
        
        download_col1, download_col2 = st.columns(2)
        
        with download_col1:
            # Download map
            with open(output_path_png, "rb") as file:
                st.download_button(
                    label="Download Map (PNG)",
                    data=file,
                    file_name="health_facility_map.png",
                    mime="image/png",
                    use_container_width=True
                )
        
        with download_col2:
            # Download processed data
            csv = coordinates_data.to_csv(index=False)
            st.download_button(
                label="Download Processed Data (CSV)",
                data=csv,
                file_name="processed_coordinates.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    except Exception as e:
        st.error(f"An error occurred during map generation: {str(e)}")
        st.info("Please check your data and try again.")
    
    st.markdown("""</div>""", unsafe_allow_html=True)

# Add footer
st.markdown("""
    <div class="footer">
        <p>Health Facility Map Generator • Built with Streamlit</p>
    </div>
""", unsafe_allow_html=True)

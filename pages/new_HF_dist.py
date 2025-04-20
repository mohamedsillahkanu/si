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
    initial_sidebar_state="expanded"
)

# Particles.js HTML configuration
particles_js = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Particles.js</title>
    <style>
        #particles-js {
            position: absolute;
            width: 100%;
            height: 100%;
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
                "number": {"value": 80, "density": {"enable": true, "value_area": 800}},
                "color": {"value": "#47B5FF"},
                "shape": {"type": "circle"},
                "opacity": {"value": 0.5, "random": false},
                "size": {"value": 2, "random": true},
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": "#47B5FF",
                    "opacity": 0.22,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": 0.3,
                    "direction": "none",
                    "random": false,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": true
                }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": {"enable": true, "mode": "grab"},
                    "onclick": {"enable": true, "mode": "repulse"},
                    "resize": true
                }
            },
            "retina_detect": true
        });
    </script>
</body>
</html>
"""

# Inject particles.js
components.html(particles_js, height=1000)

# Styling to match the dark theme with glowing blue accents
st.markdown("""
    <style>
        /* Base styling */
        .stApp {
            background-color: #0E1117 !important;
            color: #E0E0E0 !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #0E1117 !important;
            border-right: 1px solid #2E2E2E;
            z-index: 2;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdown"],
        [data-testid="stSidebar"] .stSelectbox,
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] div {
            color: white !important;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: white !important;
            font-weight: bold;
        }

        [data-testid="stSidebar"] button {
            color: white !important;
            border-color: #47B5FF !important;
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
            background: #1E1E1E !important;
            color: #E0E0E0 !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            border-left: 5px solid #47B5FF;
            transition: transform 0.3s ease;
        }
        
        .section-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.5);
            background: #2E2E2E !important;
        }

        .section-header {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #47B5FF !important;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #47B5FF !important;
            color: white !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            border-radius: 5px !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            background-color: #0E86D4 !important;
            box-shadow: 0 0 10px #47B5FF !important;
        }
        
        /* File uploader styling */
        .upload-container {
            background: #1E1E1E;
            border: 2px dashed #47B5FF;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin-bottom: 15px;
            transition: all 0.3s;
        }
        
        .upload-container:hover {
            border-color: #0E86D4;
            background: #2E2E2E;
        }
        
        .upload-icon {
            font-size: 2rem;
            color: #47B5FF;
            margin-bottom: 10px;
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
            background-color: #2E2E2E !important;
            color: #E0E0E0 !important;
            border-radius: 5px !important;
        }
        
        .streamlit-expanderContent {
            background-color: #1E1E1E !important;
            color: #E0E0E0 !important;
            border-radius: 0 0 5px 5px !important;
        }
        
        /* Map container */
        .map-container {
            background-color: #2E2E2E;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            margin: 20px 0;
            border-left: 5px solid #47B5FF;
        }
        
        /* Stats cards */
        .stat-card {
            background-color: #2E2E2E;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 15px;
        }
        
        .stat-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #47B5FF;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #B0B0B0;
        }
        
        /* Progress steps */
        .progress-steps {
            display: flex;
            justify-content: space-between;
            margin: 30px 0;
            position: relative;
        }
        
        .progress-steps::before {
            content: "";
            position: absolute;
            top: 15px;
            left: 0;
            right: 0;
            height: 2px;
            background-color: #333;
            z-index: -1;
        }
        
        .step {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .step-circle {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background-color: #333;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 10px;
            color: white;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .step-circle.active {
            background-color: #47B5FF;
            box-shadow: 0 0 10px #47B5FF;
        }
        
        .step-label {
            font-size: 0.9rem;
            color: #B0B0B0;
        }
        
        .step-label.active {
            color: #47B5FF;
            font-weight: bold;
        }
        
        /* Dataframe styling */
        .dataframe-container {
            background-color: #2E2E2E;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            border-left: 3px solid #47B5FF;
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
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3), 0 0 10px #47B5FF !important;
        }
    </style>
""", unsafe_allow_html=True)

# Display title with special styling
st.markdown("""
    <h1 style="color: #47B5FF !important; text-align: center; font-size: 2.5rem; margin-bottom: 0.5rem; text-shadow: 0 0 10px rgba(71, 181, 255, 0.5);">
        🏥 Health Facility Map Generator
    </h1>
    <p style="text-align: center; color: #B0B0B0; margin-bottom: 2rem;">
        Generate beautiful geospatial visualizations of health facilities
    </p>
""", unsafe_allow_html=True)

# Welcome animation (only on first load)
if 'first_load' not in st.session_state:
    st.session_state.first_load = True

if st.session_state.first_load:
    st.balloons()
    st.session_state.first_load = False

# Create progress steps
current_step = 1  # Set this based on user progress
st.markdown(f"""
    <div class="progress-steps">
        <div class="step">
            <div class="step-circle {'active' if current_step >= 1 else ''}">1</div>
            <div class="step-label {'active' if current_step >= 1 else ''}">Upload Files</div>
        </div>
        <div class="step">
            <div class="step-circle {'active' if current_step >= 2 else ''}">2</div>
            <div class="step-label {'active' if current_step >= 2 else ''}">Configure Map</div>
        </div>
        <div class="step">
            <div class="step-circle {'active' if current_step >= 3 else ''}">3</div>
            <div class="step-label {'active' if current_step >= 3 else ''}">Generate & Export</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.markdown("""
        <h2 style="color: #47B5FF !important; margin-bottom: 1rem;">Navigation</h2>
    """, unsafe_allow_html=True)
    
    # Navigation options
    page = st.radio("", ["Map Generator", "Help & Instructions", "About"], label_visibility="collapsed")
    
    st.markdown("<hr style='margin: 1.5rem 0; border-color: #333;'>", unsafe_allow_html=True)
    
    st.markdown("""
        <h3 style="color: #47B5FF !important; margin-bottom: 1rem;">Settings</h3>
    """, unsafe_allow_html=True)
    
    # Theme selector
    theme = st.selectbox("Color Theme", ["Blue (Default)", "Green", "Purple", "Red"])
    
    # Theme color mapping
    theme_colors = {
        "Blue (Default)": "#47B5FF",
        "Green": "#00C853",
        "Purple": "#9C27B0",
        "Red": "#F44336"
    }
    
    # Map style
    map_style = st.selectbox("Map Style", ["Dark Mode", "Light Mode", "Satellite"])
    
    st.markdown("<hr style='margin: 1.5rem 0; border-color: #333;'>", unsafe_allow_html=True)
    
    # Help section
    with st.expander("Frequently Asked Questions"):
        st.markdown("""
            **Q: What files do I need to upload?**
            
            A: You need to upload 3 shapefile components (.shp, .shx, .dbf) and a health facility Excel file with coordinates.
            
            **Q: What format should my data be in?**
            
            A: Your Excel file should have columns for longitude and latitude in decimal degrees.
            
            **Q: How can I customize my map?**
            
            A: You can adjust colors, point size, transparency, and add a title to your map.
        """)

# Main content based on selected page
if page == "Map Generator":
    # File Upload Card
    st.markdown("""
        <div class="section-card">
            <div class="section-header">📁 Upload Required Files</div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="upload-container">
                <div class="upload-icon">🗺️</div>
                <p>Upload Shapefile Components</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Shapefile uploads
        shp_file = st.file_uploader("Upload .shp file", type=["shp"], key="shp", label_visibility="collapsed")
        shx_file = st.file_uploader("Upload .shx file", type=["shx"], key="shx", label_visibility="collapsed")
        dbf_file = st.file_uploader("Upload .dbf file", type=["dbf"], key="dbf", label_visibility="collapsed")
        
        if all([shp_file, shx_file, dbf_file]):
            st.markdown('<div class="success-indicator">All boundary files uploaded successfully</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="upload-container">
                <div class="upload-icon">📊</div>
                <p>Upload Health Facility Data</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Facility data upload
        facility_file = st.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"], key="facility", label_visibility="collapsed")
        
        if facility_file:
            st.markdown('<div class="success-indicator">Facility data uploaded successfully</div>', unsafe_allow_html=True)
    
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Configuration Card
    st.markdown("""
        <div class="section-card">
            <div class="section-header">⚙️ Configure Your Map</div>
    """, unsafe_allow_html=True)
    
    # Check if files are uploaded
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
                st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                st.dataframe(coordinates_data.head(), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
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
                background_colors = {
                    "Dark": "#1A1A2E",
                    "Medium": "#16213E",
                    "Light": "#0F3460"
                }
                
                # Color selection
                background_color = st.selectbox("Background Color", list(background_colors.keys()))
                
                # Get actual color value
                bg_color_value = background_colors[background_color]
                
                # Point color options with theme support
                point_color = theme_colors[theme]
            
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
    
    # Results Card - only show if generation was requested
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
            
            # Create figure
            fig, ax = plt.subplots(figsize=(15, 10), facecolor=bg_color_value)
            ax.set_facecolor(bg_color_value)
            
            # Plot shapefile
            border_color = '#FFFFFF' if bg_color_value in ['#1A1A2E', '#16213E', '#0F3460'] else '#333333'
            shapefile.plot(
                ax=ax,
                color=bg_color_value,
                edgecolor=border_color if show_borders else bg_color_value,
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
                
                # Generate a colormap
                if len(categories) <= 10:
                    # Predefined colors that work well in dark mode
                    colors = ['#FF9671', '#FFC75F', '#F9F871', '#00C853', '#9C27B0', 
                              '#03DAC6', '#FF5252', '#B388FF', '#82B1FF', '#EA80FC'][:len(categories)]
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
                
                # Add legend
                legend = ax.legend(
                    title=category_col.title(),
                    loc='upper right',
                    frameon=True,
                    facecolor=bg_color_value,
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
            
            # Add statistics text
            stats_text = (
                f"Total Facilities: {len(coordinates_data)}\n"
                f"Longitude Range: {coordinates_data[longitude_col].min():.2f}° to {coordinates_data[longitude_col].max():.2f}°\n"
                f"Latitude Range: {coordinates_data[latitude_col].min():.2f}° to {coordinates_data[latitude_col].max():.2f}°"
            )
            
            # Add text with background box
            plt.figtext(
                0.02, 0.02, 
                stats_text, 
                fontsize=9, 
                color='white',
                bbox=dict(
                    facecolor='#2E2E2E',
                    alpha=0.8,
                    boxstyle='round,pad=0.5',
                    edgecolor='#47B5FF'
                )
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
                bbox=dict(
                    facecolor='#2E2E2E',
                    alpha=0.8,
                    boxstyle='round,pad=0.3',
                    edgecolor='#47B5FF'
                )
            )
            
            # Display the map in a container
            st.markdown('<div class="map-container">', unsafe_allow_html=True)
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display statistics in cards
            st.markdown('<h3 style="color: #47B5FF; margin-top: 1.5rem;">Statistics & Distribution</h3>', unsafe_allow_html=True)
            
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
                st.markdown('<h3 style="color: #47B5FF; margin-top: 1.5rem;">Category Distribution</h3>', unsafe_allow_html=True)
                
                # Calculate category counts
                cat_counts = coordinates_data[category_col].value_counts()
                
                # Create a horizontal bar chart
                fig2, ax2 = plt.subplots(figsize=(10, max(4, min(10, len(cat_counts) * 0.5))), facecolor=bg_color_value)
                ax2.set_facecolor(bg_color_value)
                
                # Get same colors as in map
                if len(cat_counts) <= 10:
                    colors = ['#FF9671', '#FFC75F', '#F9F871', '#00C853', '#9C27B0', 
                              '#03DAC6', '#FF5252', '#B388FF', '#82B1FF', '#EA80FC'][:len(cat_counts)]
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
            plt.savefig(output_path_png, dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor=bg_color_value)
            
            # Download options
            st.markdown('<h3 style="color: #47B5FF; margin-top: 1.5rem;">Download Options</h3>', unsafe_allow_html=True)
            
            download_col1, download_col2 = st.columns(2)
            
            with download_col1:
                # Download map
                with open(output_path_png, "rb") as file:
                    btn = st.download_button(
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

elif page == "Help & Instructions":
    st.markdown("""
        <div class="section-card">
            <div class="section-header">📘 How to Use This Tool</div>
            <p>The Health Facility Map Generator allows you to create beautiful, interactive maps showing the geographic distribution of health facilities. Follow these steps to generate your map:</p>
            
            <h3 style="color: #47B5FF; margin-top: 1.5rem;">Step 1: Prepare Your Files</h3>
            <p>You'll need two types of files:</p>
            <ul>
                <li><strong>Shapefile Components</strong>: These define the geographic boundaries. You need three files with the same name but different extensions: .shp, .shx, and .dbf.</li>
                <li><strong>Health Facility Data</strong>: An Excel (.xlsx) file containing your facility information with columns for longitude and latitude.</li>
            </ul>
            
            <h3 style="color: #47B5FF; margin-top: 1.5rem;">Step 2: Upload Your Files</h3>
            <p>Upload all required files in the Map Generator section. Make sure all shapefile components are from the same set.</p>
            
            <h3 style="color: #47B5FF; margin-top: 1.5rem;">Step 3: Configure Your Map</h3>
            <p>After uploading your files, you can customize your map:</p>
            <ul>
                <li><strong>Coordinate Columns</strong>: Select which columns in your Excel file contain longitude and latitude data.</li>
                <li><strong>Map Style</strong>: Choose colors and add a title for your map.</li>
                <li><strong>Visual Settings</strong>: Adjust point size and transparency to best display your data.</li>
            </ul>
            
            <h3 style="color: #47B5FF; margin-top: 1.5rem;">Step 4: Generate & Download</h3>
            <p>Click the "Generate Map" button to create your visualization. You can then download:</p>
            <ul>
                <li>The map as a high-resolution PNG image</li>
                <li>Your processed coordinate data as a CSV file</li>
            </ul>
        </div>
        
        <div class="section-card">
            <div class="section-header">💡 Tips for Better Maps</div>
            
            <h3 style="color: #47B5FF; margin-top: 1rem;">Data Preparation</h3>
            <ul>
                <li>Clean your data before uploading, removing or fixing invalid coordinates</li>
                <li>Include a category column (e.g., facility type) for color-coded visualization</li>
                <li>Ensure coordinates are in decimal degrees format (e.g., 9.0479, 7.4951)</li>
                <li>Check that your coordinates match the geographic region in your shapefile</li>
            </ul>
            
            <h3 style="color: #47B5FF; margin-top: 1rem;">Troubleshooting Common Issues</h3>
            <ul>
                <li><strong>Map doesn't display</strong>: Confirm your coordinate columns are correctly selected</li>
                <li><strong>Points appear in wrong locations</strong>: Check for coordinate system mismatches</li>
                <li><strong>Upload errors</strong>: Ensure all shapefile components (.shp, .shx, .dbf) are from the same set</li>
                <li><strong>No data showing</strong>: Verify your Excel file has the expected column names and data formats</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

else:  # About page
    st.markdown("""
        <div class="section-card">
            <div class="section-header">ℹ️ About This Tool</div>
            <p>The Health Facility Map Generator is designed to help healthcare professionals, researchers, and planners visualize the geographic distribution of health facilities. This tool simplifies the process of creating professional-quality maps without requiring GIS expertise.</p>
            
            <h3 style="color: #47B5FF; margin-top: 1.5rem;">Features</h3>
            <ul>
                <li>Fast processing of geospatial data</li>
                <li>Support for categorized visualization (e.g., by facility type)</li>
                <li>Customizable map styling and appearance</li>
                <li>Statistical analysis of facility distribution</li>
                <li>High-resolution export options</li>
                <li>User-friendly interface with minimal learning curve</li>
            </ul>
            
            <h3 style="color: #47B5FF; margin-top: 1.5rem;">Use Cases</h3>
            <ul>
                <li><strong>Public Health Planning</strong>: Analyze healthcare coverage and identify gaps in service</li>
                <li><strong>Resource Allocation</strong>: Make data-driven decisions about where to invest in new facilities</li>
                <li><strong>Program Monitoring</strong>: Track the expansion of health services over time</li>
                <li><strong>Reporting</strong>: Create professional visualizations for presentations and publications</li>
                <li><strong>Emergency Response</strong>: Quickly assess available health resources in affected areas</li>
            </ul>
        </div>
        
        <div class="section-card">
            <div class="section-header">🔄 Version History</div>
            <p>Current Version: 2.0</p>
            
            <h3 style="color: #47B5FF; margin-top: 1rem;">What's New</h3>
            <ul>
                <li>Dark mode interface with interactive particle background</li>
                <li>Enhanced data visualization options</li>
                <li>Improved statistical summaries</li>
                <li>Faster processing of large datasets</li>
                <li>Multiple theme options</li>
            </ul>
            
            <div style="margin-top: 2rem; text-align: center; color: #B0B0B0;">
                <p>Developed for health facility mapping and analysis</p>
                <p style="font-size: 0.8rem;">© 2025 Health GIS Tools</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Add footer
st.markdown("""
    <div style="margin-top: 4rem; padding: 1.5rem; background-color: #1E1E1E; border-radius: 10px; text-align: center;">
        <p style="color: #B0B0B0; font-size: 0.8rem;">Health Facility Map Generator • Built with Streamlit</p>
        <p style="color: #B0B0B0; font-size: 0.8rem;">For support and feedback: support@healthfacilitymapper.org</p>
    </div>
""", unsafe_allow_html=True)

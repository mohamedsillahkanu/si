import streamlit as st

# Apply sky blue background using custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color:#ffffb3;
    }
    </style>
    """, unsafe_allow_html=True
)

# Custom CSS for sidebar background and text color
sidebar_bg_css = """
<style>
[data-testid="stSidebar"] {
    background-color: #8dd3c7; /* Sky blue background */
    color: #000000; /* Sidebar text color */
}
</style>
"""

# Apply the sidebar CSS
st.markdown(sidebar_bg_css, unsafe_allow_html=True)

# Title of the app
st.title("Data Management Options")

# Dropdown menu for data management options
data_option = st.sidebar.selectbox(
    "Choose a data management option:",
    (
        'None',
        'Shapefiles',
        'Health Facilities',
        'Routine case data from DHIS2',
        'DHS data',
        'Climate data',
        'LMIS data',
        'Modeled data',
        'Population data'
    )
)

# Dropdown menu for content options
content_option = st.selectbox(
    "Choose what to view:",
    (
        'None',
        'See R Code',
        'Explanation of R Code',
        'See Python Code',
        'Explanation of Python Code',
        'Sample Output'
    )
)

# Sample R and Python code and images for different options
r_code_shapefiles = """
# Install libraries
install.packages("sf")      # For handling shapefiles
install.packages("ggplot2") # For visualization

# Load necessary libraries
library(sf)       # For spatial data handling
library(ggplot2)  # For visualization

### A.1.1 Import shapefiles

# Read a shapefile from a local directory
shapefile_path <- "/content/Chiefdom 2021.shp"
shapefile_data <- st_read(shapefile_path)

# Preview the shapefile data
print(head(shapefile_data))  # Shows the first few rows of the shapefile

### A.1.4 Visualizing shapefiles and making basic maps

# Plot the shapefile 
ggplot(data = shapefile_data) +
  geom_sf() +  # Plot the shapefile geometries
  labs(title = "Basic Shapefile Map") +
  theme_minimal() +
  theme(panel.grid = element_blank(),     # Remove grid lines
        axis.title = element_blank(),     # Remove axis titles
        axis.text = element_blank(),      # Remove axis text
        axis.ticks = element_blank())     # Remove axis ticks
"""

python_code_shapefiles = """
!pip install geopandas matplotlib

import geopandas as gpd
import matplotlib.pyplot as plt

# Path to the shapefile (adjust the path as needed)
shapefile_path = '/content/Chiefdom 2021.shp'

# Read the shapefile
shapefile_data = gpd.read_file(shapefile_path)

# Preview the shapefile data
print(shapefile_data.head())  # Shows the first few rows of the shapefile

# Plot the shapefile
fig, ax = plt.subplots(figsize=(10, 10))
shapefile_data.plot(ax=ax, color='lightblue', edgecolor='black')

# Customize the plot to remove grid lines and axis labels
ax.set_title('Basic Shapefile Map', fontsize=16)
ax.grid(False)  # Remove grid lines
ax.set_axis_off()  # Remove axis title, text, and ticks

# Show the plot
plt.show()
"""

r_code_health_facilities = """
# Example R code for Health Facilities
# Load necessary libraries
library(ggplot2)

# Sample data frame
df <- data.frame(
    Facility = c('Facility A', 'Facility B', 'Facility C'),
    Cases = c(50, 100, 75)
)

# Plot the data
ggplot(df, aes(x = Facility, y = Cases, fill = Facility)) +
    geom_bar(stat = 'identity') +
    labs(title = 'Health Facilities Cases') +
    theme_minimal()
"""

python_code_health_facilities = """
import pandas as pd
import matplotlib.pyplot as plt

# Sample data frame
df = pd.DataFrame({
    'Facility': ['Facility A', 'Facility B', 'Facility C'],
    'Cases': [50, 100, 75]
})

# Plot the data
plt.figure(figsize=(8, 6))
plt.bar(df['Facility'], df['Cases'], color='skyblue')
plt.title('Health Facilities Cases')
plt.xlabel('Facility')
plt.ylabel('Cases')
plt.show()
"""

# Explanations
explanation_r_shapefiles = """
The R code demonstrates how to import and visualize shapefiles using the `sf` and `ggplot2` libraries.
1. `st_read()` reads the shapefile data.
2. `ggplot(data = shapefile_data) + geom_sf()` creates a plot of the shapefile geometries.
3. `theme_minimal() + theme()` customizes the plot by removing grid lines and axis details.
"""

explanation_python_shapefiles = """
The Python code demonstrates how to import and visualize shapefiles using `geopandas` and `matplotlib`.
1. `gpd.read_file()` reads the shapefile data.
2. `shapefile_data.plot()` creates a plot of the shapefile geometries.
3. `ax.grid(False)` and `ax.set_axis_off()` customize the plot by removing grid lines and axis details.
"""

explanation_r_health_facilities = """
The R code demonstrates how to create a bar plot for Health Facilities data using the `ggplot2` library.
1. `ggplot(df, aes(x = Facility, y = Cases, fill = Facility))` initializes the plot with data.
2. `geom_bar(stat = 'identity')` adds bars to the plot.
3. `labs()` adds labels and titles.
"""

explanation_python_health_facilities = """
The Python code demonstrates how to create a bar plot for Health Facilities data using `matplotlib`.
1. `plt.bar(df['Facility'], df['Cases'], color='skyblue')` creates the bar plot.
2. `plt.title()`, `plt.xlabel()`, and `plt.ylabel()` add labels and title.
"""

# Sample images for different options
sample_output_shapefiles = "https://github.com/mohamedsillahkanu/si/blob/c6b5747886fb15b511fe99ac90afdbad64b0628f/MAP_R.png?raw=true"

sample_output_health_facilities = "https://example.com/health_facilities_image.png"  # Replace with actual image URL

sample_output_dhis2 = "https://example.com/dhis2_image.png"  # Replace with actual image URL
sample_output_dhs = "https://example.com/dhs_image.png"  # Replace with actual image URL
sample_output_climate = "https://example.com/climate_image.png"  # Replace with actual image URL
sample_output_lmis = "https://example.com/lmis_image.png"  # Replace with actual image URL
sample_output_modeled = "https://example.com/modeled_image.png"  # Replace with actual image URL
sample_output_population = "https://example.com/population_image.png"  # Replace with actual image URL

# Display content based on selected options
if data_option == 'Shapefiles':
    st.subheader("Shapefiles Content")
    
    if content_option == 'See R Code':
        st.code(r_code_shapefiles, language='r')
    elif content_option == 'See Python Code':
        st.code(python_code_shapefiles, language='python')
    elif content_option == 'Explanation of R Code':
        st.write(explanation_r_shapefiles)
    elif content_option == 'Explanation of Python Code':
        st.write(explanation_python_shapefiles)
    elif content_option == 'Sample Output':
        st.image(sample_output_shapefiles, caption="Sample output of the Shapefiles code")

elif data_option == 'Health Facilities':
    st.subheader("Health Facilities Content")
    
    if content_option == 'See R Code':
        st.code(r_code_health_facilities, language='r')
    elif content_option == 'See Python Code':
        st.code(python_code_health_facilities, language='python')
    elif content_option == 'Explanation of R Code':
        st.write(explanation_r_health_facilities)
    elif content_option == 'Explanation of Python Code':
        st.write(explanation_python_health_facilities)
    elif content_option == 'Sample Output':
        st.image(sample_output_health_facilities, caption="Sample output of the Health Facilities code")

# Add similar conditions for other data options if needed
elif data_option == 'Routine case data from DHIS2':
    st.subheader("Routine case data from DHIS2 Content")
    # Implement specific code and sample image for DHIS2 here
    if content_option == 'Sample Output':
        st.image(sample_output_dhis2, caption="Sample output of the DHIS2 code")

elif data_option == 'DHS data':
    st.subheader("DHS data Content")
    # Implement specific code and sample image for DHS data here
    if content_option == 'Sample Output':
        st.image(sample_output_dhs, caption="Sample output of the DHS data code")

elif data_option == 'Climate data':
    st.subheader("Climate data Content")
    # Implement specific code and sample image for Climate data here
    if content_option == 'Sample Output':
        st.image(sample_output_climate, caption="Sample output of the Climate data code")

elif data_option == 'LMIS data':
    st.subheader("LMIS data Content")
    # Implement specific code and sample image for LMIS data here
    if content_option == 'Sample Output':
        st.image(sample_output_lmis, caption="Sample output of the LMIS data code")

elif data_option == 'Modeled data':
    st.subheader("Modeled data Content")
    # Implement specific code and sample image for Modeled data here
    if content_option == 'Sample Output':
        st.image(sample_output_modeled, caption="Sample output of the Modeled data code")

elif data_option == 'Population data':
    st.subheader("Population data Content")
    # Implement specific code and sample image for Population data here
    if content_option == 'Sample Output':
        st.image(sample_output_population, caption="Sample output of the Population data code")

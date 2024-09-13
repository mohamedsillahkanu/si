import streamlit as st

# Function to display content based on selection
def show_content(selection):
    if selection == 'Motivation':
        st.subheader('Motivation')
        st.write("""
            SNT is here to stay: many NMCPs have found it useful and are continuing to embrace it...
        """)
    elif selection == 'Objectives':
        st.subheader('Objectives')
        st.write("""
            We will build a code library for SNT analysis to:
            - Ensure that SNT analysts are using similar, correct approaches
            - Improve efficiency of SNT analysis by minimizing duplication of effort
            - Promote accessibility of SNT analysis by lowering barriers to entry
        """)
    elif selection == 'Target audience':
        st.subheader('Target audience')
        st.write("""
            Anyone doing this kind of work. We assume some basic knowledge of R...
        """)
    elif selection == 'Scope':
        st.subheader('Scope')
        st.write("""
            All analysis steps of SNT up to but not including mathematical modeling...
        """)
    elif selection == 'A.1 Shapefiles':
        st.subheader('A.1 Shapefiles')
        st.write("""
            **A.1.1** Import shapefiles 
        """)

        st.write("""
            **A.1.2** Rename and match names 
        """)

        st.write("""
            **A.1.3** Link shapefiles to relevant scales
        """)

        st.write("""
            **A.1.4** Visualizing shapefiles and making basic maps 
        """)
          
        st.write("Here is an example R code snippet for importing shapefiles:")
        st.code("""
            # Load required libraries
            library(sf)
            
            # Import shapefile
            shapefile <- st_read("path/to/shapefile.shp")
            
            # Print basic info
            print(shapefile)
            
            # Plot the shapefile
            plot(shapefile)
        """, language='r')
        
    elif selection == 'A.2 Health Facilities':
        st.subheader('A.2 Health Facilities')
        st.write("""
            **A.2.1** Get MFL from the Malaria Program
            - Useful Columns:
                - adm0 - country
                - adm1 - province/region
                - adm2 - district
                - adm3 - subdistrict/sub-county
                - Health Facility (HF)
                - Date HF started reporting
                - Is HF still active?
                - Type of HF (District hospital, health post, etc.)
        """)
        st.write("Here is an example R code snippet for processing health facilities data:")
        st.code("""
            # Load required libraries
            library(dplyr)
            
            # Read health facilities data
            hf_data <- read.csv("path/to/health_facilities.csv")
            
            # Filter active health facilities
            active_hf <- hf_data %>%
                filter(is_active == TRUE)
            
            # Print the first few rows
            head(active_hf)
        """, language='r')
        
    # Add additional conditions for other sections here

# Sidebar for Table of Contents
st.sidebar.header('Table of Contents')
menu = st.sidebar.selectbox('Select a section', [
    'Motivation', 'Objectives', 'Target audience', 'Scope',
    'A.1 Shapefiles', 'A.2 Health Facilities', 'A.3 Routine case data from DHIS2',
    'A.4 DHS data', 'A.5 Climate data', 'A.6 LMIS data', 'A.7 Modeled data', 'A.8 Population data',
    'B. EPIDEMIOLOGICAL STRATIFICATION', 'C. STRATIFICATION OF OTHER DETERMINANTS',
    'D. REVIEW OF PAST INTERVENTIONS', 'E. Targeting of interventions', 'F. Retrospective analysis',
    'G. Urban microstratification'
])

# Display content based on selection
show_content(menu)

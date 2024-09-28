import streamlit as st
from streamlit_option_menu import option_menu

# Add custom CSS to increase sidebar width
st.markdown(
    """
    <style>
    /* Increase the width of the sidebar */
    [data-testid="stSidebar"] {
        width: 600px;  /* Adjust the width as needed */
    }
    [data-testid="stSidebarNav"] {
        width: 400px;  /* Keep the navigation width consistent */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state variable to track the selection
if "selected_toc" not in st.session_state:
    st.session_state.selected_toc = None

# Sidebar for Table of Contents (ToC)
with st.sidebar:
    st.title("Table of Contents")

    # All sections under one unified ToC
    selected_toc = option_menu(
        menu_title=None,  # No title
        options=[
            "A. Data Assembly and Management",  # Section A
            "A.1 Shapefiles",
            "A.2 Health Facilities",
            "A.3 Routine case data from DHIS2",
            "A.4 DHS data",
            "A.5 Population data",
            "A.6 Climate data",
            "A.7 LMIS data",
            "A.8 Modeled data",
            "B. Epidemiological Stratification",  # Section B
            "B.1 Reporting Rate per Variable",
            "B.2 Group and merge data frame",
            "B.3 Crude Incidence by Year",
            "B.4 Adjusted Incidence by Year",
            "B.5 Option to Select Incidence",
            "B.6 Risk Categorization",
            "C. Stratification of Other Determinants",  # Section C
            "C.1 Access to Care",
            "C.2 Seasonality",
            "D. Review of Past Interventions",  # Section D
            "D.1 EPI Coverage and Dropout Rate",
            "D.2 IPTp and ANC Coverage",
            "D.3 PMC (Perennial Malaria Chemoprevention)",
            "D.4 SMC (Seasonal Malaria Chemoprevention)",
            "D.5 Malaria Vaccine",
            "D.6 ITN Coverage, Ownership, Access, Usage, and Type",
            "D.7 IRS (Indoor Residual Spraying)",
            "D.8 MDA (Mass Drug Administration)",
            "D.9 IPTsc",
            "D.10 PDMC",
            "D.11 LSM",
            "D.12 Assessing the Quality of Case Management"
        ],
        icons=[""] * 30,  # Empty icons for all options
        menu_icon="cast",  # Icon for the menu itself
        default_index=-1,  # No default selection
        styles={
            "container": {"padding": "0!important", "background-color": "white"},
            "icon": {"color": "white", "font-size": "18px"},  # Hide icons
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "padding": "5px 10px",
                "color": "black",
                "background-color": "transparent"
            },
            "nav-link-selected": {
                "font-size": "16px",
                "background-color": "transparent",  # No background color on selection
                "color": "red"  # Text turns red when selected
            }
        }
    )

    # Update session state to track the selected option
    st.session_state.selected_toc = selected_toc

# Display the selected ToC option
if st.session_state.selected_toc:
    st.write(f"Selected option: {st.session_state.selected_toc}")

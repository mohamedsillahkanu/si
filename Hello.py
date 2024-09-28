import streamlit as st
from streamlit_option_menu import option_menu

# Add custom CSS to increase sidebar width and style section headers
st.markdown(
    """
    <style>
    /* Increase the width of the sidebar */
    [data-testid="stSidebar"] {
        width: 400px;
    }
    [data-testid="stSidebarNav"] {
        width: 400px;
    }
    /* Styling for section headers */
    .section-header {
        font-weight: bold;
        color: blue;
        font-size: 18px;
        margin-top: 20px;
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

    # All sections and subsections in one option_menu
    selected_toc = option_menu(
        menu_title=None,  # No title
        options=[
            "A. DATA ASSEMBLY AND MANAGEMENT",  # Section A as non-clickable text
            "A.1 Shapefiles",
            "A.2 Health Facilities",
            "A.3 Routine case data from DHIS2",
            "A.4 DHS data",
            "A.5 Population data",
            "A.6 Climate data",
            "A.7 LMIS data",
            "A.8 Modeled data",
            "B. Epidemiological Stratification",  # Section B as non-clickable text
            "B.1 Reporting Rate per Variable",
            "B.2 Group and merge data frame",
            "B.3 Crude Incidence by Year",
            "B.4 Adjusted Incidence by Year",
            "B.5 Option to Select Incidence",
            "B.6 Risk Categorization",
            "C. Stratification of Other Determinants",  # Section C as non-clickable text
            "C.1 Access to Care",
            "C.2 Seasonality",
            "D. Review of Past Interventions",  # Section D as non-clickable text
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
        icons=[""] * 34,  # Empty icons for all options
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

    # Add section header styling with st.markdown
    st.markdown(
        """
        <style>
        /* Apply blue color and bold style to section headings in the menu */
        li[data-option="A. Data Assembly and Management"],
        li[data-option="B. Epidemiological Stratification"],
        li[data-option="C. Stratification of Other Determinants"],
        li[data-option="D. Review of Past Interventions"] {
            font-weight: bold;
            color: blue;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Display the selected ToC option
if selected_toc:
    if selected_toc == "A. DATA ASSEMBLY AND MANAGEMENT":
        st.markdown('<p style="color:blue; font-weight:bold;">A. DATA ASSEMBLY AND MANAGEMENT</p>', unsafe_allow_html=True)
    else:
        st.write(f"Selected option: {selected_toc}")

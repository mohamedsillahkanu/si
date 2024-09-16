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
content_option = st.sidebar.selectbox(
    "Choose what to view:",
    (
        'See R Code',
        'Explanation of R Code',
        'See Python Code',
        'Explanation of Python Code',
        'Sample Output'
    )
)

# Sample R and Python code for demonstration
r_code = """
# Load the ggplot2 library
library(ggplot2)

# Create a simple scatter plot
ggplot(data = mtcars, aes(x = wt, y = mpg)) +
  geom_point() +
  labs(title = "Scatter plot of mpg vs. weight",
       x = "Weight (1000 lbs)",
       y = "Miles per Gallon")
"""

python_code = """
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load dataset
df = pd.DataFrame({
    'Weight': [2.5, 3.5, 4.5, 5.5, 6.5],
    'MPG': [25, 30, 22, 28, 24]
})

# Create a scatter plot
sns.scatterplot(x='Weight', y='MPG', data=df)
plt.title('Scatter plot of MPG vs. Weight')
plt.xlabel('Weight (1000 lbs)')
plt.ylabel('Miles per Gallon')
plt.show()
"""

# Explanation of the R and Python code
explanation_r = """
The R code demonstrates how to create a scatter plot using the `ggplot2` library.
1. `ggplot(data = mtcars, aes(x = wt, y = mpg))` initializes the plot with data.
2. `geom_point()` adds points to the plot.
3. `labs()` adds labels to the plot.
"""

explanation_python = """
The Python code demonstrates how to create a scatter plot using `seaborn` and `matplotlib`.
1. `sns.scatterplot(x='Weight', y='MPG', data=df)` creates the scatter plot.
2. `plt.title()`, `plt.xlabel()`, and `plt.ylabel()` add labels and title.
"""

# Content related to shapefiles
shapefile_content = {
    'Shapefiles': """
    **A.1 Shapefiles**:
    - A.1.1 Import shapefiles
    - A.1.2 Rename and match names
    - A.1.3 Link shapefiles to relevant scales
    - A.1.4 Visualizing shapefiles and making basic maps
    """,
    'Health Facilities': "Content for Health Facilities.",
    'Routine case data from DHIS2': "Content for Routine case data from DHIS2.",
    'DHS data': "Content for DHS data.",
    'Climate data': "Content for Climate data.",
    'LMIS data': "Content for LMIS data.",
    'Modeled data': "Content for Modeled data.",
    'Population data': "Content for Population data."
}

# Display content based on selected options
if data_option in shapefile_content:
    st.subheader(f"Content for {data_option}")
    st.markdown(shapefile_content[data_option])
else:
    if content_option == 'See R Code':
        st.code(r_code, language='r')
    elif content_option == 'Explanation of R Code':
        st.write(explanation_r)
    elif content_option == 'See Python Code':
        st.code(python_code, language='python')
    elif content_option == 'Explanation of Python Code':
        st.write(explanation_python)
    elif content_option == 'Sample Output':
        st.image("https://example.com/sample_output.png", caption="Sample output")

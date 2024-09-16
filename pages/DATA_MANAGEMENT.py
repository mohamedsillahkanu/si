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
st.title("R Code Display with Sample Output")

# Dropdown menu for displaying content
option = st.sidebar.selectbox("Choose an option:", ('None', 'See R Code', 'Explanation', 'Sample Output'))

# R Code to display
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

# Explanation for the R code
explanation = """
The above R code demonstrates how to create a scatter plot using the `ggplot2` library. 
1. The `ggplot()` function initializes the plot, where `data = mtcars` specifies the dataset.
2. The `aes()` function maps the `wt` column (weight) to the x-axis and `mpg` (miles per gallon) to the y-axis.
3. `geom_point()` adds points to the plot to represent each car.
4. The `labs()` function adds labels for the title and axes.
"""

# Logic for displaying R code, explanation, or sample output
if option == 'See R Code':
    st.code(r_code, language='r')
elif option == 'Explanation':
    st.write(explanation)
elif option == 'Sample Output':
    # Display the image from the provided GitHub link
    st.image("https://github.com/mohamedsillahkanu/si/blob/c6b5747886fb15b511fe99ac90afdbad64b0628f/image_10.png?raw=true", 
             caption="Sample output of the R code (scatter plot using ggplot2)")

# Provide context or additional instructions
st.markdown("""
This Streamlit app allows you to choose between viewing the R code for creating a scatter plot, 
an explanation of how the code works, or a sample output of the plot.
""")

import streamlit as st

# Apply sky blue background using custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: skyblue;
    }
    </style>
    """, unsafe_allow_html=True
)


# Custom CSS for sidebar background and text color
sidebar_bg_css = """
<style>
[data-testid="stSidebar"] {
    background-color: #FFB6C1; /* Sky blue background */
    color: #000000; /* Sidebar text color */
}
</style>
"""

# Title of the app
st.title("R Code Display and Explanation")

# Radio button to display R code or explanations
option = st.sidebar.selectbox("Choose an option:", ('None', 'See R Code', 'Explanation'))

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

# Logic for displaying R code or explanation
if option == 'See R Code':
    st.code(r_code, language='r')
elif option == 'Explanation':
    st.write(explanation)

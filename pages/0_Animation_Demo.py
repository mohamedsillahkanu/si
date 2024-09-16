import streamlit as st

# Apply sky blue background to main app and light pink to sidebar using custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: skyblue;
    }
    .css-1d391kg {  /* This class targets the sidebar */
        background-color: lightpink;
    }
    .code-block {
        max-width: 800px;
        word-wrap: break-word;
        margin: auto;
    }
    .explanation {
        max-width: 800px;
        word-wrap: break-word;
        margin: auto;
        font-size: 16px;
    }
    .centered-image img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        max-width: 90%;
    }
    </style>
    """, unsafe_allow_html=True
)

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
    st.markdown(f"<div class='code-block'>{st.code(r_code, language='r')}</div>", unsafe_allow_html=True)
elif option == 'Explanation':
    st.markdown(f"<div class='explanation'>{explanation}</div>", unsafe_allow_html=True)
elif option == 'Sample Output':
    st.markdown(
        """
        <div class='centered-image'>
            <img src='https://github.com/mohamedsillahkanu/si/blob/c6b5747886fb15b511fe99ac90afdbad64b0628f/image_10.png?raw=true' 
            alt='Sample output of the R code (scatter plot using ggplot2)' />
        </div>
        """, unsafe_allow_html=True)


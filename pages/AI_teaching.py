import streamlit as st
from transformers import pipeline

# Initialize the conversational model
generator = pipeline('text-generation', model='gpt2')

# Function to generate AI responses based on the user input
def generate_response(user_input):
    response = generator(user_input, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2)
    return response[0]['generated_text']

# Code for plotting a bar chart in Python
bar_chart_code = """
import matplotlib.pyplot as plt

# Data to plot
categories = ['A', 'B', 'C', 'D', 'E']
values = [3, 7, 2, 5, 8]

# Create the bar chart
plt.bar(categories, values)

# Add title and labels
plt.title('Bar Chart Example')
plt.xlabel('Categories')
plt.ylabel('Values')

# Display the plot
plt.show()
"""

# Function to explain the code
def explain_code():
    explanation = """
    This code demonstrates how to create a simple bar chart using the 'matplotlib' library in Python. 
    Let's break it down step by step:

    1. **Importing matplotlib:** The code starts by importing the `matplotlib.pyplot` module, which is used to create various types of plots, including bar charts.
    
    2. **Data to plot:** 
        - `categories` represents the labels for each bar (A, B, C, D, E).
        - `values` contains the corresponding values (3, 7, 2, 5, 8) for each category.
    
    3. **Creating the bar chart:** The `plt.bar()` function is used to plot the bar chart. It takes two arguments:
        - `categories` for the x-axis (the categories).
        - `values` for the y-axis (the heights of the bars).
    
    4. **Adding title and labels:** 
        - `plt.title()` adds a title to the chart.
        - `plt.xlabel()` labels the x-axis.
        - `plt.ylabel()` labels the y-axis.
    
    5. **Displaying the plot:** The `plt.show()` function displays the plot on the screen.

    This code generates a basic bar chart that shows the values for each category, and it adds titles and labels to make the chart more informative.
    """
    return explanation

# Streamlit user interface for the teaching agent
def main():
    st.title("AI Teaching Agent: Explain Bar Chart Code")
    st.markdown("This AI-powered teaching assistant explains how to plot a bar chart in Python.")

    # Display the code to the user
    st.markdown("### Python Code for Plotting a Bar Chart:")
    st.code(bar_chart_code, language='python')

    # Input box for the user to enter their question
    user_input = st.text_input("Ask about the code or type 'explain' to get an explanation:", "")

    if user_input:
        if user_input.lower() == 'explain':
            explanation = explain_code()
            st.write("### Explanation of the Code:")
            st.markdown(explanation)
        else:
            st.write("You asked: ", user_input)
            ai_response = generate_response(user_input)
            st.write("AI says: ", ai_response)

    st.markdown("### How It Works:")
    st.markdown("""
    This AI uses a GPT-2 language model to generate explanations based on your questions about the code.
    When you ask for an explanation, it breaks down the code and describes each part of the process.
    """)

if __name__ == "__main__":
    main()

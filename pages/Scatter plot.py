import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# App title
st.title("1:1 Scatter Plot Visualization")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["1:1 Scatter Plot Overview", "1:1 Scatter Plot Illustration"])

# 1. 1:1 Scatter Plot Overview Section
if section == "1:1 Scatter Plot Overview":
    st.header("1:1 Scatter Plot for Data Comparison")
    
    st.subheader("When to Use It")
    st.write("""
        A 1:1 scatter plot is used to compare two variables by plotting their values against each other, often to evaluate agreement or correlation between the two.
        It is particularly useful in identifying biases, trends, or outliers.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for creating a 1:1 scatter plot:")
    st.write("1. **Two Numerical Variables**: Data for both variables must be continuous.")
    
    st.subheader("Purpose of a 1:1 Scatter Plot")
    st.write("""
        The purpose of a 1:1 scatter plot is to visually assess the relationship between two variables. 
        The plot can help determine if the values are similar (i.e., lie close to the 1:1 line), and identify systematic biases or significant deviations.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Scatter Plot](https://en.wikipedia.org/wiki/Scatter_plot).")

# 2. 1:1 Scatter Plot Illustration Section
elif section == "1:1 Scatter Plot Illustration":
    st.header("1:1 Scatter Plot Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="scatter_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the relevant columns
            x_column = st.selectbox("Select the X-axis variable", df.columns)
            y_column = st.selectbox("Select the Y-axis variable", df.columns)
            
            # Plot the 1:1 scatter plot
            st.subheader("1:1 Scatter Plot Visualization")
            plt.figure(figsize=(10, 6))
            plt.scatter(df[x_column], df[y_column], color='blue', label='Data Points')
            plt.plot([df[x_column].min(), df[x_column].max()], [df[x_column].min(), df[x_column].max()], color='red', linestyle='--', label='1:1 Line')
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.title('1:1 Scatter Plot')
            plt.legend()
            st.pyplot(plt)
            
            # Interpretation tips
            st.subheader("How to Interpret the 1:1 Scatter Plot")
            st.write("""
                - **1:1 Line**: The red dashed line represents the 1:1 relationship, where values on the X and Y axes are equal.
                - **Data Points**: Points lying close to the 1:1 line indicate agreement between the two variables. Points far from the line may indicate biases or discrepancies.
                - **Systematic Bias**: A consistent offset of points from the 1:1 line may suggest a systematic bias between the variables.
            """)
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



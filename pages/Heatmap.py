import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# App title
st.title("Heatmap Visualization")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Heatmap Overview", "Heatmap Illustration"])

# 1. Heatmap Overview Section
if section == "Heatmap Overview":
    st.header("Heatmap for Data Visualization")
    
    st.subheader("When to Use It")
    st.write("""
        A heatmap is a data visualization tool that uses color to represent the values of a matrix. It is often used to show correlations between variables, identify patterns, and detect anomalies in the data.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for creating a heatmap:")
    st.write("1. **Two-Dimensional Data**: A matrix or DataFrame with numerical values.")
    
    st.subheader("Purpose of a Heatmap")
    st.write("""
        The purpose of a heatmap is to provide a quick and intuitive way to visualize relationships and patterns in the data. 
        Heatmaps are often used for correlation matrices, feature importance, and data distribution visualization.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Heatmaps](https://en.wikipedia.org/wiki/Heat_map).")

# 2. Heatmap Illustration Section
elif section == "Heatmap Illustration":
    st.header("Heatmap Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="heatmap_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the columns to include in the heatmap
            columns = st.multiselect("Select the columns to include in the heatmap", df.columns)
            
            if len(columns) >= 2:
                # Create a correlation matrix for the selected columns
                corr_matrix = df[columns].corr()
                
                # Plot the heatmap
                st.subheader("Heatmap Visualization")
                plt.figure(figsize=(10, 6))
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
                plt.title('Correlation Heatmap')
                st.pyplot(plt)
                
                # Interpretation tips
                st.subheader("How to Interpret the Heatmap")
                st.write("""
                    - **Color Intensity**: The color intensity represents the strength of the correlation. Darker colors indicate stronger correlations.
                    - **Correlation Values**: The numbers in each cell represent the correlation coefficient between the variables.
                    - **Positive vs Negative Correlation**: Positive values indicate positive correlation, while negative values indicate negative correlation between variables.
                """)
            else:
                st.warning("Please select at least two columns to create a heatmap.")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



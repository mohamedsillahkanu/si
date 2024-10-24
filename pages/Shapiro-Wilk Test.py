import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import shapiro
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("Shapiro-Wilk Test for Normality")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Shapiro-Wilk Test Overview", "Shapiro-Wilk Test Illustration"])

# 1. Shapiro-Wilk Test Overview Section
if section == "Shapiro-Wilk Test Overview":
    st.header("Shapiro-Wilk Test for Normality")
    
    st.subheader("When to Use It")
    st.write("""
        The Shapiro-Wilk Test is used to assess whether a dataset is normally distributed. It is commonly used to determine if the data meets the assumptions of statistical tests that require normally distributed data.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following variable for performing a Shapiro-Wilk Test:")
    st.write("1. **Sample Data**: The sample observations for which you want to test for normality.")
    
    st.subheader("Purpose of the Shapiro-Wilk Test")
    st.write("""
        The purpose of the Shapiro-Wilk Test is to determine whether a sample comes from a normally distributed population. 
        A significant result (p-value < 0.05) suggests that the data is not normally distributed.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here is a practical example of how the Shapiro-Wilk Test can be used in malaria research:")
    
    st.write("""
    **Testing Normality of Blood Parasite Counts**: 
       Researchers can use the Shapiro-Wilk Test to determine if the blood parasite count data follows a normal distribution before applying parametric statistical tests.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Shapiro-Wilk Test](https://en.wikipedia.org/wiki/Shapiro%E2%80%93Wilk_test).")

# 2. Shapiro-Wilk Test Illustration Section
elif section == "Shapiro-Wilk Test Illustration":
    st.header("Shapiro-Wilk Test Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="shapiro_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the column to perform the Shapiro-Wilk Test
            column = st.selectbox("Select the variable for Shapiro-Wilk Test", df.columns)
            
            # Button to perform the Shapiro-Wilk Test
            if st.button("Perform Shapiro-Wilk Test"):
                try:
                    # Perform the Shapiro-Wilk Test
                    stat, p_value = shapiro(df[column])
                    
                    # Display the Shapiro-Wilk Test results
                    st.write(f"**Shapiro-Wilk Test Statistic:** {stat}")
                    st.write(f"**P-Value:** {p_value}")
                    
                    # Display a tip for interpretation
                    st.write("""
                    **Tip for Interpretation**: 
                    - The p-value helps determine whether the data is normally distributed. A p-value less than 0.05 generally indicates that the data is not normally distributed.
                    """)
                    
                    # Plot the histogram and Q-Q plot
                    st.write("**Histogram of the Data**:")
                    plt.figure(figsize=(10, 6))
                    sns.histplot(df[column], kde=True)
                    plt.xlabel(column)
                    plt.ylabel("Frequency")
                    plt.title("Histogram with KDE")
                    st.pyplot(plt)
                    
                    st.write("**Q-Q Plot**:")
                    from scipy import stats
                    stats.probplot(df[column], dist="norm", plot=plt)
                    plt.title("Q-Q Plot")
                    st.pyplot(plt)
                
                except Exception as e:
                    st.error(f"Error during Shapiro-Wilk Test: {e}")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")

# requirements.txt content
requirements_txt = """
streamlit
pandas
numpy
scipy
matplotlib
seaborn
"""
with open('requirements.txt', 'w') as f:
    f.write(requirements_txt)

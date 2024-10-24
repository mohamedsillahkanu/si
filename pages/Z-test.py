import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.stats.weightstats import ztest
import matplotlib.pyplot as plt

# App title
st.title("Z-Test for Hypothesis Testing")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Z-Test Overview", "Z-Test Illustration"])

# 1. Z-Test Overview Section
if section == "Z-Test Overview":
    st.header("Z-Test for Hypothesis Testing")
    
    st.subheader("When to Use It")
    st.write("""
        A Z-Test is a statistical test used to determine whether there is a significant difference between sample and population means, or between the means of two samples.
        It is used when the sample size is large (typically n > 30) and the population variance is known.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following variables for performing a Z-Test:")
    st.write("1. **Sample Data**: The sample observations for which you want to perform the test.")
    st.write("2. **Population Mean (optional)**: The population mean to compare against (for one-sample z-test).")
    
    st.subheader("Purpose of the Z-Test")
    st.write("""
        The purpose of the Z-Test is to determine whether the observed difference is statistically significant or if it could have occurred by random chance.
        It can be used to test hypotheses about population means.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how the Z-Test can be used in malaria research:")
    
    st.write("""
    1. **Testing the Effect of a Drug on Parasite Counts**: 
       Researchers can use the Z-Test to determine if the average parasite count in patients treated with a new drug is significantly different from the known average.
    """)
    
    st.write("""
    2. **Comparing Blood Hemoglobin Levels**: 
       A Z-Test can be used to compare the mean hemoglobin levels of two groups (e.g., treated versus control group) to determine if the treatment has a significant effect.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Z-Test](https://en.wikipedia.org/wiki/Z-test).")

# 2. Z-Test Illustration Section
elif section == "Z-Test Illustration":
    st.header("Z-Test Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="ztest_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the column to perform the z-test
            column = st.selectbox("Select the variable for Z-Test", df.columns)
            
            # Optional input for population mean
            pop_mean = st.number_input("Enter the population mean (optional, for one-sample Z-Test)", value=0.0)
            
            # Button to perform the Z-Test
            if st.button("Perform Z-Test"):
                try:
                    # Perform one-sample z-test if population mean is provided
                    if pop_mean != 0.0:
                        z_stat, p_value = ztest(df[column], value=pop_mean)
                    else:
                        st.error("Population mean must be provided for a one-sample Z-Test.")
                        raise ValueError("Population mean is required.")
                    
                    # Display the Z-Test results
                    st.write(f"**Z-Statistic:** {z_stat}")
                    st.write(f"**P-Value:** {p_value}")
                    
                    # Display a tip for interpretation
                    st.write("""
                    **Tip for Interpretation**: 
                    - The Z-statistic indicates how many standard deviations the sample mean is away from the population mean.
                    - The p-value helps determine the significance of the results. A p-value less than 0.05 generally indicates a significant difference.
                    """)
                except Exception as e:
                    st.error(f"Error during Z-Test: {e}")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



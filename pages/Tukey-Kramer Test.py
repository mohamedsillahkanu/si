import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt

# App title
st.title("Tukey-Kramer Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Tukey-Kramer Test")
    
    st.subheader("When to Use It")
    st.write("""
        The Tukey-Kramer test is a post-hoc test performed after a one-way ANOVA to compare the means of every pair 
        of groups when the sample sizes are unequal. It helps determine which group means are significantly different 
        from each other.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("The test requires multiple groups with different sample sizes. One numeric variable and one categorical variable are needed.")
    
    st.subheader("Number of Categorical and Numeric Variables")
    st.write("You need one categorical variable to define the groups and one numeric variable whose means you want to compare.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the Tukey-Kramer test is to determine which specific pairs of groups have significantly different means
        after conducting an ANOVA test that shows overall differences among the groups.
    """)
    
    st.subheader("Real-Life Medical Example (Malaria)")
    st.write("""
    **Comparing Malaria Treatment Outcomes Across Different Drug Groups**: If a researcher wants to compare the efficacy (e.g., reduction 
    in parasite count) of different drugs used to treat malaria, they can use the Tukey-Kramer test to compare the mean efficacy
    of each drug group after performing ANOVA.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Tukey-Kramer Test")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the numeric and categorical columns
            num_column = st.selectbox("Select the numeric variable (e.g., outcome measure)", df.select_dtypes(include=[np.number]).columns)
            cat_column = st.selectbox("Select the categorical variable (e.g., treatment group)", df.select_dtypes(include=['object', 'category']).columns)
            
            st.write(f"You selected: {num_column} as the numeric variable and {cat_column} as the categorical variable.")
            
            # Perform Tukey-Kramer Test
            tukey_result = pairwise_tukeyhsd(endog=df[num_column], groups=df[cat_column], alpha=0.05)
            
            # Display results
            st.write("Tukey-Kramer Test Results:")
            st.write(tukey_result)
            
            # Plot the results
            fig = tukey_result.plot_simultaneous()
            st.pyplot(fig)
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

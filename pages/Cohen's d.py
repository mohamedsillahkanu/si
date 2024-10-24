import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("Cohen's d Effect Size Calculation")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Cohen's d Overview", "Cohen's d Illustration"])

# 1. Cohen's d Overview Section
if section == "Cohen's d Overview":
    st.header("Cohen's d for Effect Size")
    
    st.subheader("When to Use It")
    st.write("""
        Cohen's d is a measure of effect size used to indicate the standardized difference between two means.
        It is often used in experimental studies to quantify the magnitude of the effect between two groups.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following variables for calculating Cohen's d:")
    st.write("1. **Two Sample Groups**: Data from two groups (e.g., treatment and control groups) for which you want to measure the effect size.")
    
    st.subheader("Purpose of Cohen's d")
    st.write("""
        The purpose of Cohen's d is to provide a standardized measure of the difference between two groups. 
        It helps quantify how large the effect is, making it easier to interpret the practical significance of the results.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here is a practical example of how Cohen's d can be used in malaria research:")
    
    st.write("""
    **Comparing Treatment Efficacy**: 
       Researchers can use Cohen's d to determine the effect size of a new antimalarial drug compared to a placebo by calculating the difference in parasite counts between the two groups.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Cohen's d](https://en.wikipedia.org/wiki/Effect_size#Cohen's_d).")

# 2. Cohen's d Illustration Section
elif section == "Cohen's d Illustration":
    st.header("Cohen's d Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="cohen_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the group and outcome columns
            group_column = st.selectbox("Select the group variable", df.columns)
            outcome_column = st.selectbox("Select the outcome variable", df.columns)
            
            # Button to calculate Cohen's d
            if st.button("Calculate Cohen's d"):
                try:
                    # Separate the groups
                    group1 = df[df[group_column] == df[group_column].unique()[0]][outcome_column]
                    group2 = df[df[group_column] == df[group_column].unique()[1]][outcome_column]
                    
                    # Calculate Cohen's d
                    mean_diff = np.mean(group1) - np.mean(group2)
                    pooled_std = np.sqrt((np.var(group1, ddof=1) + np.var(group2, ddof=1)) / 2)
                    cohen_d = mean_diff / pooled_std
                    
                    # Display Cohen's d result
                    st.write(f"**Cohen's d Effect Size:** {cohen_d}")
                    
                    # Display a tip for interpretation
                    st.write("""
                    **Tip for Interpretation**: 
                    - A Cohen's d of 0.2 is considered a small effect, 0.5 is a medium effect, and 0.8 or greater is a large effect.
                    """)
                    
                    # Plot the distributions of the two groups
                    st.write("**Distribution of the Two Groups**:")
                    plt.figure(figsize=(10, 6))
                    sns.histplot(group1, color='blue', label=f'{df[group_column].unique()[0]}', kde=True)
                    sns.histplot(group2, color='orange', label=f'{df[group_column].unique()[1]}', kde=True)
                    plt.xlabel(outcome_column)
                    plt.ylabel("Frequency")
                    plt.title("Distributions of the Two Groups")
                    plt.legend()
                    st.pyplot(plt)
                
                except Exception as e:
                    st.error(f"Error during Cohen's d calculation: {e}")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kstest
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("Kolmogorov-Smirnov Test for Normality")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Kolmogorov-Smirnov Test Overview", "Kolmogorov-Smirnov Test Illustration"])

# 1. Kolmogorov-Smirnov Test Overview Section
if section == "Kolmogorov-Smirnov Test Overview":
    st.header("Kolmogorov-Smirnov Test for Normality")
    
    st.subheader("When to Use It")
    st.write("""
        The Kolmogorov-Smirnov (K-S) Test is used to assess whether a sample comes from a specific distribution, typically the normal distribution.
        It is commonly used to determine if data is normally distributed before applying parametric tests.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following variable for performing the Kolmogorov-Smirnov Test:")
    st.write("1. **Sample Data**: The sample observations for which you want to test for normality.")
    
    st.subheader("Purpose of the Kolmogorov-Smirnov Test")
    st.write("""
        The purpose of the K-S Test is to determine whether a sample comes from a specified distribution. 
        A significant result (p-value < 0.05) suggests that the sample does not come from the specified distribution.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here is a practical example of how the Kolmogorov-Smirnov Test can be used in malaria research:")
    
    st.write("""
    **Testing Normality of Parasite Counts**: 
       Researchers can use the K-S Test to determine if blood parasite count data follows a normal distribution before applying parametric statistical tests.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Kolmogorov-Smirnov Test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test).")

# 2. Kolmogorov-Smirnov Test Illustration Section
elif section == "Kolmogorov-Smirnov Test Illustration":
    st.header("Kolmogorov-Smirnov Test Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="ks_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the column to perform the K-S Test
            column = st.selectbox("Select the variable for Kolmogorov-Smirnov Test", df.columns)
            
            # Button to perform the K-S Test
            if st.button("Perform Kolmogorov-Smirnov Test"):
                try:
                    # Perform the Kolmogorov-Smirnov Test
                    stat, p_value = kstest(df[column], 'norm', args=(df[column].mean(), df[column].std()))
                    
                    # Display the K-S Test results
                    st.write(f"**Kolmogorov-Smirnov Test Statistic:** {stat}")
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
                    st.error(f"Error during Kolmogorov-Smirnov Test: {e}")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



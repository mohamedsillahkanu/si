import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import normaltest
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("D'Agostino's K-squared Test for Normality")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["D'Agostino's Test Overview", "D'Agostino's Test Illustration"])

# 1. D'Agostino's Test Overview Section
if section == "D'Agostino's Test Overview":
    st.header("D'Agostino's K-squared Test for Normality")
    
    st.subheader("When to Use It")
    st.write("""
        D'Agostino's K-squared Test is used to assess whether a dataset is normally distributed. 
        It combines skewness and kurtosis to determine if the sample comes from a normal distribution.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following variable for performing D'Agostino's K-squared Test:")
    st.write("1. **Sample Data**: The sample observations for which you want to test for normality.")
    
    st.subheader("Purpose of D'Agostino's Test")
    st.write("""
        The purpose of D'Agostino's K-squared Test is to determine whether a sample comes from a normally distributed population. 
        A significant result (p-value < 0.05) suggests that the data is not normally distributed.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here is a practical example of how D'Agostino's Test can be used in malaria research:")
    
    st.write("""
    **Testing Normality of Blood Hemoglobin Levels**: 
       Researchers can use D'Agostino's Test to determine if blood hemoglobin level data follows a normal distribution before applying parametric statistical tests.
    """)
    
    st.write("For more information, visit the [Wikipedia page on D'Agostino's K-squared Test](https://en.wikipedia.org/wiki/D%27Agostino%27s_K-squared_test).")

# 2. D'Agostino's Test Illustration Section
elif section == "D'Agostino's Test Illustration":
    st.header("D'Agostino's Test Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="dagostino_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the column to perform D'Agostino's Test
            column = st.selectbox("Select the variable for D'Agostino's Test", df.columns)
            
            # Button to perform D'Agostino's Test
            if st.button("Perform D'Agostino's Test"):
                try:
                    # Perform D'Agostino's Test
                    stat, p_value = normaltest(df[column])
                    
                    # Display the D'Agostino's Test results
                    st.write(f"**D'Agostino's K-squared Test Statistic:** {stat}")
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
                    st.error(f"Error during D'Agostino's Test: {e}")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")


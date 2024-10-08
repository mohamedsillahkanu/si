import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("Nested ANOVA Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Nested ANOVA")
    
    st.subheader("When to Use It")
    st.write("""
        Nested ANOVA is used to analyze data with a hierarchical structure, where one or more factors are nested 
        within other factors. This is common in experimental designs, where groups (e.g., schools, clinics) 
        contain sub-groups (e.g., students, patients).
    """)
    
    st.subheader("Number of Samples Required")
    st.write("You need a minimum of two levels for each nested factor and enough observations to provide reliable estimates.")
    
    st.subheader("Number of Categorical Variables")
    st.write("At least two categorical variables are needed: one for the main factor and one nested within it.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of Nested ANOVA is to assess whether there are statistically significant differences 
        between the means of different groups when accounting for the nested structure of the data.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Malaria Incidence by Region and Treatment Type**: Researchers can assess whether the incidence of malaria 
       differs across various regions, while considering the treatment types used in each region.
    """)
    
    st.write("""
    2. **Patient Recovery Rates by Hospital and Treatment Protocol**: This analysis can evaluate if recovery rates 
       differ between hospitals, accounting for different treatment protocols employed within each hospital.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Nested ANOVA")
    
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
            
            # Ask the user to select the response variable and the nested factors
            response_variable = st.selectbox("Select the response variable", df.columns)
            main_factor = st.selectbox("Select the main factor", df.columns)
            nested_factor = st.selectbox("Select the nested factor", df.columns)
            
            st.write(f"You selected: {response_variable}, {main_factor}, and {nested_factor} for the test.")
            
            # Fit the Nested ANOVA model
            formula = f"{response_variable} ~ C({main_factor}) / C({nested_factor})"
            model = ols(formula, data=df).fit()
            anova_table = sm.stats.anova_lm(model, typ=2)
            
            # Display ANOVA table
            st.write("Nested ANOVA Results:")
            st.write(anova_table)
            
            # Plotting the results
            plt.figure(figsize=(10, 6))
            sns.boxplot(x=main_factor, y=response_variable, data=df)
            plt.title("Boxplot of Response Variable by Main Factor")
            st.pyplot(plt)
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

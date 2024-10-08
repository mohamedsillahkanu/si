import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols

# App title
st.title("Two-Way ANOVA Test")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Two-Way ANOVA Test")
    
    st.subheader("When to Use It")
    st.write("""
        The Two-Way ANOVA test is used to evaluate whether two categorical independent variables have an effect on a 
        continuous dependent variable. It also assesses if there is an interaction effect between the two independent 
        variables.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("Two categorical independent variables and one continuous dependent variable with at least a few data points in each group.")

    st.subheader("Number of Categorical Variables")
    st.write("Two categorical independent variables and one continuous dependent variable.")

    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the Two-Way ANOVA test is to analyze how the independent variables affect the dependent variable,
        whether independently or through interaction.
    """)

    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("""
    1. **Effect of Medication and Age on Malaria Recovery Time**: You could assess how two categorical factors—type of 
       malaria medication and age group—affect the continuous dependent variable, recovery time.
    """)
    
    st.write("""
    2. **Effect of Region and Treatment on Malaria Severity**: Two factors, treatment type and region, could affect 
       malaria severity, and Two-Way ANOVA helps analyze these effects.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Two-Way ANOVA Test")

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

            # Ask the user to select the two categorical variables and one continuous variable
            cat_var1 = st.selectbox("Select the first categorical variable (Factor 1)", df.columns)
            cat_var2 = st.selectbox("Select the second categorical variable (Factor 2)", df.columns)
            cont_var = st.selectbox("Select the continuous dependent variable", df.columns)

            st.write(f"You selected: {cat_var1}, {cat_var2}, and {cont_var} for the test.")

            # Perform Two-Way ANOVA
            formula = f'{cont_var} ~ C({cat_var1}) + C({cat_var2}) + C({cat_var1}):C({cat_var2})'
            model = ols(formula, data=df).fit()
            anova_table = sm.stats.anova_lm(model, typ=2)

            # Display the ANOVA table
            st.write("Two-Way ANOVA Results:")
            st.write(anova_table)

            # Interpretation of results
            st.write("""
            - If the p-value for each factor is less than 0.05, it suggests that the factor significantly affects the dependent variable.
            - If the p-value for the interaction term (Factor 1:Factor 2) is less than 0.05, it suggests that there is a significant interaction effect between the two factors.
            """)

        except Exception as e:
            st.error(f"Error loading file: {e}")

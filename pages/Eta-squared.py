import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("Eta-Squared Effect Size Calculation")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Eta-Squared Overview", "Eta-Squared Illustration"])

# 1. Eta-Squared Overview Section
if section == "Eta-Squared Overview":
    st.header("Eta-Squared for Effect Size")
    
    st.subheader("When to Use It")
    st.write("""
        Eta-squared is a measure of effect size used in the context of ANOVA to indicate the proportion of variance explained by a factor.
        It is commonly used in experimental studies to quantify the magnitude of the effect of categorical independent variables on a continuous dependent variable.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following variables for calculating eta-squared:")
    st.write("1. **Categorical Independent Variable**: The grouping variable for the analysis.")
    st.write("2. **Continuous Dependent Variable**: The outcome variable for which you want to measure the effect size.")
    
    st.subheader("Purpose of Eta-Squared")
    st.write("""
        The purpose of eta-squared is to provide a standardized measure of the proportion of variance explained by one or more factors.
        It helps quantify the practical significance of the effect in the context of ANOVA.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here is a practical example of how eta-squared can be used in malaria research:")
    
    st.write("""
    **Assessing the Effect of Treatment Types**: 
       Researchers can use eta-squared to determine the effect size of different treatment types on reducing malaria symptoms by analyzing variance in patient outcomes.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Eta-Squared](https://en.wikipedia.org/wiki/Eta-squared).")

# 2. Eta-Squared Illustration Section
elif section == "Eta-Squared Illustration":
    st.header("Eta-Squared Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="eta_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the independent and dependent variables
            group_column = st.selectbox("Select the categorical independent variable (grouping variable)", df.columns)
            outcome_column = st.selectbox("Select the continuous dependent variable (outcome variable)", df.columns)
            
            # Button to calculate eta-squared
            if st.button("Calculate Eta-Squared"):
                try:
                    # Fit the ANOVA model using statsmodels
                    model = smf.ols(f'{outcome_column} ~ C({group_column})', data=df).fit()
                    anova_table = sm.stats.anova_lm(model, typ=2)
                    
                    # Calculate eta-squared
                    sum_sq_between = anova_table['sum_sq'][0]
                    sum_sq_total = sum_sq_between + anova_table['sum_sq'][1]
                    eta_squared = sum_sq_between / sum_sq_total
                    
                    # Display eta-squared result
                    st.write(f"**Eta-Squared Effect Size:** {eta_squared}")
                    
                    # Display a tip for interpretation
                    st.write("""
                    **Tip for Interpretation**: 
                    - An eta-squared value of 0.01 is considered a small effect, 0.06 is a medium effect, and 0.14 or greater is a large effect.
                    """)
                    
                    # Plot the distributions of the groups
                    st.write("**Distribution of the Groups**:")
                    plt.figure(figsize=(10, 6))
                    sns.boxplot(x=group_column, y=outcome_column, data=df)
                    plt.xlabel(group_column)
                    plt.ylabel(outcome_column)
                    plt.title("Boxplot of the Groups")
                    st.pyplot(plt)
                
                except Exception as e:
                    st.error(f"Error during Eta-Squared calculation: {e}")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")


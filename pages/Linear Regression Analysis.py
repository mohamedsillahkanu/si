import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("Linear Regression Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Linear Regression")
    
    st.subheader("When to Use It")
    st.write("""
        Linear regression is used when you want to model the relationship between one dependent variable (which should be continuous) 
        and one or more independent variables. The goal is to predict the dependent variable using the independent variables.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("At least 30 samples are recommended, but more samples usually lead to more accurate models.")
    
    st.subheader("Number of Variables")
    st.write("""
        - One dependent variable (continuous).
        - One or more independent variables (continuous or categorical).
    """)
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of linear regression is to understand the relationship between independent variables and the dependent variable. 
        It allows you to make predictions and assess how well your model explains the variation in the outcome variable.
    """)
    
    st.subheader("Real-Life Medical Examples")
    st.write("""
    1. **Predicting Blood Pressure from Age and Weight**: A linear regression can be used to model the relationship between 
       patient age, weight, and their blood pressure.
    2. **Predicting Recovery Time from Treatment Dosage**: This can model the relationship between treatment dosage and recovery time, 
       controlling for other factors like age or severity of the disease.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Linear Regression")
    
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
            
            # Ask the user to select the dependent and independent variables
            dep_var = st.selectbox("Select the dependent variable (Y)", df.columns)
            indep_vars = st.multiselect("Select the independent variable(s) (X)", df.columns)
            
            if len(indep_vars) > 0:
                st.write(f"Running regression with {dep_var} as the dependent variable and {', '.join(indep_vars)} as the independent variable(s).")
                
                # Add constant to independent variables
                X = df[indep_vars]
                X = sm.add_constant(X)
                
                # Dependent variable
                Y = df[dep_var]
                
                # Run OLS regression
                model = sm.OLS(Y, X).fit()
                
                # Display the regression results
                st.subheader("Regression Results")
                st.write(model.summary())
                
                # Plot regression results
                st.subheader("Scatter Plot with Regression Line")
                if len(indep_vars) == 1:  # Only plot if one independent variable is selected
                    plt.figure(figsize=(10, 6))
                    sns.regplot(x=df[indep_vars[0]], y=Y, line_kws={"color": "red"})
                    plt.xlabel(indep_vars[0])
                    plt.ylabel(dep_var)
                    plt.title(f"Regression Plot: {dep_var} vs {indep_vars[0]}")
                    st.pyplot(plt)
                else:
                    st.write("Scatter plot is only available for one independent variable.")
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

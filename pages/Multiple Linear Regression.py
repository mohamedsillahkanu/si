import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("Multiple Linear Regression")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Multiple Linear Regression")
    
    st.subheader("When to Use It")
    st.write("""
        Multiple Linear Regression (MLR) is used when you want to predict the value of a dependent variable
        based on two or more independent variables. It helps in modeling the linear relationship between the dependent
        variable and multiple predictors.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("""
        At least one dependent variable (target) and two or more independent variables (predictors) are required for multiple
        linear regression.
    """)
    
    st.subheader("Number of Categorical and Numeric Variables")
    st.write("""
        - The dependent variable should be continuous (numeric).
        - The independent variables can be a mix of categorical and numeric variables.
    """)
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of Multiple Linear Regression is to understand how each independent variable influences the
        dependent variable and to predict the dependent variable based on the values of the independent variables.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Predicting Malaria Incidence**: You can use MLR to predict the number of malaria cases in a region based on
       variables such as temperature, rainfall, population density, and availability of bed nets.
    """)
    
    st.write("""
    2. **Modeling Treatment Success**: Use MLR to predict treatment success (e.g., recovery rate) based on patient age,
       severity of symptoms, time to treatment, and other factors.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Multiple Linear Regression")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        try:
            # Load the dataset based on file type
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the dependent variable (target) and independent variables (predictors)
            target_var = st.selectbox("Select the dependent variable (target)", df.columns)
            predictors = st.multiselect("Select independent variables (predictors)", df.columns)
            
            if len(predictors) > 0:
                X = df[predictors]
                y = df[target_var]
                
                # Add constant (intercept) to the model
                X = sm.add_constant(X)
                
                # Fit the multiple linear regression model
                model = sm.OLS(y, X).fit()
                
                # Display regression results
                st.subheader("Regression Results")
                st.write(model.summary())
                
                # Visualize residuals
                st.subheader("Residual Plot")
                residuals = model.resid
                fitted = model.fittedvalues
                
                fig, ax = plt.subplots()
                sns.scatterplot(x=fitted, y=residuals, ax=ax)
                ax.axhline(0, color='red', linestyle='--')
                ax.set_xlabel('Fitted values')
                ax.set_ylabel('Residuals')
                ax.set_title('Residual Plot')
                st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Error loading file: {e}")

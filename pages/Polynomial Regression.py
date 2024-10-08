import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("Polynomial Regression")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Polynomial Regression")
    
    st.subheader("When to Use It")
    st.write("""
        Polynomial regression is used when the relationship between the independent and dependent variables is non-linear, 
        but can still be modeled by a polynomial function. It fits a polynomial equation to the data and helps in understanding 
        curvilinear relationships.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("A minimum of 20 samples is recommended for fitting a polynomial regression model. The larger the dataset, the better.")

    st.subheader("Number of Variables")
    st.write("At least one numeric independent variable (X) and one numeric dependent variable (Y) are needed.")

    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of polynomial regression is to predict the dependent variable (Y) based on the independent variable (X), 
        while allowing for non-linear relationships between them.
    """)

    st.subheader("Real-Life Example (Medical)")
    st.write("An example is predicting malaria infection counts based on environmental factors (e.g., rainfall), where the relationship is non-linear.")

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Polynomial Regression")
    
    # Upload your dataset
    uploaded_file = st.file_uploader("Upload your dataset (CSV or XLSX)", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        # Load the dataset
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Allow user to select the independent and dependent variables
            independent_var = st.selectbox("Select the independent variable (X)", df.select_dtypes(include=np.number).columns)
            dependent_var = st.selectbox("Select the dependent variable (Y)", df.select_dtypes(include=np.number).columns)
            
            # Select the degree of polynomial
            degree = st.slider("Select the degree of the polynomial", min_value=1, max_value=5, value=2)
            
            # Prepare the data for polynomial regression
            X = df[independent_var].values.reshape(-1, 1)
            y = df[dependent_var].values
            
            poly = PolynomialFeatures(degree=degree)
            X_poly = poly.fit_transform(X)
            
            # Fit polynomial regression model
            model = LinearRegression()
            model.fit(X_poly, y)
            
            # Predictions
            y_pred = model.predict(X_poly)
            
            # Display the results
            st.subheader("Polynomial Regression Results")
            st.write(f"Degree of Polynomial: {degree}")
            st.write(f"Mean Squared Error: {mean_squared_error(y, y_pred)}")
            st.write(f"R² Score: {r2_score(y, y_pred)}")
            
            # Visualize the polynomial regression fit
            st.subheader("Polynomial Fit Visualization")
            plt.figure(figsize=(10, 6))
            plt.scatter(X, y, color='blue', label='Data')
            plt.plot(X, y_pred, color='red', label=f'Polynomial degree {degree}')
            plt.xlabel(independent_var)
            plt.ylabel(dependent_var)
            plt.title(f'Polynomial Regression of degree {degree}')
            plt.legend()
            st.pyplot(plt)
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

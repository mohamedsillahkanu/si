import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# App title
st.title("Interactive Machine Learning Model Training: Linear Regression")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Linear Regression Overview", "Train Linear Regression Model"])

# 1. Linear Regression Overview Section
if section == "Linear Regression Overview":
    st.header("Linear Regression for Predictive Analysis")
    
    st.subheader("When to Use It")
    st.write("""
        Linear Regression is a linear approach for modeling the relationship between a dependent variable and one or more independent variables.
        It is commonly used for predicting outcomes and understanding the relationships between variables.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using Linear Regression:")
    st.write("1. **One or More Independent Variables**: The features that are used to predict the target.")
    st.write("2. **One Dependent Variable**: The target variable that you want to predict.")
    
    st.subheader("Purpose of Linear Regression")
    st.write("""
        The purpose of Linear Regression is to predict the value of a dependent variable based on the values of one or more independent variables.
        It is often used to identify relationships and trends in the data.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Linear Regression](https://en.wikipedia.org/wiki/Linear_regression).")

# 2. Train Linear Regression Model Section
elif section == "Train Linear Regression Model":
    st.header("Train Linear Regression Model")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="linear_regression_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the relevant columns
            feature_columns = st.multiselect("Select the feature columns", df.columns)
            target_column = st.selectbox("Select the target column", df.columns)
            
            if feature_columns and target_column:
                # Train Linear Regression model
                X = df[feature_columns]
                y = df[target_column]
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = LinearRegression()
                model.fit(X_train, y_train)
                
                # Save model to file
                model_file_path = "linear_regression_model.pkl"
                joblib.dump(model, model_file_path)
                
                st.success("Model trained successfully!")
                st.write(f"The trained model has been saved as `{model_file_path}`.")
                
                # Display model coefficients
                st.subheader("Model Coefficients")
                st.write(f"Intercept: {model.intercept_}")
                st.write(f"Coefficients: {model.coef_}")
                
                # Display Variable Importance Plot
                st.subheader("Variable Importance Plot")
                importance = pd.Series(model.coef_, index=feature_columns).sort_values()
                plt.figure(figsize=(8, 5))
                sns.barplot(x=importance, y=importance.index, palette='viridis')
                plt.title('Variable Importance (Coefficients)')
                plt.xlabel('Coefficient Value')
                plt.ylabel('Features')
                st.pyplot(plt)
                
                # Display Scatter Plot of Predictions vs Actual
                st.subheader("Scatter Plot of Predictions vs Actual Values")
                y_pred = model.predict(X_test)
                plt.figure(figsize=(8, 5))
                sns.scatterplot(x=y_test, y=y_pred)
                plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--', label='Ideal Fit')
                plt.xlabel('Actual Values')
                plt.ylabel('Predicted Values')
                plt.title('Predicted vs Actual Values')
                plt.legend()
                st.pyplot(plt)
                
            else:
                st.warning("Please select at least one feature column and one target column.")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")


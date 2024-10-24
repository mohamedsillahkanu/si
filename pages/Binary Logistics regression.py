import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_curve, auc, confusion_matrix, accuracy_score
import joblib

# App title
st.title("Interactive Machine Learning Model Training: Binary Logistic Regression")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Logistic Regression Overview", "Train Logistic Regression Model"])

# 1. Logistic Regression Overview Section
if section == "Logistic Regression Overview":
    st.header("Logistic Regression for Binary Classification")
    
    st.subheader("When to Use It")
    st.write("""
        Logistic Regression is used to model the probability of a binary outcome based on one or more independent variables.
        It is commonly used for classification tasks where the target variable has two possible outcomes.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using Logistic Regression:")
    st.write("1. **One or More Independent Variables**: The features that are used to predict the target.")
    st.write("2. **One Binary Dependent Variable**: The target variable that you want to classify (0 or 1).")
    
    st.subheader("Purpose of Logistic Regression")
    st.write("""
        The purpose of Logistic Regression is to predict the probability of a binary outcome based on the values of one or more independent variables.
        It is often used in medical, financial, and social sciences to determine the likelihood of an event occurring.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Logistic Regression](https://en.wikipedia.org/wiki/Logistic_regression).")

# 2. Train Logistic Regression Model Section
elif section == "Train Logistic Regression Model":
    st.header("Train Logistic Regression Model")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="logistic_regression_file")
    
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
                # Train Logistic Regression model
                X = df[feature_columns]
                y = df[target_column]
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = LogisticRegression()
                model.fit(X_train, y_train)
                
                # Save model to file
                model_file_path = "logistic_regression_model.pkl"
                joblib.dump(model, model_file_path)
                
                st.success("Model trained successfully!")
                st.write(f"The trained model has been saved as `{model_file_path}`.")
                
                # Display training and testing accuracy
                train_accuracy = accuracy_score(y_train, model.predict(X_train))
                test_accuracy = accuracy_score(y_test, model.predict(X_test))
                st.subheader("Model Accuracy")
                st.write(f"Training Accuracy: {train_accuracy:.2f}")
                st.write(f"Testing Accuracy: {test_accuracy:.2f}")
                
                # Display Classification Report
                st.subheader("Classification Report")
                y_pred = model.predict(X_test)
                report = classification_report(y_test, y_pred, output_dict=True)
                st.write(pd.DataFrame(report).transpose())
                
                # Display Confusion Matrix
                st.subheader("Confusion Matrix")
                cm = confusion_matrix(y_test, y_pred)
                plt.figure(figsize=(8, 6))
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
                plt.xlabel('Predicted Label')
                plt.ylabel('True Label')
                plt.title('Confusion Matrix')
                st.pyplot(plt)
                
                # Display ROC Curve
                st.subheader("ROC Curve")
                y_prob = model.predict_proba(X_test)[:, 1]
                fpr, tpr, _ = roc_curve(y_test, y_prob)
                roc_auc = auc(fpr, tpr)
                plt.figure(figsize=(8, 6))
                plt.plot(fpr, tpr, color='blue', label=f'ROC Curve (AUC = {roc_auc:.2f})')
                plt.plot([0, 1], [0, 1], color='red', linestyle='--')
                plt.xlabel('False Positive Rate')
                plt.ylabel('True Positive Rate')
                plt.title('Receiver Operating Characteristic (ROC) Curve')
                plt.legend()
                st.pyplot(plt)
                
            else:
                st.warning("Please select at least one feature column and one target column.")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



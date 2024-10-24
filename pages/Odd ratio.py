import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm

# App title
st.title("Odds Ratios Analysis with Multiple Intervention Points")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Odds Ratios Overview", "Odds Ratios Illustration"])

# 1. Odds Ratios Overview Section
if section == "Odds Ratios Overview":
    st.header("Odds Ratios for Causal Inference")
    
    st.subheader("When to Use It")
    st.write("""
        Odds ratios are used in statistics to quantify the strength of the association between two events, typically in case-control studies or logistic regression.
        They help determine the likelihood that a particular outcome will occur, given the presence of certain factors or interventions.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using Odds Ratios:")
    st.write("1. **Categorical Variables**: Predictor variables that can be used to calculate the odds of an outcome occurring.")
    st.write("2. **Outcome Variable**: A binary variable representing the occurrence or non-occurrence of an event.")
    
    st.subheader("Purpose of Odds Ratios")
    st.write("""
        The purpose of calculating Odds Ratios is to evaluate the strength of the association between predictors and outcomes. 
        An odds ratio greater than 1 indicates an increased likelihood of the outcome occurring, while an odds ratio less than 1 indicates a decreased likelihood.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Odds Ratio](https://en.wikipedia.org/wiki/Odds_ratio).")

# 2. Odds Ratios Illustration Section
elif section == "Odds Ratios Illustration":
    st.header("Odds Ratios Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="or_file")
    
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
            predictor_columns = st.multiselect("Select the predictor columns", df.columns)
            outcome_column = st.selectbox("Select the outcome column (binary variable)", df.columns)
            
            # Prepare the model data
            X = df[predictor_columns]
            X = sm.add_constant(X)
            y = df[outcome_column]
            model = sm.Logit(y, X).fit()
            
            # Display the regression results
            st.subheader("Regression Results")
            st.write(model.summary())
            
            # Calculate and display odds ratios
            st.subheader("Odds Ratios")
            odds_ratios = np.exp(model.params)
            st.write(odds_ratios)
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



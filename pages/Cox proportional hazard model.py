import streamlit as st
import pandas as pd
import numpy as np
from lifelines import CoxPHFitter
import matplotlib.pyplot as plt

# App title
st.title("Cox Proportional Hazards Model for Survival Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Cox Model Overview", "Cox Model Illustration"])

# 1. Cox Model Overview Section
if section == "Cox Model Overview":
    st.header("Cox Proportional Hazards Model for Survival Analysis")
    
    st.subheader("When to Use It")
    st.write("""
        The Cox Proportional Hazards Model is a semi-parametric model used to evaluate the effect of several variables on survival time. 
        It is commonly used in medical research to assess the impact of factors such as treatment, demographic information, or comorbidities on patient survival.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following variables for the Cox Model:")
    st.write("1. **Time to Event**: The time duration until the event occurs (e.g., death, relapse).")
    st.write("2. **Event Occurrence**: A binary variable indicating whether the event occurred (1 for event, 0 for censored).")
    st.write("3. **Covariates**: Variables that may affect the survival outcome (e.g., age, treatment, comorbidities).")
    
    st.subheader("Purpose of the Model")
    st.write("""
        The purpose of the Cox Proportional Hazards Model is to determine the effect of several variables on the risk of an event occurring. 
        It estimates the hazard ratio for each covariate, which describes how the hazard changes as the covariate value changes.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how the Cox Proportional Hazards Model can be used in malaria research:")
    
    st.write("""
    1. **Assessing the Effect of Treatment on Survival**: 
       Researchers can use the Cox model to assess the effect of different antimalarial treatments on patient survival time.
    """)
    
    st.write("""
    2. **Evaluating the Impact of Age and Comorbidities**: 
       The model can be used to evaluate the impact of patient age and comorbidities on the likelihood of relapse or death.
    """)
    
    st.write("For more information, visit the [Wikipedia page on the Cox Proportional Hazards Model](https://en.wikipedia.org/wiki/Cox_proportional_hazards_model).")

# 2. Cox Model Illustration Section
elif section == "Cox Model Illustration":
    st.header("Cox Proportional Hazards Model Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="cox_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the required columns
            time_column = st.selectbox("Select the time to event variable", df.columns)
            event_column = st.selectbox("Select the event occurrence variable", df.columns)
            covariate_columns = st.multiselect("Select the covariate variables", [col for col in df.columns if col not in [time_column, event_column]])
            
            st.write(f"You selected: {time_column}, {event_column}, and covariates: {covariate_columns} for the Cox Model.")
            
            # Button to fit the Cox model
            if st.button("Fit Cox Proportional Hazards Model"):
                # Prepare the dataset
                cph = CoxPHFitter()
                df_cox = df[[time_column, event_column] + covariate_columns]
                df_cox = df_cox.dropna()  # Drop missing values
                
                # Fit the Cox Proportional Hazards model
                cph.fit(df_cox, duration_col=time_column, event_col=event_column)
                
                # Display the summary of the Cox model
                st.write("Cox Proportional Hazards Model Summary:")
                st.text(cph.summary)
                
                # Plot the coefficients
                st.write("Coefficient Plot:")
                plt.figure(figsize=(10, 6))
                cph.plot()
                st.pyplot(plt)
                
                # Display a tip for interpretation
                st.write("""
                **Tip for Interpretation**: 
                - The Cox model estimates the hazard ratio for each covariate. A hazard ratio greater than 1 indicates increased risk, while a hazard ratio less than 1 indicates decreased risk.
                - The p-value associated with each covariate indicates whether its effect on the hazard is statistically significant.
                """)
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



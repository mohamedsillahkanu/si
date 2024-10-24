import streamlit as st
import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter

# App title
st.title("Kaplan-Meier Estimator for Survival Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Kaplan-Meier Overview", "Kaplan-Meier Illustration"])

# 1. Kaplan-Meier Overview Section
if section == "Kaplan-Meier Overview":
    st.header("Kaplan-Meier Estimator for Survival Analysis")
    
    st.subheader("When to Use It")
    st.write("""
        The Kaplan-Meier Estimator is a non-parametric statistic used to estimate the survival function from lifetime data. 
        It is often used in medical research to measure the fraction of patients living for a certain amount of time after treatment.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need two variables for the Kaplan-Meier Estimator:")
    st.write("1. **Time to Event**: The time duration until the event occurs (e.g., death, relapse).")
    st.write("2. **Event Occurrence**: A binary variable indicating whether the event occurred (1 for event, 0 for censored).")
    
    st.subheader("Purpose of the Estimator")
    st.write("""
        The purpose of the Kaplan-Meier Estimator is to estimate the survival probability over time, taking into account 
        the censored data (i.e., subjects for whom the event has not occurred by the end of the study).
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how the Kaplan-Meier Estimator can be used in malaria research:")
    
    st.write("""
    1. **Survival Time After Malaria Treatment**: 
       Researchers can use the Kaplan-Meier Estimator to estimate the survival time of patients after receiving antimalarial treatment.
    """)
    
    st.write("""
    2. **Time to Relapse After Treatment**: 
       The estimator can be used to evaluate the time to relapse for patients treated for malaria, considering some patients may not relapse during the study.
    """)
    
    st.write("For more information, visit the [Wikipedia page on the Kaplan-Meier Estimator](https://en.wikipedia.org/wiki/Kaplan%E2%80%93Meier_estimator).")

# 2. Kaplan-Meier Illustration Section
elif section == "Kaplan-Meier Illustration":
    st.header("Kaplan-Meier Estimator Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="km_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the time and event columns
            time_column = st.selectbox("Select the time to event variable", df.columns)
            event_column = st.selectbox("Select the event occurrence variable", df.columns)
            
            st.write(f"You selected: {time_column} and {event_column} for the Kaplan-Meier Estimator.")
            
            # Add radio buttons for Kaplan-Meier analysis options
            analysis_option = st.radio("Choose an analysis option:", ["See Python code", "Use Kaplan-Meier Estimator"])
            
            if analysis_option == "See Python code":
                st.code("""
from lifelines import KaplanMeierFitter

# Fit the Kaplan-Meier Estimator
kmf = KaplanMeierFitter()
kmf.fit(df[time_column], event_observed=df[event_column])

# Plot the survival function
kmf.plot()
                """, language='python')
            elif analysis_option == "Use Kaplan-Meier Estimator":
                # Fit the Kaplan-Meier Estimator
                kmf = KaplanMeierFitter()
                kmf.fit(df[time_column], event_observed=df[event_column])
                
                # Plot the survival function
                st.write("Kaplan-Meier Survival Curve:")
                kmf_plot = kmf.plot()
                st.pyplot(kmf_plot.figure)
                
        except Exception as e:
            st.error(f"Error loading file: {e}")

# requirements.txt content
requirements_txt = """
streamlit
pandas
numpy
lifelines
matplotlib
"""
with open('requirements.txt', 'w') as f:
    f.write(requirements_txt)

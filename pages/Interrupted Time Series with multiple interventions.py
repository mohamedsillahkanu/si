import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# App title
st.title("Interrupted Time Series Analysis with Multiple Intervention Points")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Interrupted Time Series Overview", "Interrupted Time Series Illustration"])

# 1. Interrupted Time Series Overview Section
if section == "Interrupted Time Series Overview":
    st.header("Interrupted Time Series Analysis for Causal Inference")
    
    st.subheader("When to Use It")
    st.write("""
        Interrupted Time Series (ITS) analysis is a quasi-experimental design used to evaluate the impact of multiple interventions or policy changes
        by analyzing the changes in a time series before and after each intervention.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using the Interrupted Time Series method:")
    st.write("1. **Time Series Data**: A continuous set of observations taken over time, with clear points of intervention.")
    st.write("2. **Intervention Times**: Clear points in time when each intervention or policy change occurred.")
    
    st.subheader("Purpose of the Interrupted Time Series Method")
    st.write("""
        The purpose of Interrupted Time Series analysis is to evaluate the causal effect of multiple interventions by comparing the trends before and after each intervention.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here is a practical example of how Interrupted Time Series analysis can be used in malaria research:")
    
    st.write("""
    **Evaluating the Impact of Multiple Malaria Interventions**: 
       Researchers can use ITS to evaluate the impact of multiple malaria interventions, such as insecticide-treated nets (ITNs), medicine distribution, and awareness campaigns, by analyzing malaria incidence rates before and after each intervention.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Interrupted Time Series](https://en.wikipedia.org/wiki/Interrupted_time_series_design).")

# 2. Interrupted Time Series Illustration Section
elif section == "Interrupted Time Series Illustration":
    st.header("Interrupted Time Series Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="its_file")
    
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
            time_column = st.selectbox("Select the time column", df.columns)
            outcome_column = st.selectbox("Select the outcome column (e.g., malaria cases)", df.columns)
            intervention_points = st.multiselect("Enter the time points of interventions (e.g., month numbers)", options=list(range(len(df))))
            
            # Create intervention dummy variables for each intervention point
            for i, point in enumerate(intervention_points):
                df[f'intervention_{i+1}'] = (df[time_column] >= point).astype(int)
                df[f'time_after_intervention_{i+1}'] = df['time'] * df[f'intervention_{i+1}']
            
            # Prepare the model data
            X = df[['time'] + [f'intervention_{i+1}' for i in range(len(intervention_points))] + [f'time_after_intervention_{i+1}' for i in range(len(intervention_points))]]
            X = sm.add_constant(X)
            y = df[outcome_column]
            model = sm.OLS(y, X).fit()
            
            # Display the regression results
            st.subheader("Regression Results")
            st.write(model.summary())
            
            # Plot the outcome before and after each intervention
            st.subheader("Interrupted Time Series Plot")
            plt.figure(figsize=(10, 6))
            plt.plot(df[time_column], df[outcome_column], label='Observed Data', color='blue')
            for i, point in enumerate(intervention_points):
                plt.axvline(x=point, color='red', linestyle='--', label=f'Intervention {i+1}')
            plt.xlabel('Time')
            plt.ylabel(outcome_column)
            plt.title('Interrupted Time Series Analysis with Multiple Interventions')
            plt.legend()
            st.pyplot(plt)
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



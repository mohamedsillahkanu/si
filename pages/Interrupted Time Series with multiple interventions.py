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
            intervention_dates = st.multiselect("Enter the intervention dates (Year-Month format, e.g., 2023-05)", options=pd.to_datetime(df[time_column]).dt.to_period('M').astype(str).unique())
            intervention_types = []
            for i, date in enumerate(intervention_dates):
                intervention_type = st.text_input(f"Enter the type of intervention for {date}")
                intervention_types.append(intervention_type)
            
            # Convert the time column to datetime and set as index
            df[time_column] = pd.to_datetime(df[time_column])
            df.set_index(time_column, inplace=True)
            
            # Create intervention dummy variables for each intervention point
            for i, date in enumerate(intervention_dates):
                intervention_date = pd.to_datetime(date)
                df[f'intervention_{i+1}'] = (df.index >= intervention_date).astype(int)
                df[f'time_after_intervention_{i+1}'] = (df.index - intervention_date).days
                df[f'time_after_intervention_{i+1}'] = df[f'time_after_intervention_{i+1}'].apply(lambda x: max(0, x))
            
            # Prepare the model data
            X = df[['intervention_' + str(i+1) for i in range(len(intervention_dates))] + ['time_after_intervention_' + str(i+1) for i in range(len(intervention_dates))]]
            X = sm.add_constant(X)
            y = df[outcome_column]
            model = sm.OLS(y, X).fit()
            
            # Display the regression results
            st.subheader("Regression Results")
            st.write(model.summary())
            
            # Plot the outcome before and after each intervention
            st.subheader("Interrupted Time Series Plot")
            plt.figure(figsize=(10, 6))
            plt.plot(df.index, df[outcome_column], label='Observed Data', color='blue')
            for i, date in enumerate(intervention_dates):
                intervention_date = pd.to_datetime(date)
                plt.axvline(x=intervention_date, color='red', linestyle='--', label=f'Intervention {i+1}: {intervention_types[i]}')
            plt.xlabel('Time')
            plt.ylabel(outcome_column)
            plt.title('Interrupted Time Series Analysis with Multiple Interventions')
            plt.legend()
            st.pyplot(plt)
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



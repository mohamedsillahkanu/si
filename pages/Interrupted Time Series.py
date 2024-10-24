import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# App title
st.title("Interrupted Time Series Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Interrupted Time Series Overview", "Interrupted Time Series Illustration"])

# 1. Interrupted Time Series Overview Section
if section == "Interrupted Time Series Overview":
    st.header("Interrupted Time Series Analysis for Causal Inference")
    
    st.subheader("When to Use It")
    st.write("""
        Interrupted Time Series (ITS) analysis is a quasi-experimental design used to evaluate the impact of an intervention or policy change
        by analyzing the changes in a time series before and after the intervention.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using the Interrupted Time Series method:")
    st.write("1. **Time Series Data**: A continuous set of observations taken over time, with a clear point of intervention.")
    st.write("2. **Intervention Time**: A clear point in time when the intervention or policy change occurred.")
    
    st.subheader("Purpose of the Interrupted Time Series Method")
    st.write("""
        The purpose of Interrupted Time Series analysis is to evaluate the causal effect of an intervention by comparing the trends before and after the intervention.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here is a practical example of how Interrupted Time Series analysis can be used in malaria research:")
    
    st.write("""
    **Evaluating the Impact of a New Malaria Prevention Campaign**: 
       Researchers can use ITS to evaluate the impact of a new malaria prevention campaign by analyzing malaria incidence rates before and after the campaign.
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
            intervention_point = st.number_input("Enter the time point of intervention (e.g., month number)", min_value=0, max_value=len(df)-1)
            
            # Create an intervention dummy variable
            df['intervention'] = (df[time_column] >= intervention_point).astype(int)
            df['time'] = range(len(df))
            df['time_after_intervention'] = df['time'] * df['intervention']
            
            # Fit the Interrupted Time Series model
            X = df[['time', 'intervention', 'time_after_intervention']]
            X = sm.add_constant(X)
            y = df[outcome_column]
            model = sm.OLS(y, X).fit()
            
            # Display the regression results
            st.subheader("Regression Results")
            st.write(model.summary())
            
            # Plot the outcome before and after the intervention
            st.subheader("Interrupted Time Series Plot")
            plt.figure(figsize=(10, 6))
            plt.plot(df[time_column], df[outcome_column], label='Observed Data', color='blue')
            plt.axvline(x=intervention_point, color='red', linestyle='--', label='Intervention Point')
            plt.xlabel('Time')
            plt.ylabel(outcome_column)
            plt.title('Interrupted Time Series Analysis')
            plt.legend()
            st.pyplot(plt)
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



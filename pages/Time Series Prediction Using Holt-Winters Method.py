import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt

# App title
st.title("Time Series Prediction Using Holt-Winters Method")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Holt-Winters Method")
    
    st.subheader("When to Use It")
    st.write("""
        The Holt-Winters method is used for forecasting time series data that displays 
        both a trend and seasonality. It is particularly effective for seasonal data.
    """)
    
    st.subheader("Components of the Holt-Winters Method")
    st.write("""
        The method consists of three components:
        - Level: The average value of the series.
        - Trend: The increasing or decreasing value in the series.
        - Seasonal: The repeating fluctuations in the series.
    """)
    
    st.subheader("Purpose of the Method")
    st.write("""
        The purpose of the Holt-Winters method is to produce forecasts based on historical data, 
        allowing for the incorporation of trends and seasonal patterns in the predictions.
    """)
    
    st.subheader("Real-Life Medical Examples")
    st.write("Here are two practical examples of how this method can be used in the field of medicine:")
    
    st.write("""
    1. **Hospital Admissions**: 
        Hospitals can forecast the number of patient admissions based on historical data, taking into account seasonal trends (e.g., flu season).
    """)
    
    st.write("""
    2. **Medication Demand**: 
        Pharmacies can predict the demand for certain medications, allowing them to maintain appropriate stock levels throughout the year.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Time Series Prediction Using Holt-Winters Method")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)

            st.write("Here is a preview of your data:")
            st.write(df.head())

            # Assume the time series data has a datetime index
            date_column = st.selectbox("Select the date column", df.columns)
            value_column = st.selectbox("Select the value column", df.columns)

            df[date_column] = pd.to_datetime(df[date_column])
            df.set_index(date_column, inplace=True)

            # Forecasting period
            forecast_period = st.number_input("Enter the number of periods to forecast", min_value=1, value=12)

            # Apply Holt-Winters Exponential Smoothing
            if st.button("Run Holt-Winters Forecast"):
                model = ExponentialSmoothing(df[value_column], 
                                              seasonal='add', 
                                              seasonal_periods=12).fit()
                forecast = model.forecast(forecast_period)

                # Plot the results
                plt.figure(figsize=(10, 6))
                plt.plot(df[value_column], label='Observed', color='blue')
                plt.plot(forecast, label='Forecast', color='orange', linestyle='--')
                plt.title('Holt-Winters Forecast')
                plt.xlabel('Date')
                plt.ylabel('Values')
                plt.legend()
                st.pyplot(plt)

                st.write("Forecasted Values:")
                st.write(forecast)
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

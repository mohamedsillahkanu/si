import streamlit as st
import pandas as pd
import numpy as np
from pmdarima import auto_arima
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

# App title
st.title("Time Series Analysis using SARIMAX Model")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["SARIMAX Overview", "SARIMAX Illustration"])

# 1. SARIMAX Overview Section
if section == "SARIMAX Overview":
    st.header("SARIMAX Model for Time Series Forecasting")
    
    st.subheader("When to Use It")
    st.write("""
        The SARIMAX (Seasonal AutoRegressive Integrated Moving Average with eXogenous regressors) model is used for time series forecasting when data exhibits non-stationarity, trend, and seasonality.
        It is widely used for forecasting future values in areas such as finance, economics, and environmental sciences.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using the SARIMAX model:")
    st.write("1. **Time Series Data**: Historical data with a clear time order, which may include trends, seasonality, and autocorrelation.")
    
    st.subheader("Purpose of the SARIMAX Model")
    st.write("""
        The purpose of the SARIMAX model is to provide accurate forecasts for time series data by modeling autoregressive, moving average, and seasonal components,
        along with differencing to make the data stationary. The model can also handle exogenous variables if needed.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here is a practical example of how the SARIMAX model can be used in malaria research:")
    
    st.write("""
    **Forecasting Malaria Cases**: 
       Researchers can use the SARIMAX model to forecast the number of malaria cases over time based on past trends, seasonality, and other contributing factors.
    """)
    
    st.write("For more information, visit the [Wikipedia page on ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average).")

# 2. SARIMAX Illustration Section
elif section == "SARIMAX Illustration":
    st.header("SARIMAX Model Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="sarimax_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the time series column
            time_column = st.selectbox("Select the time column", df.columns)
            value_column = st.selectbox("Select the value column (time series data)", df.columns)
            
            # Convert the time column to datetime and set as index
            df[time_column] = pd.to_datetime(df[time_column])
            df.set_index(time_column, inplace=True)
            
            # Check for stationarity
            st.write("Checking stationarity of the data using Augmented Dickey-Fuller test...")
            adf_result = adfuller(df[value_column])
            if adf_result[1] > 0.05:
                st.write("The data is non-stationary (p-value > 0.05). Differencing will be applied to make it stationary.")
                df[value_column] = df[value_column].diff().dropna()
            else:
                st.write("The data is stationary (p-value <= 0.05). Proceeding with SARIMAX modeling.")
            
            # Button to apply SARIMAX model
            if st.button("Apply SARIMAX Model"):
                try:
                    # Use auto_arima to determine the best parameters for SARIMAX
                    st.write("Determining the best SARIMAX parameters using auto_arima...")
                    model_auto = auto_arima(df[value_column], seasonal=True, m=12, trace=True, error_action='ignore', suppress_warnings=True, stepwise=True)
                    p, d, q = model_auto.order
                    P, D, Q, m = model_auto.seasonal_order
                    
                    # Fit the SARIMAX model with the best parameters
                    model = SARIMAX(df[value_column], order=(p, d, q), seasonal_order=(P, D, Q, m))
                    model_fit = model.fit(disp=False)
                    df['Fitted'] = model_fit.fittedvalues
                    forecast = model_fit.get_forecast(steps=12)
                    forecast_ci = forecast.conf_int()
                    forecast_index = pd.date_range(df.index[-1], periods=12, freq='M')
                    
                    # Plot the original time series, fitted values, and forecast with confidence intervals
                    st.write("**SARIMAX Forecast**:")
                    plt.figure(figsize=(12, 6))
                    plt.plot(df.index, df[value_column], label='Original Data', color='blue')
                    plt.plot(df.index, df['Fitted'], label='Fitted Values', color='orange')
                    plt.plot(forecast_index, forecast.predicted_mean, label='Forecast', color='green')
                    plt.fill_between(forecast_index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='green', alpha=0.2)
                    plt.xlabel('Time')
                    plt.ylabel(value_column)
                    plt.title('SARIMAX Forecasting with Confidence Intervals')
                    plt.legend()
                    st.pyplot(plt)
                    
                except Exception as e:
                    st.error(f"Error during SARIMAX Model: {e}")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



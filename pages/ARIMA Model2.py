import streamlit as st
import pandas as pd
import numpy as np
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# App title
st.title("Time Series Analysis using Improved ARIMA Model")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["ARIMA Overview", "ARIMA Illustration"])

# 1. ARIMA Overview Section
if section == "ARIMA Overview":
    st.header("ARIMA Model for Time Series Forecasting")
    
    st.subheader("When to Use It")
    st.write("""
        The ARIMA (AutoRegressive Integrated Moving Average) model is used for time series forecasting when data exhibits non-stationarity and autocorrelation.
        It is widely used for forecasting future values in areas such as finance, economics, and environmental sciences.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using the ARIMA model:")
    st.write("1. **Time Series Data**: Historical data with a clear time order, which may include trends and autocorrelation.")
    
    st.subheader("Purpose of the ARIMA Model")
    st.write("""
        The purpose of the ARIMA model is to provide accurate forecasts for time series data by modeling both the autoregressive and moving average components,
        along with differencing to make the data stationary.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here is a practical example of how the ARIMA model can be used in malaria research:")
    
    st.write("""
    **Forecasting Malaria Cases**: 
       Researchers can use the ARIMA model to forecast the number of malaria cases over time based on past trends and autocorrelation.
    """)
    
    st.write("For more information, visit the [Wikipedia page on ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average).")

# 2. ARIMA Illustration Section
elif section == "ARIMA Illustration":
    st.header("ARIMA Model Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="arima_file")
    
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
            
            # Button to apply ARIMA model
            if st.button("Apply Improved ARIMA Model"):
                try:
                    # Use auto_arima to determine the best parameters for ARIMA
                    st.write("Determining the best ARIMA parameters using auto_arima...")
                    model_auto = auto_arima(df[value_column], seasonal=False, trace=True, error_action='ignore', suppress_warnings=True, stepwise=True)
                    p, d, q = model_auto.order
                    
                    # Fit the ARIMA model with the best parameters
                    model = ARIMA(df[value_column], order=(p, d, q))
                    model_fit = model.fit()
                    df['Fitted'] = model_fit.fittedvalues
                    forecast = model_fit.get_forecast(steps=12)
                    forecast_ci = forecast.conf_int()
                    forecast_index = pd.date_range(df.index[-1], periods=13, freq='M')[1:]
                    
                    # Plot the original time series, fitted values, and forecast with confidence intervals
                    st.write("**Improved ARIMA Forecast**:")
                    plt.figure(figsize=(12, 6))
                    plt.plot(df.index, df[value_column], label='Original Data', color='blue')
                    plt.plot(df.index, df['Fitted'], label='Fitted Values', color='orange')
                    plt.plot(forecast_index, forecast.predicted_mean, label='Forecast', color='green')
                    plt.fill_between(forecast_index, forecast_ci.iloc[:, 0], forecast_ci.iloc[:, 1], color='green', alpha=0.2)
                    plt.xlabel('Time')
                    plt.ylabel(value_column)
                    plt.title('Improved ARIMA Forecasting with Confidence Intervals')
                    plt.legend()
                    st.pyplot(plt)
                    
                except Exception as e:
                    st.error(f"Error during ARIMA Model: {e}")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



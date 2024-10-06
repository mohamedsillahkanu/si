import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Function to check stationarity
def test_stationarity(timeseries):
    result = adfuller(timeseries)
    return result[1]  # Return the p-value

# Function to apply differencing if not stationary
def apply_differencing(timeseries):
    d = 0
    while test_stationarity(timeseries) > 0.05 and d < 5:  # Apply differencing up to 5 times
        timeseries = timeseries.diff().dropna()
        d += 1
    return timeseries, d

# App title
st.title("Time Series Prediction Using ARIMA")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: ARIMA Model")
    st.write("Overview of ARIMA model...")

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Time Series Prediction Using ARIMA")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)

            st.write("Here is a preview of your data:")
            st.write(df.head())

            # Select date and value columns
            date_column = st.selectbox("Select the date column", df.columns)
            value_column = st.selectbox("Select the value column", df.columns)

            df[date_column] = pd.to_datetime(df[date_column])
            df.set_index(date_column, inplace=True)

            # Resample to monthly data if not already
            df = df.resample('M').sum()

            # Check for missing values
            if df[value_column].isnull().any():
                st.warning("There are missing values in the selected value column. Please handle them before forecasting.")
            else:
                # Test for stationarity and apply differencing if necessary
                st.write(f"Testing for stationarity on {value_column}...")
                p_value = test_stationarity(df[value_column])

                if p_value < 0.05:
                    st.success("The time series is stationary. Proceeding with ARIMA.")
                    differenced_series, d = df[value_column], 0  # No differencing required
                else:
                    st.warning("The time series is not stationary. Applying differencing...")
                    differenced_series, d = apply_differencing(df[value_column])
                    st.write(f"Differencing applied {d} time(s).")

                # Define forecast period
                forecast_period = st.number_input("Select the forecast period (number of months to forecast)", min_value=1, value=5)

                if st.button("Run ARIMA Forecast"):
                    # Define ARIMA parameters
                    p = st.number_input("Select the value for p (AR term)", min_value=0, value=1)
                    q = st.number_input("Select the value for q (MA term)", min_value=0, value=1)

                    # Fit the ARIMA model
                    try:
                        model = ARIMA(differenced_series, order=(p, d, q))
                        model_fit = model.fit()

                        # Forecast the values
                        forecast = model_fit.get_forecast(steps=forecast_period)
                        forecast_values = forecast.predicted_mean
                        forecast_index = pd.date_range(start=differenced_series.index[-1] + pd.DateOffset(months=1), 
                                                        periods=forecast_period, freq='M')
                        forecast_df = pd.DataFrame(forecast_values, index=forecast_index, columns=['Forecast'])

                        # Confidence intervals
                        conf_int = forecast.conf_int()
                        lower_conf = conf_int.iloc[:, 0]
                        upper_conf = conf_int.iloc[:, 1]

                        # Plot the results
                        plt.figure(figsize=(12, 6))
                        plt.plot(df[value_column], label='Observed', color='blue', marker='o')
                        plt.plot(forecast_df.index, forecast_df['Forecast'], label='Forecast', color='red', linestyle='--', marker='x')
                        plt.fill_between(forecast_df.index, lower_conf, upper_conf, color='pink', alpha=0.3, label='Confidence Interval')
                        plt.title('ARIMA Forecast')
                        plt.xlabel('Date')
                        plt.ylabel('Values')
                        plt.legend()
                        plt.xticks(rotation=45)
                        st.pyplot(plt)

                        st.write("Forecast Values:")
                        st.write(forecast_df)

                    except Exception as e:
                        st.error(f"Error fitting the ARIMA model: {e}")

        except Exception as e:
            st.error(f"Error loading file: {e}")

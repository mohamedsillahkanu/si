import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# App title
st.title("Time Series Prediction Using ARIMA")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: ARIMA Model")
    
    st.subheader("When to Use It")
    st.write("""
        The ARIMA model is used for forecasting time series data by considering 
        its own past values, past errors, and a number of differences of the data.
    """)
    
    st.subheader("Components of the ARIMA Model")
    st.write("""
        The ARIMA model consists of three main components:
        - **AR (AutoRegressive)**: Uses the dependency between an observation and a number of lagged observations.
        - **I (Integrated)**: Uses differencing of raw observations to allow for the time series to become stationary.
        - **MA (Moving Average)**: Uses the dependency between an observation and a residual error from a moving average model applied to lagged observations.
    """)
    
    st.subheader("Purpose of the Method")
    st.write("""
        The ARIMA model is used to predict future points in the series by learning the relationships between observations.
    """)
    
    st.subheader("Real-Life Medical Examples")
    st.write("Here are two practical examples of how this method can be used in the field of medicine:")
    
    st.write("""
    1. **Patient Admission Forecasting**: 
        Hospitals can use ARIMA to forecast the number of patient admissions based on historical data.
    """)
    
    st.write("""
    2. **Disease Spread Prediction**: 
        Public health organizations can model the spread of diseases over time and use ARIMA for future incidence predictions.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Time Series Prediction Using ARIMA")
    
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

            # Resample to monthly data if not already
            df = df.resample('M').sum()

            # Define the forecast period in months
            forecast_period = st.number_input("Select the forecast period (number of months to forecast)", min_value=1, value=5)

            # Apply ARIMA
            if st.button("Run ARIMA Forecast"):
                # Define the order for ARIMA (p, d, q)
                p = st.number_input("Select the value for p (AR term)", min_value=0, value=1)
                d = st.number_input("Select the value for d (I term)", min_value=0, value=1)
                q = st.number_input("Select the value for q (MA term)", min_value=0, value=1)

                # Fit the ARIMA model
                model = ARIMA(df[value_column], order=(p, d, q))
                model_fit = model.fit()

                # Forecast the values
                forecast = model_fit.forecast(steps=forecast_period)

                # Create a DataFrame for the forecast values
                forecast_index = pd.date_range(start=df.index[-1] + pd.DateOffset(months=1), 
                                                periods=forecast_period, freq='M')
                forecast_df = pd.DataFrame(forecast, index=forecast_index, columns=['Forecast'])

                # Combine original data and forecast
                combined_df = pd.concat([df[value_column], forecast_df])

                # Plot the results
                plt.figure(figsize=(12, 6))
                plt.plot(df[value_column], label='Observed', color='blue', marker='o')
                plt.plot(forecast_df.index, forecast_df['Forecast'], label='Forecast', color='red', linestyle='--', marker='x')
                plt.title('ARIMA Forecast')
                plt.xlabel('Date')
                plt.ylabel('Values')
                plt.legend()
                plt.xticks(rotation=45)
                st.pyplot(plt)

                st.write("Forecast Values:")
                st.write(forecast_df)

        except Exception as e:
            st.error(f"Error loading file: {e}")

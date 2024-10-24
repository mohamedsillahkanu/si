import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt

# App title
st.title("Time Series Analysis using Holt-Winters Method")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Holt-Winters Overview", "Holt-Winters Illustration"])

# 1. Holt-Winters Overview Section
if section == "Holt-Winters Overview":
    st.header("Holt-Winters Method for Time Series Forecasting")
    
    st.subheader("When to Use It")
    st.write("""
        The Holt-Winters method is used for time series forecasting and is effective when data has trend and seasonality components.
        It is commonly used in many fields, including finance, inventory management, and environmental science, to forecast future values based on historical data.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using the Holt-Winters method:")
    st.write("1. **Time Series Data**: Historical data with a clear time order, containing trend and/or seasonality.")
    
    st.subheader("Purpose of the Holt-Winters Method")
    st.write("""
        The purpose of the Holt-Winters method is to provide accurate forecasts for time series data by accounting for trend and seasonality.
        It uses exponential smoothing to generate forecasts, making it suitable for data with repetitive patterns.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here is a practical example of how the Holt-Winters method can be used in malaria research:")
    
    st.write("""
    **Forecasting Malaria Cases**: 
       Researchers can use the Holt-Winters method to forecast the number of malaria cases in different seasons based on historical data.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Exponential Smoothing](https://en.wikipedia.org/wiki/Exponential_smoothing#Triple_exponential_smoothing).")

# 2. Holt-Winters Illustration Section
elif section == "Holt-Winters Illustration":
    st.header("Holt-Winters Method Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="holtwinters_file")
    
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
            
            # Button to apply Holt-Winters method
            if st.button("Apply Holt-Winters Method"):
                try:
                    # Fit the Holt-Winters model
                    model = ExponentialSmoothing(df[value_column], seasonal='add', trend='add', seasonal_periods=12).fit()
                    df['Forecast'] = model.fittedvalues
                    forecast = model.forecast(steps=12)
                    
                    # Plot the original time series and forecast
                    st.write("**Holt-Winters Forecast**:")
                    plt.figure(figsize=(12, 6))
                    plt.plot(df.index, df[value_column], label='Original Data', color='blue')
                    plt.plot(df.index, df['Forecast'], label='Fitted Values', color='orange')
                    plt.plot(pd.date_range(df.index[-1], periods=13, freq='M')[1:], forecast, label='Forecast', color='green')
                    plt.xlabel('Time')
                    plt.ylabel(value_column)
                    plt.title('Holt-Winters Forecasting')
                    plt.legend()
                    st.pyplot(plt)
                    
                except Exception as e:
                    st.error(f"Error during Holt-Winters Method: {e}")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# App title
st.title("Time Series Prediction Using Moving Average")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Moving Average")
    
    st.subheader("When to Use It")
    st.write("""
        The Moving Average method is used for smoothing time series data to identify 
        trends over time. It is particularly useful for removing noise and fluctuations 
        in the data.
    """)
    
    st.subheader("Components of the Moving Average Method")
    st.write("""
        The Moving Average method consists of calculating the average of a specific 
        number of previous observations to make predictions.
    """)
    
    st.subheader("Purpose of the Method")
    st.write("""
        The purpose of the Moving Average method is to provide a simplified view of 
        the data and to identify underlying trends more clearly, without the influence 
        of short-term fluctuations.
    """)
    
    st.subheader("Real-Life Medical Examples")
    st.write("Here are two practical examples of how this method can be used in the field of medicine:")
    
    st.write("""
    1. **Patient Monitoring**: 
        Hospitals can use moving averages to monitor patient vitals over time, 
        smoothing out sudden spikes or drops.
    """)
    
    st.write("""
    2. **Epidemiological Trends**: 
        Health organizations can track the incidence of diseases, such as malaria, 
        over time to identify trends and plan interventions accordingly.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Time Series Prediction Using Moving Average")
    
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

            # Define the moving average window size
            window_size = st.number_input("Select the moving average window size (in months)", min_value=1, value=3)

            # Define the forecast period in months
            forecast_period = st.number_input("Select the forecast period (number of months to forecast)", min_value=1, value=5)

            # Apply Moving Average
            if st.button("Run Moving Average Forecast"):
                moving_average = df[value_column].rolling(window=window_size).mean()

                # Prepare data for linear regression
                X = np.array(range(len(df))).reshape(-1, 1)  # Time variable (0, 1, 2, ...)
                y = df[value_column].values

                # Fit the linear regression model
                model = LinearRegression()
                model.fit(X, y)

                # Create future time points for forecasting
                future_X = np.array(range(len(df), len(df) + forecast_period)).reshape(-1, 1)

                # Predict future values
                future_values = model.predict(future_X)

                # Create a DataFrame for the forecast values
                forecast_index = pd.date_range(start=moving_average.index[-1] + pd.DateOffset(months=1), 
                                                periods=forecast_period, freq='M')
                forecast_df = pd.DataFrame(future_values, index=forecast_index, columns=['Forecast'])

                # Combine original data, moving average, and forecast
                combined_df = pd.concat([df[value_column], moving_average, forecast_df])

                # Plot the results
                plt.figure(figsize=(12, 6))
                plt.plot(df[value_column], label='Observed', color='blue', marker='o')
                plt.plot(moving_average.index, moving_average, label=f'Moving Average (window={window_size})', color='orange')
                plt.plot(forecast_df.index, forecast_df['Forecast'], label='Forecast', color='red', linestyle='--', marker='x')
                plt.title('Moving Average Forecast')
                plt.xlabel('Date')
                plt.ylabel('Values')
                plt.legend()
                plt.xticks(rotation=45)
                st.pyplot(plt)

                st.write("Moving Average Values:")
                st.write(moving_average)
                st.write("Forecast Values:")
                st.write(forecast_df)

        except Exception as e:
            st.error(f"Error loading file: {e}")

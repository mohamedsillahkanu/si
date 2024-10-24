import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# App title
st.title("Time Series Analysis using Moving Average")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Moving Average Overview", "Moving Average Illustration"])

# 1. Moving Average Overview Section
if section == "Moving Average Overview":
    st.header("Moving Average for Time Series Smoothing and Forecasting")
    
    st.subheader("When to Use It")
    st.write("""
        The Moving Average method is used for time series smoothing and is effective for identifying trends by removing short-term fluctuations.
        It can be used to forecast future values and make the data more interpretable.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using the Moving Average method:")
    st.write("1. **Time Series Data**: Historical data with a clear time order, containing trend and potential noise.")
    
    st.subheader("Purpose of the Moving Average Method")
    st.write("""
        The purpose of the Moving Average method is to provide a smoother representation of the time series data by averaging data points over a specified window.
        It helps in understanding the underlying trend by reducing noise.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here is a practical example of how the Moving Average method can be used in malaria research:")
    
    st.write("""
    **Identifying Trends in Malaria Cases**: 
       Researchers can use a Moving Average to smooth monthly malaria case counts and identify long-term trends over different seasons.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Moving Average](https://en.wikipedia.org/wiki/Moving_average).")

# 2. Moving Average Illustration Section
elif section == "Moving Average Illustration":
    st.header("Moving Average Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="moving_average_file")
    
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
            
            # Button to apply 3-month moving average
            if st.button("Apply 3-Month Moving Average"):
                try:
                    # Calculate 3-month moving average
                    df['3_Month_Moving_Avg'] = df[value_column].rolling(window=3).mean()
                    
                    # Plot the original time series and moving average
                    st.write("**3-Month Moving Average Smoothing**:")
                    plt.figure(figsize=(12, 6))
                    plt.plot(df.index, df[value_column], label='Original Data', color='blue')
                    plt.plot(df.index, df['3_Month_Moving_Avg'], label='3-Month Moving Average', color='orange')
                    plt.xlabel('Time')
                    plt.ylabel(value_column)
                    plt.title('3-Month Moving Average Smoothing')
                    plt.legend()
                    st.pyplot(plt)
                    
                except Exception as e:
                    st.error(f"Error during Moving Average calculation: {e}")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")

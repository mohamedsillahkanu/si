import streamlit as st
import geopandas as gpd
import rasterio
import rasterio.mask
import numpy as np
import os
import requests
import gzip
import shutil
import tempfile
from io import BytesIO
from matplotlib import pyplot as plt
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.model_selection import train_test_split

# Function to load and process the shapefile
def load_shapefile(shp_file, shx_file, dbf_file):
    with tempfile.TemporaryDirectory() as tmpdir:
        for file, ext in zip([shp_file, shx_file, dbf_file], ['.shp', '.shx', '.dbf']):
            with open(os.path.join(tmpdir, f"file{ext}"), "wb") as f:
                f.write(file.getbuffer())

        shapefile_path = os.path.join(tmpdir, "file.shp")
        gdf = gpd.read_file(shapefile_path)

    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")  # Assuming WGS84; replace with correct CRS if different

    return gdf

# Function to download, unzip, and process CHIRPS data
def process_chirps_data(gdf, year, month):
    link = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/africa_monthly/tifs/chirps-v2.0.{year}.{month:02d}.tif.gz"
    response = requests.get(link)
    with tempfile.TemporaryDirectory() as tmpdir:
        zipped_file_path = os.path.join(tmpdir, "chirps.tif.gz")
        unzipped_file_path = os.path.join(tmpdir, "chirps.tif")

        with open(zipped_file_path, "wb") as f:
            f.write(response.content)

        with gzip.open(zipped_file_path, "rb") as f_in:
            with open(unzipped_file_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        with rasterio.open(unzipped_file_path) as src:
            gdf = gdf.to_crs(src.crs)
            out_image, out_transform = rasterio.mask.mask(src, gdf.geometry, crop=True)
            mean_rains = []
            for geom in gdf.geometry:
                masked_data, _ = rasterio.mask.mask(src, [geom], crop=True)
                masked_data = masked_data.flatten()
                masked_data = masked_data[masked_data != src.nodata]
                mean_rains.append(masked_data.mean())

            gdf['mean_rain'] = mean_rains

    return gdf

# Streamlit app layout
st.title("CHIRPS Data Analysis and Holt-Winters Prediction")

# Upload shapefile components
uploaded_shp = st.file_uploader("Upload .shp file", type="shp")
uploaded_shx = st.file_uploader("Upload .shx file", type="shx")
uploaded_dbf = st.file_uploader("Upload .dbf file", type="dbf")

# Year and month selection
years = st.multiselect("Select Years", range(1981, 2025))
months = st.multiselect("Select Months", range(1, 13))

if uploaded_shp and uploaded_shx and uploaded_dbf and years and months:
    with st.spinner("Loading and processing shapefile..."):
        gdf = load_shapefile(uploaded_shp, uploaded_shx, uploaded_dbf)
    st.success("Shapefile loaded successfully!")

    all_data = []
    for year in years:
        for month in months:
            with st.spinner(f"Processing CHIRPS data for {year}-{month:02d}..."):
                df = process_chirps_data(gdf, year, month)
                df['Year'] = year
                df['Month'] = month
                all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)
    st.success("CHIRPS data processed successfully!")

    # Date processing
    combined_df['Date'] = pd.to_datetime(combined_df['Year'].astype(str) + '-' + combined_df['Month'].astype(str) + '-01')
    combined_df.set_index('Date', inplace=True)

    # Split the dataset into train and test sets
    train_set, test_set = train_test_split(combined_df, test_size=0.20, random_state=6313)
    train = train_set['mean_rain'].resample('M').sum()
    test = test_set['mean_rain'].resample('M').sum()

    train_diff = train.diff().dropna()
    test_diff = test.diff().dropna()

    # Fit the Holt-Winters model
    model = ExponentialSmoothing(train_diff, trend='add', seasonal='add', seasonal_periods=12)
    fit_model = model.fit()

    # User selection for forecast periods
    forecast_steps = st.slider("Select forecast periods (months)", min_value=1, max_value=24, value=12, step=1)

    # Forecast based on user-selected steps
    forecast = fit_model.forecast(steps=forecast_steps)

    # Generate a date range for the forecast period
    forecast_period = pd.date_range(start=test_diff.index[-1], periods=forecast_steps + 1, freq='M')[1:]
    forecast_series = pd.Series(forecast, index=forecast_period)

    # Plot the original data and the forecast
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(train_diff, label='Train data')
    ax.plot(test_diff, label='Test data')
    ax.plot(forecast_series, label=f'Forecast for {forecast_steps} periods')
    ax.set_title(f'Test Set vs Forecast ({forecast_steps} months)')
    ax.legend()
    st.pyplot(fig)

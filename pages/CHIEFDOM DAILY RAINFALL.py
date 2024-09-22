# Function to download and process CHIRPS daily data
def process_daily_chirps_data(gdf, year, month, day):
    # Define the link for CHIRPS daily data
    link = f"https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p05/chirps-v2.0.{year}.{month:02d}.{day:02d}.tif.gz"

    # Download the .tif.gz file
    response = requests.get(link)
    with tempfile.TemporaryDirectory() as tmpdir:
        zipped_file_path = os.path.join(tmpdir, "chirps_daily.tif.gz")
        unzipped_file_path = os.path.join(tmpdir, "chirps_daily.tif")

        with open(zipped_file_path, "wb") as f:
            f.write(response.content)

        # Unzip the file
        with gzip.open(zipped_file_path, "rb") as f_in:
            with open(unzipped_file_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Open the unzipped .tif file with Rasterio
        with rasterio.open(unzipped_file_path) as src:
            # Reproject shapefile to match CHIRPS data CRS
            gdf = gdf.to_crs(src.crs)

            # Mask the CHIRPS data using the shapefile geometry
            out_image, out_transform = rasterio.mask.mask(src, gdf.geometry, crop=True)

            # Flatten the masked array and calculate mean excluding masked values
            daily_rains = []
            for geom in gdf.geometry:
                masked_data, _ = rasterio.mask.mask(src, [geom], crop=True)
                masked_data = masked_data.flatten()
                masked_data = masked_data[masked_data != src.nodata]  # Exclude nodata values
                daily_rains.append(masked_data.mean())

            gdf[f'rain_{year}_{month:02d}_{day:02d}'] = daily_rains

    return gdf


# Streamlit app layout
st.title("CHIRPS Daily Data Analysis and Map Generation")
st.image("icf_sl (1).jpg", caption="MAP GENERATOR", use_column_width=True)

# Upload shapefile components
uploaded_shp = st.file_uploader("Upload .shp file", type="shp")
uploaded_shx = st.file_uploader("Upload .shx file", type="shx")
uploaded_dbf = st.file_uploader("Upload .dbf file", type="dbf")

# Year and month selection
years = st.multiselect("Select Years", range(1981, 2025))
months = st.multiselect("Select Months", range(1, 13))

# Variable selection for line plot
variable = st.selectbox("Select Variable for Line Plot", ["rain"])  # Daily rainfall variable

# Ensure that the shapefile and other inputs are provided
if uploaded_shp and uploaded_shx and uploaded_dbf and years and months:
    # Load and process the shapefile
    with st.spinner("Loading and processing shapefile..."):
        gdf = load_shapefile(uploaded_shp, uploaded_shx, uploaded_dbf)

    st.success("Shapefile loaded successfully!")

    # Initialize a list to collect DataFrames
    all_data = []

    # Iterate over each year, month, and day
    for year in years:
        for month in months:
            # Determine the number of days in the selected month
            days_in_month = 30 if month in [4, 6, 9, 11] else 31
            if month == 2:
                # February (account for leap years)
                days_in_month = 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28

            # Process daily data for each day of the month
            for day in range(1, days_in_month + 1):
                with st.spinner(f"Processing CHIRPS data for {year}-{month:02d}-{day:02d}..."):
                    df = process_daily_chirps_data(gdf, year, month, day)
                    df['Year'] = year
                    df['Month'] = month
                    df['Day'] = day
                    all_data.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(all_data, ignore_index=True)

    st.success("CHIRPS daily data processed successfully!")

    # Display the daily rainfall data
    st.write(combined_df)

    # Line plot for each FIRST_DNAM and its corresponding FIRST_CHIE
    st.subheader("Line Plots for Each FIRST_CHIE under FIRST_DNAM")

    # Create separate figures for each unique FIRST_DNAM and plot each associated FIRST_CHIE
    for dnam in combined_df['FIRST_DNAM'].unique():
        # Filter data for the current FIRST_DNAM
        dnam_data = combined_df[combined_df['FIRST_DNAM'] == dnam]
        
        # For each FIRST_DNAM, plot each associated FIRST_CHIE
        for chie in dnam_data['FIRST_CHIE'].unique():
            chie_data = dnam_data[dnam_data['FIRST_CHIE'] == chie]

            # Group data by Year, Month, and Day to plot daily rainfall
            daily_rainfall = chie_data.groupby(['Year', 'Month', 'Day'])[f'rain_{year}_{month:02d}_{day:02d}'].mean().reset_index()

            # Create plot for each FIRST_CHIE under its respective FIRST_DNAM
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.plot(daily_rainfall['Day'], daily_rainfall[f'rain_{year}_{month:02d}_{day:02d}'], marker='o', label=f'{year}-{month:02d}')
            
            ax.set_title(f"{chie} in {dnam}: Daily Rainfall over Days")
            ax.set_xlabel('Day')
            ax.set_ylabel('Rainfall (mm)')
            ax.legend(loc='best')
            ax.annotate(chie, xy=(0.5, 1.05), xycoords='axes fraction', ha='center', fontsize=14, fontweight='bold')

            # Display the plot
            st.pyplot(fig)
            
            # Optionally, add download functionality for each line plot
            line_plot_output = BytesIO()
            fig.savefig(line_plot_output, format='png')
            st.download_button(label=f"Download Line Plot for {chie} in {dnam}",
                               data=line_plot_output.getvalue(),
                               file_name=f"daily_line_plot_{chie}_in_{dnam}_{year}_{month:02d}.png",
                               mime="image/png")

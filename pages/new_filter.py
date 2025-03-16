import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sample DataFrame (replace this with your actual DataFrame)
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
    'Value': [10, 20, 30, 25, 15, 40, 35, 50],
    'Region': ['North', 'South', 'East', 'West', 'North', 'South', 'East', 'West'],
    'Year': [2020, 2021, 2020, 2021, 2020, 2021, 2020, 2021]
})

# Streamlit Sidebar Filters
st.sidebar.header('Select Filters')

# Create filters
category_filter = st.sidebar.selectbox('Select Category', df['Category'].unique())
region_filter = st.sidebar.selectbox('Select Region', df['Region'].unique())
year_filter = st.sidebar.selectbox('Select Year', df['Year'].unique())

# Filter the DataFrame based on the selected values
filtered_df = df[(df['Category'] == category_filter) & 
                 (df['Region'] == region_filter) & 
                 (df['Year'] == year_filter)]

# Display filtered data
st.write("Filtered Data:", filtered_df)

# Plot the bar chart
st.subheader(f'Bar Chart for {category_filter} in {region_filter} ({year_filter})')

plt.figure(figsize=(10, 6))
sns.set_palette("tab10")  # Tab10 color palette
sns.barplot(x='Category', y='Value', data=filtered_df)

# Customize plot appearance
plt.title(f"Value by Category in {region_filter} ({year_filter})", fontsize=16)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Value', fontsize=12)
plt.xticks(rotation=45)

# Show the bar chart in Streamlit
st.pyplot(plt)


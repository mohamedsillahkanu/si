import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sample DataFrame (replace with your actual data)
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
    'Value': [10, 20, 30, 25, 15, 40, 35, 50],
    'Region': ['North', 'South', 'East', 'West', 'North', 'South', 'East', 'West'],
    'Year': [2020, 2021, 2020, 2021, 2020, 2021, 2020, 2021],
    'Sales': [100, 200, 150, 175, 120, 230, 180, 250],
    'Revenue': [10, 30, 25, 20, 15, 40, 35, 45]
})

# List of 10 criteria (customize based on your needs)
criteria_list = ['Sales', 'Revenue', 'Value', 'Category', 'Region', 'Year']

# Streamlit Sidebar - Criteria Selection
st.sidebar.header('Select Criteria')
criteria = st.sidebar.radio('Select Criteria', criteria_list)

# Sidebar Filters for the selected criterion
if criteria == 'Sales':
    region_filter = st.sidebar.selectbox('Select Region', df['Region'].unique())
    year_filter = st.sidebar.selectbox('Select Year', df['Year'].unique())
    filtered_df = df[(df['Region'] == region_filter) & (df['Year'] == year_filter)]
    
elif criteria == 'Revenue':
    category_filter = st.sidebar.selectbox('Select Category', df['Category'].unique())
    year_filter = st.sidebar.selectbox('Select Year', df['Year'].unique())
    filtered_df = df[(df['Category'] == category_filter) & (df['Year'] == year_filter)]
    
elif criteria == 'Value':
    category_filter = st.sidebar.selectbox('Select Category', df['Category'].unique())
    region_filter = st.sidebar.selectbox('Select Region', df['Region'].unique())
    filtered_df = df[(df['Category'] == category_filter) & (df['Region'] == region_filter)]
    
elif criteria == 'Category':
    region_filter = st.sidebar.selectbox('Select Region', df['Region'].unique())
    filtered_df = df[df['Region'] == region_filter]

elif criteria == 'Region':
    category_filter = st.sidebar.selectbox('Select Category', df['Category'].unique())
    year_filter = st.sidebar.selectbox('Select Year', df['Year'].unique())
    filtered_df = df[(df['Category'] == category_filter) & (df['Year'] == year_filter)]

elif criteria == 'Year':
    category_filter = st.sidebar.selectbox('Select Category', df['Category'].unique())
    region_filter = st.sidebar.selectbox('Select Region', df['Region'].unique())
    filtered_df = df[(df['Category'] == category_filter) & (df['Region'] == region_filter)]

# Filtered DataFrame Preview
st.write("Filtered Data:", filtered_df)

# Plotting the bar chart based on selected criterion
st.subheader(f'Bar Chart for {criteria}')

plt.figure(figsize=(10, 6))
sns.set_palette("tab10")  # Tab10 color palette
sns.barplot(x='Category', y=criteria, data=filtered_df)

# Customize plot appearance
plt.title(f"{criteria} by Category", fontsize=16)
plt.xlabel('Category', fontsize=12)
plt.ylabel(criteria, fontsize=12)
plt.xticks(rotation=45)

# Display the plot
st.pyplot(plt)

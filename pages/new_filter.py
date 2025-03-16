import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import numpy as np

# Define unique values for each category
categories = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
regions = ['North', 'South', 'East', 'West']
years = [2020, 2021, 2022]

# Generate all possible combinations of (Category, Region, Year)
data = list(itertools.product(categories, regions, years))

# Create a DataFrame with values for each combination
df = pd.DataFrame(data, columns=['Category', 'Region', 'Year'])

# Generate random values for Sales, Revenue, and Value
np.random.seed(42)  # For reproducibility
df['Sales'] = np.random.randint(50, 300, size=len(df))
df['Revenue'] = np.random.randint(10, 100, size=len(df))
df['Value'] = np.random.randint(5, 50, size=len(df))

# Sidebar filters
st.sidebar.header('Filters')
category_filter = st.sidebar.selectbox('Select Category', df['Category'].unique())
region_filter = st.sidebar.selectbox('Select Region', df['Region'].unique())

# Create a new column marking if the row meets the selected criteria
df['Criteria_Met'] = df.apply(
    lambda row: "Yes" if (row['Category'] == category_filter) & (row['Region'] == region_filter) else "No", axis=1
)

# Count occurrences of "Yes" and "No"
criteria_counts = df['Criteria_Met'].value_counts().reset_index()
criteria_counts.columns = ['Criteria Met', 'Count']

# Display filtered data
st.write("Filtered Data:", df)

# Bar chart visualization
st.subheader('Criteria Met Bar Chart')

plt.figure(figsize=(8, 5))
sns.set_palette("tab10")  # Set color theme
sns.barplot(x='Criteria Met', y='Count', data=criteria_counts)

# Customize chart appearance
plt.title("Count of Criteria Met ('Yes' vs. 'No')", fontsize=14)
plt.xlabel("Criteria Met", fontsize=12)
plt.ylabel("Count", fontsize=12)

# Show plot in Streamlit
st.pyplot(plt)

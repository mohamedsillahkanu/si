import streamlit as st
import plotly.express as px
import pandas as pd

# Sample Data (you can replace this with your own dataset)
df = px.data.gapminder()

# Filter data for fewer countries to make the animation cleaner
df = df[df['continent'] == 'Asia']

# Create an animated bar chart
fig = px.bar(df, x='country', y='gdpPercap', color='country',
             animation_frame='year', animation_group='country',
             range_y=[0, df['gdpPercap'].max()],
             title="GDP per Capita Over Time in Asia",
             labels={'gdpPercap':'GDP per Capita', 'country':'Country'})

# Display the animated bar chart in Streamlit
st.plotly_chart(fig)

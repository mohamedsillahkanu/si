import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to create a stacked bar chart
def create_stacked_bar_chart(data, feature1, feature2):
    cross_tab = pd.crosstab(data[feature1], data[feature2])
    cross_tab_percentage = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100  # Convert to percentage

    ax = cross_tab_percentage.plot(kind='bar', stacked=True, figsize=(10, 6))
    ax.set_ylabel("Percentage")
    ax.set_title(f'Stacked Bar Chart of {feature1} vs {feature2}')
    ax.legend(title=feature2, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    st.pyplot(plt)

# Function to create a component bar chart
def create_component_bar_chart(data, feature1):
    counts = data[feature1].value_counts(normalize=True) * 100  # Get percentages
    ax = counts.plot(kind='bar', figsize=(10, 6))
    ax.set_ylabel("Percentage")
    ax.set_title(f'Component Bar Chart of {feature1}')

    plt.tight_layout()
    st.pyplot(plt)

# Streamlit app
st.title("Categorical Variable Visualization App")

# Upload file
uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=['xlsx', 'csv'])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("Data Preview:")
    st.write(df)

    # Select columns for analysis
    feature1 = st.selectbox("Select primary feature (e.g., District)", df.columns)
    feature2 = st.selectbox("Select secondary feature (e.g., Chiefdom)", df.columns)

    chart_type = st.radio("Select chart type", ('Stacked Bar Chart', 'Component Bar Chart'))

    if chart_type == 'Stacked Bar Chart':
        create_stacked_bar_chart(df, feature1, feature2)
    else:
        create_component_bar_chart(df, feature1)

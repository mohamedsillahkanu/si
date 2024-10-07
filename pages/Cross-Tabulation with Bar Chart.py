import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# App title
st.title("Cross-Tabulation with Bar Chart")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Overview: Cross-Tabulation and Bar Chart")

    st.subheader("What is Cross-Tabulation?")
    st.write("""
        Cross-tabulation, or contingency table analysis, helps examine the relationship between two or more categorical variables. 
        It shows the frequency (count) and often percentages of combinations of categories.
    """)

    st.subheader("Bar Chart Illustration")
    st.write("After constructing the cross-tabulation table, a bar chart can visually display the frequency distribution across categories.")

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Illustration: Cross-Tabulation with Bar Chart")
    
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

            # Ask the user to select two categorical columns for cross-tabulation
            cat_column1 = st.selectbox("Select the first categorical variable", df.columns)
            cat_column2 = st.selectbox("Select the second categorical variable", df.columns)

            # Generate the cross-tabulation table with counts and percentages
            cross_tab = pd.crosstab(df[cat_column1], df[cat_column2], margins=False)

            # Add percentage formatting to the cross-tabulation table
            cross_tab_percent = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100
            formatted_table = cross_tab.astype(str) + ' (' + cross_tab_percent.round(2).astype(str) + '%)'

            # Display the cross-tabulation table with counts and percentages
            st.write("Cross-Tabulation Table (Count and Percentage):")
            st.write(formatted_table)

            # Bar chart of the counts
            st.write("Bar Chart of Counts:")
            cross_tab.plot(kind='bar', stacked=True)

            # Display the bar chart using Matplotlib
            plt.title('Cross-Tabulation Bar Chart')
            plt.ylabel('Count')
            plt.xlabel(cat_column1)
            st.pyplot(plt)

        except Exception as e:
            st.error(f"Error loading file: {e}")

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# App title
st.title("Cross-Tabulation with Bar Chart and Pie Chart")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Overview: Cross-Tabulation, Bar Chart, and Pie Chart")

    st.subheader("What is Cross-Tabulation?")
    st.write("""
        Cross-tabulation, or contingency table analysis, helps examine the relationship between two or more categorical variables. 
        It shows the frequency (count) and often percentages of combinations of categories.
    """)

    st.subheader("Visual Representation")
    st.write("""
        - **Bar Chart**: Visualizes the count for each combination of categories.
        - **Pie Chart**: Displays the proportion of each category combination.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Illustration: Cross-Tabulation, Bar Chart, and Pie Chart")
    
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
            ax = cross_tab.plot(kind='bar', stacked=True)

            # Add the legend to the bar chart
            ax.legend(title=cat_column2, loc='upper right', bbox_to_anchor=(1.15, 1))
            plt.title('Cross-Tabulation Bar Chart')
            plt.ylabel('Count')
            plt.xlabel(cat_column1)

            # Display the bar chart using Matplotlib
            st.pyplot(plt)

            # Pie Chart Section
            st.write("Pie Chart of Proportions:")
            
            # Flatten the cross_tab DataFrame to create pie chart data
            cross_tab_flat = cross_tab.stack().reset_index(name='count')
            cross_tab_flat['label'] = cross_tab_flat[cat_column1] + ' - ' + cross_tab_flat[cat_column2]

            # Generate the pie chart
            fig, ax = plt.subplots()
            ax.pie(cross_tab_flat['count'], labels=cross_tab_flat['label'], autopct='%1.1f%%', startangle=90)
            ax.legend(loc="upper right", bbox_to_anchor=(1, 1))
            plt.title("Proportions of Categories")
            plt.tight_layout()

            # Display the pie chart in Streamlit
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error loading file: {e}")

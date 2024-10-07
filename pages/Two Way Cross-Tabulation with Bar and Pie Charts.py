import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# App title
st.title("2-Way Cross-Tabulation with Bar and Pie Charts")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Overview: 2-Way Cross-Tabulation, Bar and Pie Charts")

    st.subheader("What is a 2-Way Cross-Tabulation?")
    st.write("""
        A 2-way cross-tabulation examines the relationships among two categorical variables.
        It provides insight into how the combination of these two variables interacts.
    """)

    st.subheader("Visual Representation")
    st.write("""
        - **Bar Chart**: Visualizes the count for combinations of two categorical variables.
        - **Pie Chart**: Displays the proportions for each combination of categories.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Illustration: 2-Way Cross-Tabulation, Bar and Pie Charts")
    
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

            # Ask the user to select two categorical columns
            cat_column1 = st.selectbox("Select the first categorical variable", df.columns)
            cat_column2 = st.selectbox("Select the second categorical variable", df.columns)

            # Generate the 2-way cross-tabulation table
            cross_tab = pd.crosstab(df[cat_column1], df[cat_column2], margins=False)

            # Add percentage formatting to the cross-tabulation table
            cross_tab_percent = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100
            formatted_table = cross_tab.astype(str) + ' (' + cross_tab_percent.round(2).astype(str) + '%)'

            # Display the cross-tabulation table with counts and percentages
            st.write("2-Way Cross-Tabulation Table (Count and Percentage):")
            st.write(formatted_table)

            # Input fields for custom titles
            bar_chart_title = st.text_input("Enter a title for the Bar Chart:", "2-Way Cross-Tabulation Bar Chart")
            pie_chart_title = st.text_input("Enter a title for the Pie Chart:", "Proportions of Categories")

            # Bar chart of the counts
            st.write("Bar Chart of Counts:")
            ax = cross_tab.plot(kind='bar', stacked=True)

            # Add the legend to the bar chart
            ax.legend(title=cat_column2, loc='upper left', bbox_to_anchor=(1, 1))  # Legend outside
            plt.title(bar_chart_title)
            plt.ylabel('Count')
            plt.xlabel(cat_column1)

            # Display the bar chart using Matplotlib
            st.pyplot(plt)

            # Pie Chart Section
            st.write("Pie Chart of Proportions:")
            
            # Flatten the cross_tab DataFrame to create pie chart data
            cross_tab_flat = cross_tab.stack().reset_index(name='count')
            cross_tab_flat['label'] = cross_tab_flat[cat_column1] + ' - ' + cross_tab_flat[cat_column2]

            # Generate the pie chart with a smaller size
            fig, ax = plt.subplots(figsize=(8, 8))  # Set a smaller size for the pie chart
            ax.pie(cross_tab_flat['count'], labels=cross_tab_flat['label'], autopct='%1.1f%%', startangle=90)

            # Create a rectangular box around the pie chart
            box = plt.Rectangle((-1.5, -1.5), 3, 3, fill=False, edgecolor='black', linewidth=2)
            ax.add_artist(box)

            # Set legend at the bottom of the pie chart
            ax.legend(title="Categories", loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3)  # Legend at the bottom
            plt.title(pie_chart_title)
            plt.tight_layout()

            # Display the pie chart in Streamlit
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error loading file: {e}")

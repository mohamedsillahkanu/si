import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# App title
st.title("Dummy Table with Categorical and Numeric Variables")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Overview: Dummy Table")

    st.subheader("What is a Dummy Table?")
    st.write("""
        A dummy table summarizes data involving both categorical and numeric variables.
        It provides insights into how numeric values interact with categorical groups.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Illustration: Dummy Table")
    
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

            # Ask the user to select one categorical and one numeric column
            cat_column = st.selectbox("Select a categorical variable", df.select_dtypes(include=['object', 'category']).columns)
            num_column = st.selectbox("Select a numeric variable", df.select_dtypes(include=['float64', 'int64']).columns)

            # Input field for the title of the dummy table
            table_title = st.text_input("Enter a title for the Dummy Table:", "Summary Table")

            # Generate the summary table
            summary_table = df.groupby(cat_column)[num_column].agg(['count', 'mean', 'sum', 'std']).reset_index()
            summary_table.columns = [cat_column, 'Count', 'Mean', 'Total', 'Std Dev']

            # Calculate percentage
            summary_table['Percentage'] = (summary_table['Total'] / summary_table['Total'].sum()) * 100

            # Display the summary table
            st.write(f"**{table_title}**")
            st.write(summary_table)

            # Input fields for plot titles
            bar_chart_title = st.text_input("Enter a title for the Horizontal Bar Chart:", "Mean by Category")
            pie_chart_title = st.text_input("Enter a title for the Pie Chart:", "Total by Category")
            histogram_title = st.text_input("Enter a title for the Histogram:", f'Histogram of {num_column}')

            # Horizontal Bar Chart of Mean
            st.write("Horizontal Bar Chart of Mean:")
            mean_values = summary_table.sort_values(by='Mean', ascending=False)
            plt.figure(figsize=(10, 6))
            plt.barh(mean_values[cat_column], mean_values['Mean'], color='skyblue')
            plt.xlabel('Mean')
            plt.title(bar_chart_title)
            plt.grid(axis='x')
            plt.tight_layout()
            plt.savefig('mean_bar_chart.png')
            st.pyplot(plt)

            # Pie Chart of Total
            st.write("Pie Chart of Total:")
            plt.figure(figsize=(8, 8))
            plt.pie(mean_values['Total'], labels=mean_values[cat_column], autopct='%1.1f%%', startangle=90)
            plt.title(pie_chart_title)
            plt.tight_layout()
            plt.savefig('total_pie_chart.png')
            st.pyplot(plt)

            # Histogram of Numeric Variable
            st.write("Histogram of Numeric Variable:")
            plt.figure(figsize=(10, 6))
            plt.hist(df[num_column], bins=20, color='lightgreen', edgecolor='black')
            plt.xlabel(num_column)
            plt.ylabel('Frequency')
            plt.title(histogram_title)
            plt.grid(axis='y')
            plt.tight_layout()
            plt.savefig('histogram.png')
            st.pyplot(plt)

            st.success("Plots have been generated and saved as PNG files.")

        except Exception as e:
            st.error(f"Error loading file: {e}")

import streamlit as st
import pandas as pd

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
        A dummy table can summarize data involving both categorical and numeric variables.
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

            # Generate the summary table
            summary_table = df.groupby(cat_column)[num_column].agg(['count', 'mean', 'sum', 'std']).reset_index()
            summary_table.columns = [cat_column, 'Count', 'Mean', 'Total', 'Std Dev']

            # Display the summary table
            st.write("Summary Table:")
            st.write(summary_table)

        except Exception as e:
            st.error(f"Error loading file: {e}")

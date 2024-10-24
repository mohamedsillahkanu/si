import streamlit as st
import pandas as pd
import numpy as np
import pingouin as pg

# App title
st.title("Repeated Measures ANOVA Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Repeated Measures ANOVA Overview", "Repeated Measures ANOVA Illustration"])

# 1. Repeated Measures ANOVA Overview Section
if section == "Repeated Measures ANOVA Overview":
    st.header("Repeated Measures ANOVA for Comparing Means")
    
    st.subheader("When to Use It")
    st.write("""
        Repeated Measures ANOVA is used to determine if there are significant differences between the means of three or more related groups.
        It is commonly used when the same subjects are used for each condition (e.g., measurements at different times).
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using Repeated Measures ANOVA:")
    st.write("1. **Three or More Related Samples**: Measurements taken under different conditions or at different times for the same subjects.")
    
    st.subheader("Purpose of Repeated Measures ANOVA")
    st.write("""
        The purpose of Repeated Measures ANOVA is to determine if there are statistically significant differences between the means of the related groups.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Repeated Measures ANOVA](https://en.wikipedia.org/wiki/Repeated_measures_ANOVA).")

# 2. Repeated Measures ANOVA Illustration Section
elif section == "Repeated Measures ANOVA Illustration":
    st.header("Repeated Measures ANOVA Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="rm_anova_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the subject and measurement columns
            subject_column = st.selectbox("Select the subject identifier column", df.columns)
            measurement_columns = st.multiselect("Select the columns representing the repeated measurements", df.columns)
            
            if len(measurement_columns) >= 2:
                # Prepare the data for Repeated Measures ANOVA
                df_long = pd.melt(df, id_vars=[subject_column], value_vars=measurement_columns, var_name='Condition', value_name='Value')
                
                # Perform Repeated Measures ANOVA
                aov = pg.rm_anova(dv='Value', within='Condition', subject=subject_column, data=df_long, detailed=True)
                
                # Display the results
                st.subheader("Repeated Measures ANOVA Results")
                st.write(aov)
                
                # Interpretation tips
                st.subheader("How to Interpret the Results")
                st.write("""
                    - **F-Statistic**: The F-statistic indicates the ratio of the variance between the conditions to the variance within the conditions.
                    - **P-value**: A p-value less than 0.05 indicates that there are significant differences between the means of the conditions.
                    
                    If the p-value is significant, you can conclude that at least one of the conditions differs from the others.
                """)
            else:
                st.warning("Please select at least two columns for Repeated Measures ANOVA.")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")


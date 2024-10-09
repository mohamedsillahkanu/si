import streamlit as st
import pandas as pd
import numpy as np
from factor_analyzer import FactorAnalyzer

# App title
st.title("Factor Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Factor Analysis")
    
    st.subheader("When to Use It")
    st.write("""
        Factor analysis is used to identify underlying relationships between variables. 
        It is helpful in data reduction, revealing the structure of the data, and in understanding 
        the latent constructs that influence observed variables.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("A general rule is to have at least 5-10 observations per variable.")
    
    st.subheader("Number of Variables")
    st.write("Factor analysis can be performed on datasets with multiple numeric variables.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of factor analysis is to reduce the number of variables and identify 
        the underlying relationships between them. This can help in identifying key factors 
        that explain the observed correlations.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how this test can be used in malaria research:")
    
    st.write("""
    1. **Malaria Symptoms and Test Results**: Factor analysis can help identify groups of symptoms that commonly occur together in malaria patients, 
       providing insight into symptom clusters.
    """)
    
    st.write("""
    2. **Risk Factors for Malaria**: Researchers can use factor analysis to uncover underlying risk factors related to malaria infection, such as 
       environmental, behavioral, and socio-economic factors.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Factor Analysis")
    
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
            
            # Selecting numeric columns for factor analysis
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            selected_columns = st.multiselect("Select numeric variables for factor analysis", numeric_columns)
            
            if selected_columns:
                # Performing Factor Analysis
                fa = FactorAnalyzer(n_factors=2, rotation='varimax')
                fa.fit(df[selected_columns])
                
                # Get Eigenvalues
                eigenvalues = fa.get_eigenvalues()
                
                # Display Eigenvalues
                st.write("Eigenvalues:")
                st.write(eigenvalues)
                
                # Get Factor Loadings
                loadings = fa.loadings_
                st.write("Factor Loadings:")
                st.write(pd.DataFrame(loadings, index=selected_columns, columns=[f'Factor {i+1}' for i in range(loadings.shape[1])]))

                # Check the proportion of variance explained
                variance_explained = fa.get_factor_variance()
                st.write("Variance Explained by Each Factor:")
                st.write(pd.DataFrame(variance_explained, index=['Variance', 'Proportion Variance', 'Cumulative Variance']))
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

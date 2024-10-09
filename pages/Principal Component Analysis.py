import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# App title
st.title("Principal Component Analysis (PCA)")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Test Overview", "Test Illustration"])

# 1. Test Overview Section
if section == "Test Overview":
    st.header("Test Overview: Principal Component Analysis (PCA)")

    st.subheader("When to Use It")
    st.write("""
        Principal Component Analysis (PCA) is used when you want to reduce the dimensionality of your dataset while preserving 
        as much variance as possible. It is particularly useful when you have a large number of features and want to visualize 
        or analyze the data more easily.
    """)
    
    st.subheader("Number of Samples Required")
    st.write("There is no strict minimum, but typically at least 10 samples per feature is recommended for effective PCA.")
    
    st.subheader("Number of Variables")
    st.write("PCA can be applied to datasets with any number of numerical variables. Categorical variables should be converted into numerical form before PCA.")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of PCA is to transform the original variables into a new set of variables (principal components) that are 
        uncorrelated and that capture the maximum variance in the data.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how PCA can be used in malaria research:")
    
    st.write("""
    1. **Analysis of Malaria Symptoms**: PCA can help in identifying patterns among multiple symptoms of malaria, allowing 
       researchers to understand which symptoms contribute most to the variance in patient presentations.
    """)
    
    st.write("""
    2. **Genomic Data Analysis**: In genomic studies related to malaria, PCA can be used to reduce the dimensionality of genetic 
       data, helping researchers to visualize and identify relationships between different genetic markers associated with malaria susceptibility.
    """)

# 2. Test Illustration Section
elif section == "Test Illustration":
    st.header("Test Illustration: Principal Component Analysis (PCA)")
    
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
            
            # Select numeric columns for PCA
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            selected_cols = st.multiselect("Select numeric columns for PCA", numeric_cols)
            
            if st.button("Perform PCA"):
                if len(selected_cols) == 0:
                    st.warning("Please select at least one numeric column.")
                else:
                    # Standardizing the data
                    scaler = StandardScaler()
                    scaled_data = scaler.fit_transform(df[selected_cols])

                    # Performing PCA
                    pca = PCA(n_components=2)
                    principal_components = pca.fit_transform(scaled_data)

                    # Create a DataFrame with PCA results
                    pca_df = pd.DataFrame(data=principal_components, columns=['Principal Component 1', 'Principal Component 2'])
                    
                    # Display PCA results
                    st.write("PCA Results:")
                    st.write(pca_df.head())
                    
                    # Explained variance
                    st.write("Explained Variance Ratio:")
                    st.write(pca.explained_variance_ratio_)

                    # Plotting PCA
                    plt.figure(figsize=(10, 6))
                    plt.scatter(pca_df['Principal Component 1'], pca_df['Principal Component 2'], alpha=0.5)
                    plt.title("PCA Result")
                    plt.xlabel("Principal Component 1")
                    plt.ylabel("Principal Component 2")
                    plt.grid()
                    st.pyplot(plt)
        
        except Exception as e:
            st.error(f"Error loading file: {e}")

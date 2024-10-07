import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to display cross-tabulation for two categorical variables
def two_way_analysis(df):
    # Get user selection for the two categorical variables
    var_a = st.selectbox("Select Variable A", df.columns)
    var_b = st.selectbox("Select Variable B", df.columns)

    # Create cross-tabulation
    crosstab = pd.crosstab(df[var_a], df[var_b], margins=True)
    
    st.write("### Cross-Tabulation Table:")
    st.dataframe(crosstab)

    # Plotting the bar chart
    st.write("### Bar Chart:")
    ax = crosstab.iloc[:-1, :-1].plot(kind='bar', stacked=True)
    plt.title(f'Bar Chart of {var_a} vs {var_b}')
    plt.xlabel(var_a)
    plt.ylabel('Counts')
    plt.legend(title=var_b, bbox_to_anchor=(1.05, 1), loc='upper left')  # Legend outside
    st.pyplot()

    # Plotting the pie chart
    st.write("### Pie Chart:")
    pie_ax = crosstab.iloc[:-1, :-1].sum().plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title(f'Pie Chart of {var_a}')
    plt.legend(title=var_b, bbox_to_anchor=(1.05, 1), loc='upper left')  # Legend outside
    st.pyplot()

# Streamlit app for Two-Way Analysis
def main():
    st.title("Two-Way Categorical Variable Analysis App")

    # File upload
    uploaded_file = st.file_uploader("Upload an Excel file", type=['xlsx'])
    
    if uploaded_file:
        # Read the uploaded file
        df = pd.read_excel(uploaded_file)

        st.write("### Uploaded Data:")
        st.dataframe(df)

        two_way_analysis(df)

if __name__ == "__main__":
    main()

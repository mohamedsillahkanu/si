import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to display cross-tabulation for three categorical variables
def three_way_analysis(df):
    # Get user selection for the three categorical variables
    var_x = st.selectbox("Select Variable X", df.columns)
    var_y = st.selectbox("Select Variable Y", df.columns)
    var_z = st.selectbox("Select Variable Z", df.columns)

    # Create cross-tabulation
    crosstab = pd.crosstab(index=[df[var_x], df[var_y]], columns=df[var_z])
    
    st.write("### Cross-Tabulation Table:")
    st.dataframe(crosstab)

    # Plotting the bar chart
    st.write("### Bar Chart:")
    ax = crosstab.plot(kind='bar', stacked=True)
    plt.title(f'Bar Chart of {var_x} vs {var_y} vs {var_z}')
    plt.xlabel(f'{var_x} and {var_y}')
    plt.ylabel('Counts')
    plt.legend(title=var_z, bbox_to_anchor=(1.05, 1), loc='upper left')  # Legend outside
    st.pyplot()

    # Plotting the pie chart
    st.write("### Pie Chart:")
    pie_ax = crosstab.sum(axis=1).plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title(f'Pie Chart of {var_x}')
    plt.legend(title=var_z, bbox_to_anchor=(1.05, 1), loc='upper left')  # Legend outside
    st.pyplot()

# Streamlit app for Three-Way Analysis
def main():
    st.title("Three-Way Categorical Variable Analysis App")

    # File upload
    uploaded_file = st.file_uploader("Upload an Excel file", type=['xlsx'])
    
    if uploaded_file:
        # Read the uploaded file
        df = pd.read_excel(uploaded_file)

        st.write("### Uploaded Data:")
        st.dataframe(df)

        three_way_analysis(df)

if __name__ == "__main__":
    main()

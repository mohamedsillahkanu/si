import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# App title
st.title("Difference-in-Differences Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Difference-in-Differences Overview", "Difference-in-Differences Illustration"])

# 1. Difference-in-Differences Overview Section
if section == "Difference-in-Differences Overview":
    st.header("Difference-in-Differences Analysis for Causal Inference")
    
    st.subheader("When to Use It")
    st.write("""
        Difference-in-Differences (DiD) is a statistical technique used in econometrics and social sciences to estimate the causal effect of a treatment or intervention.
        It is commonly used when observational data is available, and there is a need to compare outcomes between treated and control groups before and after the intervention.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need the following data for using the Difference-in-Differences method:")
    st.write("1. **Treated and Control Groups**: Two groups, one that receives the intervention and one that does not.")
    st.write("2. **Before and After Periods**: Data from before and after the intervention for both groups.")
    
    st.subheader("Purpose of the Difference-in-Differences Method")
    st.write("""
        The purpose of the Difference-in-Differences method is to estimate the causal effect of an intervention by comparing the differences in outcomes over time between treated and control groups.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here is a practical example of how the Difference-in-Differences method can be used in malaria research:")
    
    st.write("""
    **Evaluating the Impact of a New Malaria Treatment**: 
       Researchers can use DiD to estimate the effect of a new malaria treatment by comparing malaria incidence in regions that received the treatment (treated group) with those that did not (control group) before and after the treatment rollout.
    """)
    
    st.write("For more information, visit the [Wikipedia page on Difference-in-Differences](https://en.wikipedia.org/wiki/Difference_in_differences).")

# 2. Difference-in-Differences Illustration Section
elif section == "Difference-in-Differences Illustration":
    st.header("Difference-in-Differences Illustration")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="did_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the relevant columns
            time_column = st.selectbox("Select the time column (before/after)", df.columns)
            group_column = st.selectbox("Select the group column (treated/control)", df.columns)
            outcome_column = st.selectbox("Select the outcome column (e.g., malaria cases)", df.columns)
            
            # Create dummy variables for regression
            df['time_dummy'] = df[time_column].apply(lambda x: 1 if x == 'after' else 0)
            df['group_dummy'] = df[group_column].apply(lambda x: 1 if x == 'treated' else 0)
            df['interaction'] = df['time_dummy'] * df['group_dummy']
            
            # Fit the Difference-in-Differences model
            X = df[['time_dummy', 'group_dummy', 'interaction']]
            X = sm.add_constant(X)
            y = df[outcome_column]
            model = sm.OLS(y, X).fit()
            
            # Display the regression results
            st.subheader("Regression Results")
            st.write(model.summary())
            
            # Plot the outcome for treated and control groups before and after the intervention
            st.subheader("Difference-in-Differences Plot")
            avg_outcomes = df.groupby([time_column, group_column])[outcome_column].mean().unstack()
            avg_outcomes.plot(kind='bar', figsize=(10, 6))
            plt.xlabel('Time Period')
            plt.ylabel(outcome_column)
            plt.title('Difference-in-Differences Plot')
            plt.legend(title='Group')
            st.pyplot(plt)
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



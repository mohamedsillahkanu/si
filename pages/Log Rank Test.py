import streamlit as st
import pandas as pd
import numpy as np
from lifelines.statistics import logrank_test
import matplotlib.pyplot as plt

# App title
st.title("Log-Rank Test for Survival Analysis")

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Log-Rank Test Overview", "Log-Rank Test Illustration"])

# 1. Log-Rank Test Overview Section
if section == "Log-Rank Test Overview":
    st.header("Log-Rank Test for Comparing Survival Curves")
    
    st.subheader("When to Use It")
    st.write("""
        The Log-Rank Test is a statistical test used to compare the survival distributions of two groups. 
        It is commonly used in medical research to determine if there is a significant difference in survival times between two groups.
    """)
    
    st.subheader("Data Requirements")
    st.write("You need three variables for the Log-Rank Test:")
    st.write("1. **Time to Event**: The time duration until the event occurs (e.g., death, relapse).")
    st.write("2. **Event Occurrence**: A binary variable indicating whether the event occurred (1 for event, 0 for censored).")
    st.write("3. **Grouping Variable**: A categorical variable indicating the group assignment of each subject (e.g., treatment group, control group).")
    
    st.subheader("Purpose of the Test")
    st.write("""
        The purpose of the Log-Rank Test is to determine if there is a statistically significant difference between the survival curves of two groups.
    """)
    
    st.subheader("Real-Life Medical Examples (Malaria)")
    st.write("Here are two practical examples of how the Log-Rank Test can be used in malaria research:")
    
    st.write("""
    1. **Comparing Survival Times Between Treatment Groups**: 
       Researchers can use the Log-Rank Test to compare the survival times of patients receiving two different types of antimalarial treatments.
    """)
    
    st.write("""
    2. **Evaluating the Effectiveness of Preventive Measures**: 
       The test can be used to compare the time to relapse for patients using different preventive measures, such as bed nets versus no bed nets.
    """)
    
    st.write("For more information, visit the [Wikipedia page on the Log-Rank Test](https://en.wikipedia.org/wiki/Log-rank_test).")

# 2. Log-Rank Test Illustration Section
elif section == "Log-Rank Test Illustration":
    st.header("Log-Rank Test for Comparing Survival Curves")
    
    st.subheader("Upload your dataset (CSV or XLSX)")
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"], key="logrank_file")
    
    if uploaded_file is not None:
        # Load the dataset based on file type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                
            st.write("Here is a preview of your data:")
            st.write(df.head())
            
            # Ask the user to select the time, event, and group columns
            time_column = st.selectbox("Select the time to event variable", df.columns)
            event_column = st.selectbox("Select the event occurrence variable", df.columns)
            group_column = st.selectbox("Select the grouping variable", df.columns)
            
            st.write(f"You selected: {time_column}, {event_column}, and {group_column} for the Log-Rank Test.")
            
            # Button to perform the log-rank test
            if st.button("Perform Log-Rank Test"):
                unique_groups = df[group_column].unique()
                if len(unique_groups) == 2:
                    group1, group2 = unique_groups
                    df_group1 = df[df[group_column] == group1]
                    df_group2 = df[df[group_column] == group2]

                    # Perform the log-rank test
                    results = logrank_test(
                        df_group1[time_column], df_group2[time_column],
                        event_observed_A=df_group1[event_column],
                        event_observed_B=df_group2[event_column]
                    )

                    # Display the p-value
                    st.write(f"**Log-Rank Test p-value:** {results.p_value}")
                    
                    # Display a tip for interpretation
                    st.write("""
                    **Tip for Interpretation**: 
                    - The p-value from the log-rank test indicates whether there is a statistically significant difference between the survival curves of the two groups.
                    - A p-value less than 0.05 generally indicates a significant difference in survival between the groups.
                    """)
                else:
                    st.error("The selected grouping variable must have exactly two unique values for the log-rank test.")
                
        except Exception as e:
            st.error(f"Error loading file: {e}")



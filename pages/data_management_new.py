import streamlit as st
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import probplot, norm

# Sidebar for Data Management
st.sidebar.title("Data Management")
data_management_option = st.sidebar.radio(
    "Choose an option:",
    ["Import Dataset", "Data Cleaning"]
)

# Initialize session state variables
if 'df' not in st.session_state:
    st.session_state.df = None
if 'saved_df' not in st.session_state:
    st.session_state.saved_df = None
if 'history' not in st.session_state:
    st.session_state.history = []

def save_data():
    if st.session_state.df is not None:
        st.session_state.history.append(st.session_state.df.copy())
        if len(st.session_state.history) > 5:
            st.session_state.history.pop(0)
        st.session_state.saved_df = st.session_state.df.copy()
    else:
        st.warning("No data available to save.")

def undo_last_action():
    if st.session_state.history:
        st.session_state.df = st.session_state.history.pop()
        st.success("Last action undone.")
    else:
        st.warning("No more actions to undo.")

# Main App
st.title("Data Processing App")

if data_management_option == "Import Dataset":
    st.header("Import Dataset")
    file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    if file:
        if file.name.endswith(".csv"):
            st.session_state.df = pd.read_csv(file)
        elif file.name.endswith(".xlsx"):
            st.session_state.df = pd.read_excel(file)
        st.success("Dataset uploaded successfully!")
        st.write("Preview of the uploaded dataset:")
        st.dataframe(st.session_state.df)

elif data_management_option == "Data Cleaning":
    st.header("Data Cleaning")
    cleaning_option = st.selectbox("Choose a cleaning option:", ["Compute or Create New Variable"])

    if cleaning_option == "Compute or Create New Variable":
        st.header("Compute or Create New Variable")
        if st.session_state.df is not None:
            st.subheader("Define New Variable")

            # Step 1: Select columns
            columns_selected = st.multiselect("Select columns to include in computation:", st.session_state.df.columns)

            # Step 2: Specify operations
            operation = st.radio("Choose an operation:", ["Add (+)", "Subtract (-)", "Multiply (*)", "Divide (/)"])

            # Step 3: Add parentheses (optional)
            use_parentheses = st.checkbox("Use parentheses?")
            parentheses_expression = ""
            if use_parentheses:
                parentheses_expression = st.text_input(
                    "Enter parentheses expression (e.g., (A+B)*C):",
                    key="parentheses_expression"
                )

            # Step 4: Add conditional logic (if-else statement)
            use_if_else = st.checkbox("Add conditional logic?")
            if_condition = ""
            else_value = ""
            if use_if_else:
                if_condition = st.text_input("Enter the if-condition (e.g., A-B):", key="if_condition")
                else_value = st.text_input("Enter the value to replace if the condition is met (e.g., 0):", key="else_value")

            # Step 5: Enter a new variable name
            new_var_name = st.text_input("Enter the name for the new variable:", key="new_var_name")

            # Step 6: Compute the variable
            if st.button("Compute New Variable"):
                try:
                    if not new_var_name:
                        st.error("Please enter a name for the new variable.")
                    elif not columns_selected:
                        st.error("Please select at least one column.")
                    else:
                        # Build the computation expression
                        if use_parentheses and parentheses_expression:
                            expression = parentheses_expression
                        else:
                            operations_map = {
                                "Add (+)": "+",
                                "Subtract (-)": "-",
                                "Multiply (*)": "*",
                                "Divide (/)": "/"
                            }
                            operator = operations_map[operation]
                            expression = f" {operator} ".join(columns_selected)

                        # Add conditional logic if enabled
                        if use_if_else and if_condition and else_value:
                            expression = f"np.where({if_condition} >= 0, {if_condition}, {else_value})"

                        # Safely evaluate the expression
                        st.session_state.df[new_var_name] = st.session_state.df.eval(expression)
                        st.success(f"Computed new variable '{new_var_name}':")
                        st.dataframe(st.session_state.df)
                        save_data()
                except Exception as e:
                    st.error(f"Error computing new variable: {e}")
        else:
            st.warning("No dataset available. Please import and merge datasets first.")

# Add Undo Button
if st.session_state.df is not None:
    if st.button("Undo Last Action"):
        undo_last_action()
        st.dataframe(st.session_state.df)

# Always show Save and Download buttons
if st.session_state.df is not None:
    st.write("Save and Download Updated Data:")
    if st.button("Save"):
        save_data()
        st.success("Data saved successfully.")

    if st.session_state.saved_df is not None:
        st.download_button(
            label="Download Updated Data",
            data=st.session_state.saved_df.to_csv(index=False),
            file_name="updated_data.csv",
            mime="text/csv"
        )

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
    ["Import Dataset", "Sanity Checks", "Merge Datasets", "Data Cleaning", "Quality Control/Checks"]
)

# Initialize session state variables
if 'df' not in st.session_state:
    st.session_state.df = None
if 'saved_df' not in st.session_state:
    st.session_state.saved_df = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'dfs' not in st.session_state:
    st.session_state.dfs = []

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
    files = st.file_uploader("Upload files", type=["csv", "xlsx", "xls"], accept_multiple_files=True)
    if files:
        st.session_state.dfs = []
        for file in files:
            if file.name.endswith(".csv"):
                st.session_state.dfs.append(pd.read_csv(file))
            elif file.name.endswith(".xlsx") or file.name.endswith(".xls"):
                st.session_state.dfs.append(pd.read_excel(file))
            else:
                st.error(f"Unsupported file format: {file.name}")
        st.success("Datasets uploaded successfully!")
        for i, df in enumerate(st.session_state.dfs):
            st.write(f"Preview of Dataset {i + 1}:")
            st.dataframe(df)

elif data_management_option == "Sanity Checks":
    st.header("Sanity Checks")
    if st.session_state.dfs:
        column_lengths = [len(df.columns) for df in st.session_state.dfs]
        column_names = [set(df.columns) for df in st.session_state.dfs]
        if len(set(column_lengths)) == 1 and len(set(frozenset(names) for names in column_names)) == 1:
            st.success("All datasets have consistent columns. Ready to merge!")
            if st.button("Merge Datasets"):
                st.session_state.df = pd.concat(st.session_state.dfs, ignore_index=True)
                st.write("Merged Data:")
                st.dataframe(st.session_state.df)
                save_data()
        else:
            st.error("Inconsistency detected in columns across the datasets.")
    else:
        st.warning("Please upload datasets first.")

elif data_management_option == "Merge Datasets":
    st.header("Merge Datasets")
    if st.session_state.df is not None:
        st.write("Merged Data:")
        st.dataframe(st.session_state.df)
    else:
        st.warning("No merged dataset available. Please perform sanity checks and merge the datasets.")

elif data_management_option == "Data Cleaning":
    st.header("Data Cleaning")
    cleaning_option = st.selectbox("Choose a cleaning option:", ["EDA", "Recode Variables", "Change Data Type", "Compute or Create New Variable", "Delete Column", "Sort Columns", "GroupBy", "Filter Data"])

    if cleaning_option == "EDA":
        if st.session_state.df is not None:
            option = st.radio("Choose analysis type:", ["Summary Statistics", "Variable Info", "Null Values Chart"])
            if option == "Summary Statistics":
                st.write("Summary Statistics:")
                st.write(st.session_state.df.describe())
            elif option == "Variable Info":
                st.write("Variable Info:")
                buffer = io.StringIO()
                st.session_state.df.info(buf=buffer)
                info_str = buffer.getvalue()
                st.text(info_str)
            elif option == "Null Values Chart":
                st.write("Null Values Chart:")
                for column in st.session_state.df.columns:
                    null_count = st.session_state.df[column].isnull().sum()
                    non_null_count = st.session_state.df[column].notnull().sum()
                    fig, ax = plt.subplots()
                    ax.bar(['Missing Values', 'Non-missing Values'], [null_count, non_null_count], color=['red', 'green'])
                    ax.set_title(f'Null vs Non-null Values for {column}')
                    ax.set_ylabel('Count')
                    st.pyplot(fig)
        else:
            st.warning("No dataset available. Please import and merge datasets first.")

    elif cleaning_option == "GroupBy":
        if st.session_state.df is not None:
            st.subheader("Group By Operation")
            
            # Select columns to group by
            group_columns = st.multiselect("Select columns to group by:", st.session_state.df.columns)
            
            if group_columns:
                # Select columns to apply operations on
                numeric_columns = st.session_state.df.select_dtypes(include=['number']).columns
                agg_columns = st.multiselect("Select columns to aggregate:", numeric_columns)
                
                if agg_columns:
                    # Select operations
                    operations = st.multiselect("Select operations to apply:", 
                                               ["sum", "mean", "median", "min", "max", "count", "std", "var"])
                    
                    if operations:
                        # Create aggregation dictionary
                        agg_dict = {col: operations for col in agg_columns}
                        
                        # Apply groupby
                        try:
                            grouped_df = st.session_state.df.groupby(group_columns).agg(agg_dict)
                            st.write("Grouped Data:")
                            st.dataframe(grouped_df)
                            
                            # Option to save the grouped data
                            if st.button("Save Grouped Data as New DataFrame"):
                                st.session_state.df = grouped_df.reset_index()
                                st.success("Grouped data saved as the current DataFrame.")
                                st.dataframe(st.session_state.df)
                                save_data()
                            
                            # Option to download grouped data
                            csv = grouped_df.to_csv().encode('utf-8')
                            st.download_button(
                                label="Download Grouped Data",
                                data=csv,
                                file_name="grouped_data.csv",
                                mime="text/csv"
                            )
                        except Exception as e:
                            st.error(f"Error performing groupby: {e}")
                    else:
                        st.warning("Please select at least one operation.")
                else:
                    st.warning("Please select columns to aggregate.")
            else:
                st.warning("Please select at least one column to group by.")
        else:
            st.warning("No dataset available. Please import and merge datasets first.")
            
    elif cleaning_option == "Filter Data":
        if st.session_state.df is not None:
            st.subheader("Filter Data")
            
            filter_method = st.radio("Choose filter method:", ["Simple Filter", "Advanced Filter (Query)"])
            
            if filter_method == "Simple Filter":
                # Select column to filter
                filter_column = st.selectbox("Select column to filter:", st.session_state.df.columns)
                
                # Display unique values for the column (limit to 20 for display purposes)
                unique_values = st.session_state.df[filter_column].unique()
                if len(unique_values) > 20:
                    st.warning(f"Column has {len(unique_values)} unique values. Showing only first 20.")
                    display_values = unique_values[:20]
                else:
                    display_values = unique_values
                    
                st.write("Sample of unique values:", display_values)
                
                # Handle different data types
                col_type = st.session_state.df[filter_column].dtype
                if np.issubdtype(col_type, np.number):
                    # Numeric filter
                    min_val = float(st.session_state.df[filter_column].min())
                    max_val = float(st.session_state.df[filter_column].max())
                    
                    filter_type = st.radio("Filter type:", ["Range", "Equal to", "Greater than", "Less than"])
                    
                    if filter_type == "Range":
                        range_min, range_max = st.slider("Select range:", min_val, max_val, (min_val, max_val))
                        filtered_df = st.session_state.df[(st.session_state.df[filter_column] >= range_min) & 
                                                         (st.session_state.df[filter_column] <= range_max)]
                    elif filter_type == "Equal to":
                        value = st.number_input("Enter value:", min_val, max_val)
                        filtered_df = st.session_state.df[st.session_state.df[filter_column] == value]
                    elif filter_type == "Greater than":
                        value = st.number_input("Enter minimum value:", min_val, max_val)
                        filtered_df = st.session_state.df[st.session_state.df[filter_column] > value]
                    else:  # Less than
                        value = st.number_input("Enter maximum value:", min_val, max_val)
                        filtered_df = st.session_state.df[st.session_state.df[filter_column] < value]
                else:
                    # Categorical filter
                    selected_values = st.multiselect("Select values to include:", unique_values)
                    if selected_values:
                        filtered_df = st.session_state.df[st.session_state.df[filter_column].isin(selected_values)]
                    else:
                        filtered_df = st.session_state.df.copy()
                        st.warning("No filter applied. Select at least one value.")
            
            else:  # Advanced Filter (Query)
                st.write("Available columns:", list(st.session_state.df.columns))
                query = st.text_area("Enter your query expression (e.g., 'column1 > 10 and column2 == \"value\"'):")
                
                if query:
                    try:
                        filtered_df = st.session_state.df.query(query)
                    except Exception as e:
                        st.error(f"Error in query: {e}")
                        filtered_df = st.session_state.df.copy()
                else:
                    filtered_df = st.session_state.df.copy()
                    st.warning("No filter applied. Enter a query to filter data.")
            
            # Display filtered data
            st.write(f"Filtered Data ({len(filtered_df)} rows):")
            st.dataframe(filtered_df)
            
            # Option to save filtered data
            if st.button("Save Filtered Data as Current DataFrame"):
                st.session_state.df = filtered_df.copy()
                st.success("Filtered data saved as the current DataFrame.")
                save_data()

    elif cleaning_option == "Compute or Create New Variable":
        st.header("Compute or Create New Variable")
        if st.session_state.df is not None:
            st.write("Available columns:")
            st.write(list(st.session_state.df.columns))

            expression = st.text_input("Write your expression using column names (e.g., A + B - (C * D)):")

            if st.checkbox("Add conditional logic?"):
                condition = st.text_input("Enter the condition (e.g., A > B):", key="condition")
                true_value = st.text_input("Enter the value when condition is true (number or text):", key="true_value")
                false_value = st.text_input("Enter the value when condition is false (number or text):", key="false_value")
                if condition and true_value and false_value:
                    expression = f"np.where({condition}, {true_value}, {false_value})"

            new_var_name = st.text_input("Enter the name for the new variable:", key="new_var_name")

            if st.button("Compute New Variable"):
                try:
                    if not new_var_name:
                        st.error("Please enter a name for the new variable.")
                    elif not expression:
                        st.error("Please enter a valid expression.")
                    else:
                        st.session_state.df[new_var_name] = st.session_state.df.eval(expression, engine='python')
                        st.success(f"Computed new variable '{new_var_name}':")
                        st.dataframe(st.session_state.df)
                        save_data()
                except Exception as e:
                    st.error(f"Error computing new variable: {e}")
        else:
            st.warning("No dataset available. Please import and merge datasets first.")

    elif cleaning_option == "Recode Variables":
        if st.session_state.df is not None:
            recode_option = st.selectbox("Choose recoding option:", ["Recode a Column", "Recode Values in a Column"])
            if recode_option == "Recode a Column":
                column = st.selectbox("Select column to recode", st.session_state.df.columns)
                new_name = st.text_input("New name for the selected column")
                if st.button("Recode"):
                    if new_name:
                        st.session_state.df.rename(columns={column: new_name}, inplace=True)
                        st.success(f"Column name updated:")
                        st.dataframe(st.session_state.df)
                        save_data()
                    else:
                        st.error("Please enter a new column name.")

            elif recode_option == "Recode Values in a Column":
                column = st.selectbox("Select column to recode", st.session_state.df.columns)
                old_values = st.text_input(f"Old values for {column} (comma-separated)")
                new_values = st.text_input(f"New values for {column} (comma-separated)")
                if old_values and new_values:
                    old_values_list = old_values.split(",")
                    new_values_list = new_values.split(",")
                    recode_map = dict(zip(old_values_list, new_values_list))
                    if st.button("Recode"):
                        st.session_state.df[column] = st.session_state.df[column].replace(recode_map)
                        st.success("Recoded Data:")
                        st.dataframe(st.session_state.df)
                        save_data()
                else:
                    st.error("Ensure you provide both old and new values.")

    elif cleaning_option == "Change Data Type":
        if st.session_state.df is not None:
            col = st.selectbox("Select column to change data type:", st.session_state.df.columns)
            dtype = st.selectbox("Select new data type:", ["int", "float", "str", "bool"])
            if st.button("Change Data Type"):
                try:
                    st.session_state.df[col] = st.session_state.df[col].astype(dtype)
                    st.success(f"Changed data type of {col} to {dtype}.")
                    st.dataframe(st.session_state.df)
                    save_data()
                except ValueError as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("No dataset available. Please import and merge datasets first.")

    elif cleaning_option == "Delete Column":
        if st.session_state.df is not None:
            columns_to_delete = st.multiselect("Select columns to delete:", st.session_state.df.columns)
            if st.button("Delete"):
                if columns_to_delete:
                    st.session_state.df.drop(columns=columns_to_delete, inplace=True)
                    st.success(f"Deleted columns: {', '.join(columns_to_delete)}")
                    st.dataframe(st.session_state.df)
                    save_data()
                else:
                    st.error("Please select at least one column to delete.")
        else:
            st.warning("No dataset available. Please import and merge datasets first.")

    elif cleaning_option == "Sort Columns":
        if st.session_state.df is not None:
            st.write("Current Column Order:")
            st.dataframe(st.session_state.df.head())
            new_order = st.multiselect("Rearrange columns by selecting them in the desired order:", st.session_state.df.columns, default=list(st.session_state.df.columns))
            if st.button("Rearrange Columns"):
                if len(new_order) == len(st.session_state.df.columns):
                    st.session_state.df = st.session_state.df[new_order]
                    st.success("Columns rearranged successfully.")
                    st.dataframe(st.session_state.df)
                    save_data()
                else:
                    st.error("Please select all columns to ensure the DataFrame structure is preserved.")
        else:
            st.warning("No dataset available. Please import and merge datasets first.")

elif data_management_option == "Quality Control/Checks":
    st.header("Quality Control/Checks")
    quality_control_option = st.selectbox("Choose a quality control option:", ["", "Check for Normality", "Outlier Detection", "Outlier Correction"])
    if quality_control_option == "Check for Normality":
        if st.session_state.df is not None:
            column = st.selectbox("Select column to check normality:", st.session_state.df.columns)
            if column:
                data = st.session_state.df[column].dropna()
                from scipy.stats import shapiro, normaltest, anderson
                p_value, _, _ = shapiro(data)
                st.write(f"Shapiro-Wilk Test p-value: {p_value:.8f}")
                if p_value > 0.05:
                    st.success("Data is likely normally distributed.")
                else:
                    st.warning("Data is not normally distributed.")
        else:
            st.warning("No dataset available. Please import and merge datasets first.")

if st.session_state.df is not None:
    if st.button("Undo Last Action"):
        undo_last_action()
        st.dataframe(st.session_state.df)
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

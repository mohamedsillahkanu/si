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
    cleaning_option = st.selectbox("Choose a cleaning option:", ["EDA", "Recode Variables", "Change Data Type", "Compute or Create New Variable", "Delete Column", "Sort Columns", "GroupBy", "Filter Data", "Split Column"])

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
            
            # Initialize saved filters dictionary if it doesn't exist
            if 'saved_filters' not in st.session_state:
                st.session_state.saved_filters = {}
            
            filter_method = st.radio("Choose filter method:", ["Multiple Column Filter", "Advanced Filter (Query)"])
            
            if filter_method == "Multiple Column Filter":
                # Allow selecting multiple columns to filter
                filter_columns = st.multiselect("Select columns to filter by:", st.session_state.df.columns)
                
                filtered_df = st.session_state.df.copy()
                active_filters = {}
                
                for filter_column in filter_columns:
                    st.subheader(f"Filter by {filter_column}")
                    
                    # Display unique values for the column
                    unique_values = st.session_state.df[filter_column].unique()
                    
                    # Handle different data types
                    col_type = st.session_state.df[filter_column].dtype
                    if np.issubdtype(col_type, np.number):
                        # Numeric filter
                        min_val = float(st.session_state.df[filter_column].min())
                        max_val = float(st.session_state.df[filter_column].max())
                        
                        filter_type = st.radio(f"Filter type for {filter_column}:", ["Range", "Equal to", "Greater than", "Less than"], key=f"filter_type_{filter_column}")
                        
                        if filter_type == "Range":
                            range_min, range_max = st.slider(f"Select range for {filter_column}:", min_val, max_val, (min_val, max_val), key=f"range_{filter_column}")
                            filtered_df = filtered_df[(filtered_df[filter_column] >= range_min) & (filtered_df[filter_column] <= range_max)]
                            active_filters[filter_column] = f"Between {range_min} and {range_max}"
                        elif filter_type == "Equal to":
                            value = st.number_input(f"Enter value for {filter_column}:", min_val, max_val, key=f"equal_{filter_column}")
                            filtered_df = filtered_df[filtered_df[filter_column] == value]
                            active_filters[filter_column] = f"= {value}"
                        elif filter_type == "Greater than":
                            value = st.number_input(f"Enter minimum value for {filter_column}:", min_val, max_val, key=f"gt_{filter_column}")
                            filtered_df = filtered_df[filtered_df[filter_column] > value]
                            active_filters[filter_column] = f"> {value}"
                        else:  # Less than
                            value = st.number_input(f"Enter maximum value for {filter_column}:", min_val, max_val, key=f"lt_{filter_column}")
                            filtered_df = filtered_df[filtered_df[filter_column] < value]
                            active_filters[filter_column] = f"< {value}"
                    else:
                        # Categorical filter with multiselect
                        if len(unique_values) > 100:
                            st.warning(f"Column has {len(unique_values)} unique values. Consider using a different filtering method.")
                        
                        selected_values = st.multiselect(f"Select values to include for {filter_column}:", unique_values, key=f"multiselect_{filter_column}")
                        if selected_values:
                            filtered_df = filtered_df[filtered_df[filter_column].isin(selected_values)]
                            active_filters[filter_column] = f"is in {selected_values}"
            
            else:  # Advanced Filter (Query)
                st.write("Available columns:", list(st.session_state.df.columns))
                query = st.text_area("Enter your query expression (e.g., 'column1 > 10 and column2 == \"value\"'):")
                
                if query:
                    try:
                        filtered_df = st.session_state.df.query(query)
                        active_filters = {"Query": query}
                    except Exception as e:
                        st.error(f"Error in query: {e}")
                        filtered_df = st.session_state.df.copy()
                        active_filters = {}
                else:
                    filtered_df = st.session_state.df.copy()
                    active_filters = {}
                    st.warning("No filter applied. Enter a query to filter data.")
            
            # Display summary of active filters
            if active_filters:
                st.subheader("Active Filters")
                for col, filter_desc in active_filters.items():
                    st.write(f"- {col}: {filter_desc}")
            
            # Display filtered data
            st.subheader(f"Filtered Data ({len(filtered_df)} rows out of {len(st.session_state.df)} total)")
            st.dataframe(filtered_df)
            
            # Option to save the filter with a name
            filter_name = st.text_input("Enter a name for this filter (required to save):")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Filter") and filter_name:
                    # Save filter but preserve the original dataframe
                    st.session_state.saved_filters[filter_name] = {
                        "filtered_df": filtered_df.copy(),
                        "active_filters": active_filters.copy()
                    }
                    st.success(f"Filter '{filter_name}' saved successfully. Original data preserved.")
            
            with col2:
                if st.button("Apply Filter as Current DataFrame") and active_filters:
                    st.session_state.df = filtered_df.copy()
                    st.success("Filtered data applied as the current DataFrame.")
                    save_data()
            
            # Option to download filtered data without changing original
            if active_filters:
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Filtered Data",
                    data=csv,
                    file_name=f"filtered_data{'_' + filter_name if filter_name else ''}.csv",
                    mime="text/csv"
                )
            
            # Display saved filters
            if st.session_state.saved_filters:
                st.subheader("Saved Filters")
                selected_filter = st.selectbox("Select a saved filter to view or apply:", 
                                             list(st.session_state.saved_filters.keys()))
                
                if selected_filter:
                    saved_filter = st.session_state.saved_filters[selected_filter]
                    st.write("Filter criteria:")
                    for col, filter_desc in saved_filter["active_filters"].items():
                        st.write(f"- {col}: {filter_desc}")
                    
                    st.write(f"Filtered data ({len(saved_filter['filtered_df'])} rows):")
                    st.dataframe(saved_filter["filtered_df"])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("Apply This Saved Filter"):
                            filtered_df = saved_filter["filtered_df"].copy()
                            active_filters = saved_filter["active_filters"].copy()
                            st.experimental_rerun()
                    
                    with col2:
                        if st.button("Set As Current DataFrame"):
                            st.session_state.df = saved_filter["filtered_df"].copy()
                            st.success(f"Filter '{selected_filter}' applied as current DataFrame.")
                            save_data()
                    
                    with col3:
                        if st.button("Delete This Filter"):
                            del st.session_state.saved_filters[selected_filter]
                            st.success(f"Filter '{selected_filter}' deleted.")
                            if st.session_state.saved_filters:
                                st.experimental_rerun()

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
            
    elif cleaning_option == "Split Column":
        if st.session_state.df is not None:
            st.subheader("Split Column")
            
            # Select column to split
            column_to_split = st.selectbox("Select column to split:", st.session_state.df.columns)
            
            # Display sample values
            sample_values = st.session_state.df[column_to_split].head(5).tolist()
            st.write("Sample values from selected column:", sample_values)
            
            # Choose split method
            split_method = st.radio("Choose split method:", [
                "Split by position (e.g., '201501' → '2015' and '01')",
                "Split by delimiter (e.g., 'first_last' → 'first' and 'last')",
                "Split date format (e.g., 'January 2015' → month and year)"
            ])
            
            if split_method == "Split by position (e.g., '201501' → '2015' and '01')":
                # Position-based splitting
                st.info("This will split the text based on character positions")
                
                # Get the length of the first non-null value to suggest positions
                sample_len = len(str(st.session_state.df[column_to_split].dropna().iloc[0])) if not st.session_state.df[column_to_split].dropna().empty else 0
                
                # If we have a sample, show splitting preview
                if sample_len > 0:
                    # Collect split positions
                    positions = []
                    
                    st.write(f"The selected column values have approximately {sample_len} characters")
                    
                    # Allow adding multiple split positions
                    num_splits = st.number_input("How many parts do you want to split into?", min_value=2, max_value=5, value=2)
                    
                    # Define the split positions
                    for i in range(1, num_splits):
                        pos = st.number_input(f"Position to split at (part {i})", 
                                             min_value=1, 
                                             max_value=sample_len-1,
                                             value=min(i * (sample_len // num_splits), sample_len-1))
                        positions.append(pos)
                    
                    # Sort positions to ensure they're in ascending order
                    positions.sort()
                    
                    # Show preview of split on first few rows
                    st.subheader("Preview of split result")
                    
                    # Create a preview table
                    preview_data = {"Original": []}
                    for i in range(num_splits):
                        preview_data[f"Part {i+1}"] = []
                    
                    # Get sample values for preview
                    sample_rows = st.session_state.df[column_to_split].dropna().head(5)
                    
                    for val in sample_rows:
                        str_val = str(val)
                        preview_data["Original"].append(str_val)
                        
                        # Split by positions
                        prev_pos = 0
                        for i, pos in enumerate(positions):
                            preview_data[f"Part {i+1}"].append(str_val[prev_pos:pos])
                            prev_pos = pos
                        
                        # Add the last part
                        preview_data[f"Part {num_splits}"].append(str_val[prev_pos:])
                    
                    # Display preview
                    st.table(pd.DataFrame(preview_data))
                    
                    # Get new column names
                    new_col_names = []
                    for i in range(num_splits):
                        new_name = st.text_input(f"Name for Part {i+1}:", value=f"{column_to_split}_{i+1}")
                        new_col_names.append(new_name)
                    
                    # Apply the split
                    if st.button("Apply Split"):
                        try:
                            # Convert to string to ensure consistent behavior
                            str_series = st.session_state.df[column_to_split].astype(str)
                            
                            # Split by positions
                            prev_pos = 0
                            for i, pos in enumerate(positions):
                                st.session_state.df[new_col_names[i]] = str_series.str.slice(prev_pos, pos)
                                prev_pos = pos
                            
                            # Add the last part
                            st.session_state.df[new_col_names[-1]] = str_series.str.slice(prev_pos)
                            
                            st.success("Column split successfully")
                            st.dataframe(st.session_state.df)
                            save_data()
                        except Exception as e:
                            st.error(f"Error splitting column: {e}")
                else:
                    st.error("Cannot determine the length of values in the selected column. Ensure it contains non-null values.")
            
            elif split_method == "Split by delimiter (e.g., 'first_last' → 'first' and 'last')":
                # Delimiter-based splitting
                delimiter = st.text_input("Enter delimiter (e.g., '_', '-', ',', etc.)", value="_")
                
                # Count expected parts after split
                if delimiter:
                    try:
                        # Use a sample to estimate number of parts
                        sample = st.session_state.df[column_to_split].dropna().iloc[0]
                        num_parts = len(str(sample).split(delimiter))
                        st.write(f"Splitting will create approximately {num_parts} parts")
                        
                        # Preview split
                        st.subheader("Preview of split result")
                        preview_data = {"Original": []}
                        
                        # Maximum reasonable number of parts to expect
                        max_parts = 10
                        for i in range(max_parts):
                            preview_data[f"Part {i+1}"] = []
                        
                        # Get sample values for preview
                        sample_rows = st.session_state.df[column_to_split].dropna().head(5)
                        max_parts_found = 0
                        
                        for val in sample_rows:
                            str_val = str(val)
                            preview_data["Original"].append(str_val)
                            parts = str_val.split(delimiter)
                            max_parts_found = max(max_parts_found, len(parts))
                            
                            # Add parts to preview
                            for i, part in enumerate(parts):
                                if i < max_parts:
                                    preview_data[f"Part {i+1}"].append(part)
                            
                            # Fill in empty values for missing parts
                            for i in range(len(parts), max_parts):
                                preview_data[f"Part {i+1}"].append("")
                        
                        # Trim preview to only show relevant parts
                        for i in range(max_parts_found, max_parts):
                            del preview_data[f"Part {i+1}"]
                        
                        # Display preview
                        st.table(pd.DataFrame(preview_data))
                        
                        # Get new column names
                        new_col_names = []
                        for i in range(max_parts_found):
                            new_name = st.text_input(f"Name for Part {i+1}:", value=f"{column_to_split}_{i+1}")
                            new_col_names.append(new_name)
                        
                        # Apply the split
                        if st.button("Apply Split"):
                            try:
                                # Convert all values to string
                                str_series = st.session_state.df[column_to_split].astype(str)
                                
                                # Create new columns for each part
                                for i in range(max_parts_found):
                                    st.session_state.df[new_col_names[i]] = str_series.str.split(delimiter).str[i]
                                
                                st.success("Column split successfully")
                                st.dataframe(st.session_state.df)
                                save_data()
                            except Exception as e:
                                st.error(f"Error splitting column: {e}")
                    except Exception as e:
                        st.error(f"Cannot preview split: {e}")
                else:
                    st.error("Please enter a delimiter")
            
            elif split_method == "Split date format (e.g., 'January 2015' → month and year)":
                # Date format splitting
                st.info("This will attempt to parse dates and extract components")
                
                # Determine the format of the date
                date_format = st.selectbox("Select date format in your column:", [
                    "Auto-detect",
                    "Month Year (e.g., 'January 2015')",
                    "Year-Month (e.g., '2015-01')",
                    "Day-Month-Year (e.g., '15-Jan-2020')",
                    "Custom format"
                ])
                
                custom_format = ""
                if date_format == "Custom format":
                    custom_format = st.text_input("Enter custom date format (e.g., '%Y%m' for '202001'):")
                    st.write("Common format codes: %Y=year, %m=month, %d=day, %b=abbreviated month name")
                
                # Choose which components to extract
                components = st.multiselect("Select date components to extract:", 
                                          ["Year", "Month (numeric)", "Month (name)", "Day", "Quarter", "Week of year"])
                
                # Preview conversion
                if components:
                    try:
                        # Get sample data
                        sample_rows = st.session_state.df[column_to_split].dropna().head(5)
                        
                        preview_data = {"Original": sample_rows.tolist()}
                        component_cols = {}
                        
                        # Initialize component columns
                        for comp in components:
                            component_cols[comp] = []
                        
                        # Process each sample
                        for val in sample_rows:
                            # Try to parse the date
                            try:
                                if date_format == "Auto-detect":
                                    # Try common formats
                                    try:
                                        # For 'January 2015' type formats
                                        date_val = pd.to_datetime(val)
                                    except:
                                        try:
                                            # For '201501' type formats
                                            date_val = pd.to_datetime(val, format='%Y%m')
                                        except:
                                            # Last resort
                                            date_val = pd.to_datetime(val, errors='coerce')
                                
                                elif date_format == "Month Year (e.g., 'January 2015')":
                                    date_val = pd.to_datetime(val)
                                
                                elif date_format == "Year-Month (e.g., '2015-01')":
                                    date_val = pd.to_datetime(val)
                                
                                elif date_format == "Day-Month-Year (e.g., '15-Jan-2020')":
                                    date_val = pd.to_datetime(val)
                                
                                elif date_format == "Custom format" and custom_format:
                                    date_val = pd.to_datetime(val, format=custom_format)
                                
                                # Extract components
                                for comp in components:
                                    if comp == "Year":
                                        component_cols[comp].append(date_val.year)
                                    elif comp == "Month (numeric)":
                                        component_cols[comp].append(date_val.month)
                                    elif comp == "Month (name)":
                                        component_cols[comp].append(date_val.strftime("%B"))
                                    elif comp == "Day":
                                        component_cols[comp].append(date_val.day)
                                    elif comp == "Quarter":
                                        component_cols[comp].append(date_val.quarter)
                                    elif comp == "Week of year":
                                        component_cols[comp].append(date_val.isocalendar()[1])
                            
                            except Exception as e:
                                # If parsing fails, add placeholders
                                for comp in components:
                                    component_cols[comp].append(f"Error: {str(e)[:20]}...")
                        
                        # Create preview dataframe
                        for comp, values in component_cols.items():
                            preview_data[comp] = values
                        
                        # Display preview
                        st.subheader("Preview of date components")
                        st.table(pd.DataFrame(preview_data))
                        
                        # Get column names for the new components
                        new_col_names = {}
                        for comp in components:
                            default_name = f"{column_to_split}_{comp.lower().replace(' ', '_')}"
                            new_col_names[comp] = st.text_input(f"Name for {comp} column:", value=default_name)
                        
                        # Apply the extraction
                        if st.button("Apply Date Extraction"):
                            try:
                                # Try to parse all dates
                                if date_format == "Auto-detect":
                                    date_series = pd.to_datetime(st.session_state.df[column_to_split], errors='coerce')
                                elif date_format == "Custom format" and custom_format:
                                    date_series = pd.to_datetime(st.session_state.df[column_to_split], format=custom_format, errors='coerce')
                                else:
                                    date_series = pd.to_datetime(st.session_state.df[column_to_split], errors='coerce')
                                
                                # Extract and add each component
                                for comp, new_name in new_col_names.items():
                                    if comp == "Year":
                                        st.session_state.df[new_name] = date_series.dt.year
                                    elif comp == "Month (numeric)":
                                        st.session_state.df[new_name] = date_series.dt.month
                                    elif comp == "Month (name)":
                                        st.session_state.df[new_name] = date_series.dt.strftime("%B")
                                    elif comp == "Day":
                                        st.session_state.df[new_name] = date_series.dt.day
                                    elif comp == "Quarter":
                                        st.session_state.df[new_name] = date_series.dt.quarter
                                    elif comp == "Week of year":
                                        st.session_state.df[new_name] = date_series.dt.isocalendar().week
                                
                                st.success("Date components extracted successfully")
                                st.dataframe(st.session_state.df)
                                save_data()
                            except Exception as e:
                                st.error(f"Error extracting date components: {e}")
                    
                    except Exception as e:
                        st.error(f"Error previewing date extraction: {e}")
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

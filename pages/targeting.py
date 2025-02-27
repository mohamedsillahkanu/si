import streamlit as st
import pandas as pd
import numpy as np
import base64
from io import BytesIO

st.set_page_config(page_title="Dataset Logical Conditioner", layout="wide")

def read_file(file):
    """Read uploaded file into a dataframe."""
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith(('.xlsx', '.xls')):
        return pd.read_excel(file)
    else:
        st.error(f"Unsupported file format: {file.name}")
        return None

# Initialize session state
if 'datasets' not in st.session_state:
    st.session_state.datasets = {}
if 'merged_df' not in st.session_state:
    st.session_state.merged_df = None
if 'conditions' not in st.session_state:
    st.session_state.conditions = []
if 'result_column_name' not in st.session_state:
    st.session_state.result_column_name = "result"
if 'logic_operator' not in st.session_state:
    st.session_state.logic_operator = "AND"
if 'true_value' not in st.session_state:
    st.session_state.true_value = "Yes"
if 'false_value' not in st.session_state:
    st.session_state.false_value = "No"

# App header
st.title("Dataset Logical Conditioner")

# Sidebar for uploading files
with st.sidebar:
    st.header("Upload Datasets")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload dataset (CSV or Excel)", type=['csv', 'xlsx', 'xls'], key="file_upload")
    
    if uploaded_file is not None:
        dataset_name = st.text_input("Enter a name for this dataset:", 
                                     value=uploaded_file.name.split('.')[0])
        
        if st.button("Add Dataset"):
            df = read_file(uploaded_file)
            if df is not None:
                st.session_state.datasets[dataset_name] = df
                st.success(f"Added dataset: {dataset_name}")
    
    # Show currently loaded datasets
    if st.session_state.datasets:
        st.subheader("Loaded Datasets")
        for name in st.session_state.datasets.keys():
            st.write(f"- {name} ({len(st.session_state.datasets[name])} rows)")
        
        if st.button("Clear All Datasets"):
            st.session_state.datasets = {}
            st.session_state.merged_df = None
            st.session_state.conditions = []
            st.experimental_rerun()

# Main workspace
tab1, tab2, tab3 = st.tabs(["Merge Datasets", "Create Conditions", "Download Results"])

# Tab 1: Merge Datasets
with tab1:
    st.header("Merge Datasets")
    
    if len(st.session_state.datasets) < 1:
        st.info("Please upload at least 1 dataset in the sidebar.")
    else:
        # Select datasets to merge
        st.subheader("Select Datasets to Merge")
        
        dataset_names = list(st.session_state.datasets.keys())
        
        if len(dataset_names) == 1:
            # If only one dataset, use it directly
            base_dataset = dataset_names[0]
            st.info(f"Using dataset: {base_dataset}")
            result_df = st.session_state.datasets[base_dataset].copy()
            st.session_state.merged_df = result_df
            
            # Display dataset preview
            st.subheader("Dataset Preview")
            st.dataframe(st.session_state.merged_df.head())
            st.info(f"Total columns: {len(st.session_state.merged_df.columns)}")
        else:
            # If multiple datasets, allow merging
            base_dataset = st.selectbox("Select base dataset:", dataset_names)
            
            merge_list = []
            merge_settings = {}
            
            # Start with base dataset
            if base_dataset:
                base_df = st.session_state.datasets[base_dataset]
                result_df = base_df.copy()
                
                # Setup for merging additional datasets
                for i, name in enumerate([n for n in dataset_names if n != base_dataset]):
                    if st.checkbox(f"Merge with {name}", key=f"merge_{i}"):
                        merge_list.append(name)
                        
                        # Find common columns
                        second_df = st.session_state.datasets[name]
                        common_cols = list(set(result_df.columns).intersection(set(second_df.columns)))
                        
                        # Select merge columns
                        merge_cols = st.multiselect(
                            f"Select columns to join on for {name}:",
                            common_cols,
                            default=common_cols[0] if common_cols else None,
                            key=f"cols_{i}"
                        )
                        
                        # Select merge type
                        merge_type = st.selectbox(
                            f"Join type for {name}:",
                            ["Left join", "Inner join", "Right join", "Outer join"],
                            key=f"type_{i}"
                        )
                        
                        # Store merge settings for this dataset
                        merge_settings[name] = {
                            "columns": merge_cols,
                            "type": merge_type
                        }
                
                # Perform merge button
                if st.button("Perform Merge"):
                    if not merge_list:
                        # If no datasets selected for merge, just use the base dataset
                        result_df = base_df.copy()
                        st.session_state.merged_df = result_df
                        st.success(f"Using dataset: {base_dataset}")
                    else:
                        result_df = base_df.copy()
                        
                        # Sequentially merge datasets
                        for name in merge_list:
                            second_df = st.session_state.datasets[name]
                            merge_cols = merge_settings[name]["columns"]
                            merge_how = {
                                "Left join": "left",
                                "Inner join": "inner", 
                                "Right join": "right",
                                "Outer join": "outer"
                            }[merge_settings[name]["type"]]
                            
                            # Perform the merge
                            result_df = pd.merge(
                                result_df, 
                                second_df,
                                on=merge_cols,
                                how=merge_how,
                                suffixes=(f'', f'_{name}')
                            )
                        
                        st.session_state.merged_df = result_df
                        st.success(f"Successfully merged {len(merge_list)+1} datasets! Result has {len(result_df)} rows.")
                
                # Display merged result preview
                if st.session_state.merged_df is not None:
                    st.subheader("Merged Dataset Preview")
                    st.dataframe(st.session_state.merged_df.head())
                    st.info(f"Total columns: {len(st.session_state.merged_df.columns)}")

# Tab 2: Create Conditions
with tab2:
    st.header("Create Conditions with AND/OR Logic")
    
    if st.session_state.merged_df is None:
        st.info("Please prepare your dataset in the 'Merge Datasets' tab first.")
    else:
        # Define result settings
        st.subheader("1. Set Result Column Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            result_column_name = st.text_input(
                "Name for the result column:", 
                value=st.session_state.result_column_name
            )
            st.session_state.result_column_name = result_column_name
        
        with col2:
            logic_operator = st.selectbox(
                "Combine conditions with:", 
                options=["AND", "OR"],
                index=0 if st.session_state.logic_operator == "AND" else 1
            )
            st.session_state.logic_operator = logic_operator
        
        st.write("#### Values for Result Column")
        col1, col2 = st.columns(2)
        with col1:
            true_value = st.text_input(
                "Value when conditions are TRUE:", 
                value=st.session_state.true_value
            )
            st.session_state.true_value = true_value
        
        with col2:
            false_value = st.text_input(
                "Value when conditions are FALSE:", 
                value=st.session_state.false_value
            )
            st.session_state.false_value = false_value
        
        # Add conditions
        st.subheader("2. Add Conditions")
        
        # Create form to add a new condition
        with st.form("add_condition_form"):
            st.write("#### New Condition")
            
            all_columns = st.session_state.merged_df.columns.tolist()
            source_column = st.selectbox("Select column:", all_columns)
            
            # Show sample values for the selected column
            if source_column:
                unique_values = st.session_state.merged_df[source_column].dropna().unique()
                if len(unique_values) > 5:
                    st.write(f"Sample values: {', '.join(map(str, unique_values[:5]))}, ...")
                else:
                    st.write(f"Unique values: {', '.join(map(str, unique_values))}")
            
            # Operator selection
            operator = st.selectbox(
                "Condition operator:", 
                options=["equals", "not equals", "greater than", "less than", "contains", "does not contain"]
            )
            
            # Value for condition
            if source_column and len(unique_values) <= 20 and operator in ["equals", "not equals"]:
                # If few unique values and using equals/not equals, show dropdown
                condition_value = st.selectbox(
                    "Select value:",
                    options=unique_values
                )
            else:
                # Otherwise use text input
                condition_value = st.text_input(
                    "Enter value for condition:"
                )
            
            submit_condition = st.form_submit_button("Add Condition")
        
        if submit_condition and source_column and condition_value:
            new_condition = {
                "column": source_column,
                "operator": operator,
                "value": condition_value
            }
            st.session_state.conditions.append(new_condition)
            st.success(f"Added condition: {source_column} {operator} {condition_value}")
            st.experimental_rerun()
        
        # Display existing conditions
        if st.session_state.conditions:
            st.subheader("3. Current Conditions")
            
            # Display each condition with a remove button
            for i, condition in enumerate(st.session_state.conditions):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"{condition['column']} {condition['operator']} '{condition['value']}'")
                
                with col3:
                    if st.button("Remove", key=f"remove_{i}"):
                        st.session_state.conditions.pop(i)
                        st.experimental_rerun()
            
            st.write(f"These conditions will be combined with {st.session_state.logic_operator} logic.")
            
            # Apply conditions button
            if st.button("Apply Conditions"):
                result_df = st.session_state.merged_df.copy()
                
                # Apply conditions based on the logical operator
                if st.session_state.conditions:
                    # Initialize a mask based on the logic operator
                    if st.session_state.logic_operator == "AND":
                        # Start with all True for AND logic
                        final_mask = pd.Series([True] * len(result_df))
                    else:  # OR
                        # Start with all False for OR logic
                        final_mask = pd.Series([False] * len(result_df))
                    
                    # Apply each condition to build the mask
                    for condition in st.session_state.conditions:
                        column = condition["column"]
                        operator = condition["operator"]
                        value = condition["value"]
                        
                        # Convert value to numeric if the column is numeric
                        if pd.api.types.is_numeric_dtype(result_df[column]) and str(value).replace('.', '', 1).isdigit():
                            value = float(value)
                        
                        # Apply the operator to create a condition mask
                        if operator == "equals":
                            condition_mask = result_df[column] == value
                        elif operator == "not equals":
                            condition_mask = result_df[column] != value
                        elif operator == "greater than":
                            condition_mask = result_df[column] > value
                        elif operator == "less than":
                            condition_mask = result_df[column] < value
                        elif operator == "contains":
                            condition_mask = result_df[column].astype(str).str.contains(str(value), na=False)
                        elif operator == "does not contain":
                            condition_mask = ~result_df[column].astype(str).str.contains(str(value), na=False)
                        
                        # Combine with final mask based on logic operator
                        if st.session_state.logic_operator == "AND":
                            final_mask = final_mask & condition_mask
                        else:  # OR
                            final_mask = final_mask | condition_mask
                    
                    # Create the result column
                    result_df[result_column_name] = np.where(
                        final_mask, 
                        true_value, 
                        false_value
                    )
                    
                    st.session_state.merged_df = result_df
                    st.success(f"Successfully applied conditions and created column: {result_column_name}")
                    
                    # Show preview
                    st.subheader("Result Preview")
                    st.dataframe(st.session_state.merged_df.head())
                else:
                    st.error("Please add at least one condition.")

# Tab 3: Download Results
with tab3:
    st.header("Download Results")
    
    if st.session_state.merged_df is None:
        st.info("Please prepare your dataset before downloading.")
    else:
        st.subheader("Preview Final Dataset")
        st.dataframe(st.session_state.merged_df.head())
        
        st.subheader("Download Options")
        filename = st.text_input("Enter filename for download (without extension):", value="processed_data")
        
        file_format = st.radio("Select file format:", ["CSV", "Excel"])
        
        if st.button("Generate Download Link"):
            try:
                if file_format == "CSV":
                    csv = st.session_state.merged_df.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Click here to download {filename}.csv</a>'
                else:
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        st.session_state.merged_df.to_excel(writer, index=False, sheet_name='Results')
                    b64 = base64.b64encode(buffer.getvalue()).decode()
                    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}.xlsx">Click here to download {filename}.xlsx</a>'
                
                st.markdown(href, unsafe_allow_html=True)
                st.success(f"Download link generated for {filename}!")
            except Exception as e:
                st.error(f"Error generating download: {e}")

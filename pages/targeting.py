import streamlit as st
import pandas as pd
import numpy as np
import base64
from io import BytesIO

st.set_page_config(page_title="Dataset Conditioner", layout="wide")

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
if 'selected_columns' not in st.session_state:
    st.session_state.selected_columns = []
if 'column_conditions' not in st.session_state:
    st.session_state.column_conditions = {}
if 'result_column_name' not in st.session_state:
    st.session_state.result_column_name = "result"

# App header
st.title("Dataset Conditioner")

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
            st.session_state.selected_columns = []
            st.session_state.column_conditions = {}
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
    st.header("Create Conditions")
    
    if st.session_state.merged_df is None:
        st.info("Please prepare your dataset in the 'Merge Datasets' tab first.")
    else:
        # Step 1: Select columns for conditions
        st.subheader("1. Select Columns for Conditions")
        
        all_columns = st.session_state.merged_df.columns.tolist()
        selected_columns = st.multiselect(
            "Select columns to create conditions for:",
            options=all_columns
        )
        
        # Update the selected columns in session state
        if st.button("Confirm Selected Columns"):
            st.session_state.selected_columns = selected_columns
            # Reset column conditions if columns changed
            st.session_state.column_conditions = {col: {} for col in selected_columns}
            st.success(f"Selected {len(selected_columns)} columns for conditions")
        
        # Step 2: Define conditions for each selected column
        if st.session_state.selected_columns:
            st.subheader("2. Define Conditions for Selected Columns")
            
            # Name for the result column
            result_column_name = st.text_input(
                "Name for the result column:", 
                value=st.session_state.result_column_name
            )
            st.session_state.result_column_name = result_column_name
            
            # Create a section for each selected column
            for col in st.session_state.selected_columns:
                with st.expander(f"Condition for: {col}", expanded=True):
                    # Get unique values for the column
                    unique_values = st.session_state.merged_df[col].dropna().unique()
                    
                    # Display unique values for reference
                    if len(unique_values) > 10:
                        st.write(f"Column has {len(unique_values)} unique values. Sample: {', '.join(map(str, unique_values[:10]))}, ...")
                    else:
                        st.write(f"Unique values: {', '.join(map(str, unique_values))}")
                    
                    # Select a value for the condition
                    if len(unique_values) <= 20:
                        # If few unique values, use a selectbox
                        selected_value = st.selectbox(
                            f"Select value to check for in {col}:",
                            options=unique_values,
                            key=f"value_{col}"
                        )
                    else:
                        # If many unique values, use a text input
                        selected_value = st.text_input(
                            f"Enter value to check for in {col}:",
                            key=f"value_{col}"
                        )
                    
                    # Define what happens when condition is met
                    true_value = st.text_input(
                        f"Value when {col} equals '{selected_value}':",
                        value="Yes" if col not in st.session_state.column_conditions else st.session_state.column_conditions[col].get("true_value", "Yes"),
                        key=f"true_{col}"
                    )
                    
                    false_value = st.text_input(
                        f"Value when {col} does not equal '{selected_value}':",
                        value="No" if col not in st.session_state.column_conditions else st.session_state.column_conditions[col].get("false_value", "No"),
                        key=f"false_{col}"
                    )
                    
                    # Save this column's condition settings
                    if st.button(f"Save condition for {col}"):
                        st.session_state.column_conditions[col] = {
                            "value": selected_value,
                            "true_value": true_value,
                            "false_value": false_value
                        }
                        st.success(f"Saved condition for column: {col}")
            
            # Display summary of all conditions
            if st.session_state.column_conditions:
                st.subheader("3. Summary of Defined Conditions")
                
                for col, condition in st.session_state.column_conditions.items():
                    if "value" in condition:
                        st.write(f"- If {col} equals '{condition['value']}', set to '{condition['true_value']}', otherwise '{condition['false_value']}'")
                
                # Apply all conditions button
                if st.button("Apply All Conditions"):
                    result_df = st.session_state.merged_df.copy()
                    
                    # Initialize the result column with default value (first column's false value)
                    default_value = list(st.session_state.column_conditions.values())[0]["false_value"]
                    result_df[result_column_name] = default_value
                    
                    # Apply each condition
                    for col, condition in st.session_state.column_conditions.items():
                        if "value" in condition:
                            # Create a mask for where this condition is true
                            mask = result_df[col] == condition["value"]
                            
                            # Update the result column where the condition is true
                            result_df.loc[mask, result_column_name] = condition["true_value"]
                    
                    st.session_state.merged_df = result_df
                    st.success(f"Applied all conditions and created column: {result_column_name}")
                    
                    # Show preview of result
                    st.subheader("Result Preview")
                    st.dataframe(st.session_state.merged_df.head())

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
